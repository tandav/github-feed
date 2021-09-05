import datetime
import operator
import string
import collections
import pipe21 as P

import ghfeed


user_2_avatar = dict(ghfeed.get_following('tandav', pages=(1, 2), fields=('login', 'avatar_url')))
len(user_2_avatar)

users = tuple(user_2_avatar)
events = ghfeed.get_events(users)
events = [
    event for event in events
    if (datetime.date.today() - datetime.datetime.strptime(event[0], '%Y-%m-%d').date()).days < 5
]

feed = ''

g0 = P.GroupBy(operator.itemgetter(0))
for day, day_events in events | g0:
    feed += f'<h2>{day}</h1>\n'
    day_events = day_events | P.Map(operator.itemgetter(1, 2, 3)) | P.Pipe(list)
    for user, user_events in day_events | g0:
        feed += f'''
        <a href='https://github.com/{user}'>
            <img src='{user_2_avatar[user]}&s=64'>
            <h3>{user}</h3>
        </a>
        '''

        user_events = user_events | P.Map(operator.itemgetter(1, 2)) | P.Pipe(list)
        for repo, repo_events in user_events | g0:
            repo_events = repo_events | P.Map(operator.itemgetter(1)) | P.Pipe(collections.Counter)
            repo_events = ' '.join(f'{e}: {n}' for e, n in sorted(repo_events.items()))
            feed += f"<a href='https://github.com/{repo}'><span>{repo}: {repo_events}</span></a>\n"
            # print(day, user, repo, repo_events)
    feed += '<hr>\n\n'

html = string.Template(open('template.html').read()).substitute(feed=feed)
open('index.html', 'w').write(html)
