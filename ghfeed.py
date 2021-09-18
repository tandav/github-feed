import operator
from collections.abc import Iterable
from typing import Optional
from typing import Union

import pipe21 as P
import requests
import tqdm

from credentials import user_token


def get_following(
    user: str,
    pages: tuple,
    fields: Optional[tuple] = None,
) -> list:
    users = []
    for page in pages:
        for followed_user in requests.get(
            f'https://api.github.com/users/{user}/following',
            params={'per_page': 100, 'page': page},
            auth=user_token,
        ).json():
            if fields is None:
                users.append(followed_user)
            else:
                users.append(tuple(followed_user[field] for field in fields))
    return users


def commits_info(commits):
    out = []
    for commit in commits:
        url = commit['url'].replace('//api.', '//').replace('/repos', '').replace('/commits', '/commit')
        message = commit['message'].splitlines()[0]
        out.append({'url': url, 'message': message})
    return out


def create_event_info(e):
    create_type = e['payload']['ref_type']
    if create_type == 'repository':
        url = e['repo']['url'].replace('//api.', '//').replace('/repos', '')
    elif create_type == 'branch':
        url = e['repo']['url'].replace('//api.', '//').replace('/repos', '') + '/tree/' + e['payload']['ref']
    elif create_type == 'tag':
        url = e['repo']['url'].replace('//api.', '//').replace('/repos', '') + '/releases/tag/' + e['payload']['ref']
    return {'url': url, 'type': create_type}

not_supported_events_yet = {'MemberEvent', 'GollumEvent'}

def get_event_url(event):
    t = event['type']
    if   t == 'IssuesEvent': return event['payload']['issue']['html_url']
    # elif t == 'IssueCommentEvent': return event['payload']['issue']['url']
    elif t == 'WatchEvent': return event['repo']['url'].replace('//api.', '//').replace('/repos', '')
    elif t == 'PublicEvent': return f"https://github.com/{event['repo']['name']}"
    elif t == 'PushEvent': return commits_info(event['payload']['commits'])
    elif t == 'ReleaseEvent': return event['payload']['release']['html_url']
    elif t == 'PullRequestEvent': return event['payload']['pull_request']['url'].replace('//api.', '//').replace('/repos', '')
    elif t == 'PullRequestReviewEvent': return event['payload']['review']['html_url']
    elif t == 'PullRequestReviewCommentEvent': return event['payload']['comment']['html_url']
    elif t == 'ForkEvent': return event['payload']['forkee']['html_url']
    elif t in {'IssueCommentEvent', 'CommitCommentEvent'}: return event['payload']['comment']['html_url']
    elif t == 'CreateEvent': return create_event_info(event)
    elif t == 'DeleteEvent': return create_event_info(event)
    # elif t == 'DeleteEvent': return f"https://github.com/{event['repo']['name']}"
    else: raise TypeError(f'cant handle event of type {t}')


def get_events_raw(user: Union[str, Iterable]) -> list:
    if isinstance(user, str):  # one user
        return (
            requests
            .get(f'https://api.github.com/users/{user}/events', auth=user_token)
            .json()
        )
    elif isinstance(user, Iterable):
        events = []
        t = tqdm.tqdm(user)
        for u in t:
            t.set_description(u)
            events += get_events_raw(u)
        return events
        # return user | P.FlatMap(get_events) | P.Pipe(sorted)
    else:
        raise TypeError

def get_events(user: Union[str, Iterable]) -> list:
    return (
        get_events_raw(user)
        | P.Filter(lambda e: e['type'] not in not_supported_events_yet)
        | P.Map(lambda e: (dict(
            user = e['actor']['login'],
            date = e['created_at'].split('T')[0],
            timestamp = e['created_at'],
            repo = e['repo']['name'],
            type = e['type'],
            url = get_event_url(e))
        ))
        | P.Pipe(lambda it: sorted(it, key=operator.itemgetter('user', 'date', 'repo', 'type', 'timestamp')))
    )
