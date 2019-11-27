import hashlib
import hmac
import time
import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def build_indico_request(path, params, api_key=None, secret_key=None, only_public=False, persistent=False):
    items = list(params.items()) if hasattr(params, 'items') else list(params)
    if api_key:
        items.append(('apikey', api_key))
    if only_public:
        items.append(('onlypublic', 'yes'))
    if secret_key:
        if not persistent:
            items.append(('timestamp', str(int(time.time()))))
        items = sorted(items, key=lambda x: x[0].lower())
        url = '%s?%s' % (path, urlencode(items))
        signature = hmac.new(secret_key.encode('utf-8'), url.encode('utf-8'),
                             hashlib.sha1).hexdigest()
        items.append(('signature', signature))
    if not items:
        return path
    return '%s?%s' % (path, urlencode(items))


if __name__ == '__main__':
    eventId = input("Please enter ID of the event you want to get: ")
	
    API_KEY = 'd672f1fd-d6f3-43cd-8579-0707b41730a2'
    SECRET_KEY = ''
    PATH = f'http://localhost:9090/export/event/{eventId}.json?occ=yes&pretty=yes'
    PARAMS = {
        'limit': 123
    }

    indico_request = build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY)
    r = requests.get(indico_request)
    event = r.json()
    event = event['results'][0]
    
    display = '\n'

    if event['title']:
        title = event['title']
        display += f'Title: {title}\n'

    if event['startDate']['date']:
        startDate = event['startDate']['date']
        display += f'Start date: {startDate}\n'

    if event['endDate']['date']:
        endDate = event['endDate']['date']
        display += f'End date: {endDate}\n'
    
    if event['type']:
        eventType = event['type']
        display += f'Type: {eventType}\n'
    
    if event['description']:
        description = event['description']
        display += f'Description: {description}'
        
    print(display)


