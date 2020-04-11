import requests

API_KEY = '43b92a648c3db579499a902b89d61ef1'

headers = {
    'user-agent': 'constellation'
}

payload = {
    'api_key': API_KEY,
    'method': 'chart.gettopartists',
    'format': 'json'
}

r = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
r.status_code