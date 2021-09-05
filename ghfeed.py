import requests
import itertools
import random
import string
import collections
import tqdm
from collections.abc import Iterable
from typing import Union

from credentials import user_token
import pipe21 as P


def get_following(
    user: str,
    pages: tuple,
    fields=('login', 'avatar_url'),
) -> list:
    users = []
    for page in pages:
        for followed_user in requests.get(
            f'https://api.github.com/users/{user}/following',
            params={'per_page': 100, 'page': page},
            auth=user_token,
        ).json():
            users.append(tuple(followed_user[field] for field in fields))
    return users


def get_events(user: Union[str, Iterable]) -> list:
    if isinstance(user, str): # one user
        return (
            requests
            .get(f'https://api.github.com/users/{user}/events', auth=user_token)
            .json()
            | P.Map(lambda e: (e['created_at'].split('T')[0], user, e['repo']['name'], e['type']))
            | P.Pipe(list)
        )
    elif isinstance(user, Iterable):
        events = []
        t = tqdm.tqdm(user)
        for u in t:
            t.set_description(u)
            events += get_events(u)
        return events
        #return user | P.FlatMap(get_events) | P.Pipe(sorted)
    else:
        raise TypeError
