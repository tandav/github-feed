import json
import time
import datetime

import credentials
import ghfeed


def make_json():
    user_2_avatar = dict(ghfeed.get_following(credentials.user, pages=(1, 2), fields=('login', 'avatar_url')))
    user_2_avatar[credentials.user] = 'https://via.placeholder.com/400'
    users = tuple(user_2_avatar) + (credentials.user,)
    events = ghfeed.get_events(users)

    data = {
        'user_2_avatar': user_2_avatar,
        'events': events,
        'updated': int(datetime.datetime.now().timestamp()) * 1000,
    }
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
    while True:
        try:
            make_json()
        except Exception as e:
            print(f'error while make_json():\n{e}')
        time.sleep(60 * 10)
