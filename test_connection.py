import requests
from credentials import user_token


print(requests.get('https://api.github.com/users/tandav/events', auth=user_token).json())

