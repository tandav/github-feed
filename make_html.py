import datetime
import operator
import string
import collections
import pipe21 as P
import ghfeed





class User:
    def __init__(self, username, events, avatar_url):
        self.username = username
        self.events = events
        self.avatar_url = avatar_url

    @property
    def events_html(self):
        html = ''

        for event in self.events:
            # timestamp = f"<code>{datetime.datetime.fromisoformat(event['timestamp'][:-1]).strftime('%Y-%m-%d %H:%M')}</code>"
            timestamp = f"<code>{event['ago']}</code>"
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
            <span class='user_header'><a href='https://github.com/{self.username}'><img src='{self.avatar_url}&s=64'><h3>{self.username}</h3></a></span>
            {self.events_html}
        </div>
        '''




def main():
    user_2_avatar = dict(ghfeed.get_following('tandav', pages=(1, 2), fields=('login', 'avatar_url')))
    len(user_2_avatar)

    users = tuple(user_2_avatar)
    events = ghfeed.get_events(users)
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
    html = string.Template(open('template.html').read()).substitute(
        updated=int(datetime.datetime.now().timestamp()) * 1000, feed=feed)
    open('index.html', 'w').write(html)


if __name__ == '__main__':
    main()
