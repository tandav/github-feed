import requests
import itertools
import random
import string
import collections
import tqdm
from collections.abc import Iterable
from typing import Union

import pipe21 as P


def get_following(
    user: str,
    pages: tuple,
    fields=('login', 'avatar_url'),
) -> list:
    users = []
    for page in pages:
        p = {'per_page': 100, 'page': page}
        for user in requests.get(f'https://api.github.com/users/{user}/following', params=p).json():
            users.append(tuple(user[field] for field in fields))
    return users


def get_events(user: Union[str, Iterable]) -> list:
    if isinstance(user, str): # one user
        print(user)
        return (
            requests
            .get(f'https://api.github.com/users/{user}/events')
            .json()
            | P.Map(lambda e: (e['created_at'].split('T')[0], user, e['repo']['name'], e['type']))
            | P.Pipe(list)
        )
    elif isinstance(user, Iterable):
        events = []
        for u in tqdm.tqdm(user):
            events += get_events(u)
        return events
        #return user | P.FlatMap(get_events) | P.Pipe(sorted)
    else:
        raise TypeError
