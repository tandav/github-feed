import datetime
import json
import operator
import string
from pathlib import Path

import pipe21 as P
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import util

app = FastAPI()

HTML_TEMPLATE = string.Template(open('template.html').read())

class User:
    def __init__(self, username, events, avatar_url):
        self.username = username
        self.events = events
        self.avatar_url = avatar_url

    @property
    def events_html(self):
        html = ''
        now = datetime.datetime.utcnow()

        for event in self.events:
            ago = util.ago((now - datetime.datetime.fromisoformat(event['timestamp'][:-1])).total_seconds())
            # timestamp = f"<code>{datetime.datetime.fromisoformat(event['timestamp'][:-1]).strftime('%Y-%m-%d %H:%M')}</code>"
            timestamp = f"<code>{ago}</code>"
            event_type = f"<code>{event['type']}</code>"
            repo = f"<code>{event['repo']}</code>"

            if event['type'] == 'PushEvent':
                for commit in event['url']:
                    html += f'''
                    <li>{timestamp} | {event_type} {repo} <a href='{commit['url']}'>{commit['message']}</a></li>
                    '''
            elif event['type'] in {'CreateEvent', 'DeleteEvent'}:
                html += f'''
                <li>{timestamp} | {event_type} {repo} {event['url']['type']} <a href='{event['url']['url']}'>{event['url']['url']}</a></li>
                '''
            else:
                html += f'''
                <li>{timestamp} | {event_type} {repo} <a href='{event['url']}'>{event['url'].split('https://github.com/')[1]}</a></li>
                '''

        return f'''
        <ul class='user_events'>
        {html}
        </ul>
        '''

    def _repr_html_(self):
        return f'''
        <div class='user card'>
            <a class='user_header' href='https://github.com/{self.username}'><img src='{self.avatar_url}&s=64'><h1 class='username'>{self.username}</h1></a>
            {self.events_html}
        </div>
        '''


data_file = Path('data.json')


@app.get("/", response_class=HTMLResponse)
async def root():
    if not data_file.exists():
        return 'page is creating, please reload page after 1-2 minutes'

    with open(data_file) as f: data = json.load(f)
    user_2_avatar = data['user_2_avatar']
    events = data['events']

    events = [
        event for event in events
        if (datetime.date.today() - datetime.datetime.fromisoformat(event['timestamp'][:-1]).date()).days < 3
    ]

    user_events = (
        events
        | P.GroupBy(operator.itemgetter('user'))
        | P.MapValues(lambda it: sorted(it, key=operator.itemgetter('timestamp'), reverse=True))
        | P.Pipe(lambda it: sorted(it, key=lambda kv: kv[1][0]['timestamp'], reverse=True))
    )

    feed = ''
    for user, u_events in user_events:
        feed += User(user, u_events, user_2_avatar[user])._repr_html_()
    return HTML_TEMPLATE.substitute(updated=data['updated'], feed=feed)
