import hashlib
import hmac
import time
import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

API_KEY = 'eecedc48-34ea-4131-8784-ef9a5a8a0d48'
SECRET_KEY = ''
PARAMS = {
    'limit': 123
}

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
        signature = hmac.new(secret_key.encode('utf-8'), url.encode('utf-8'), hashlib.sha1).hexdigest()
        items.append(('signature', signature))
    if not items:
        return path
    return '%s?%s' % (path, urlencode(items))

def getEvent():
    eventId = input('\nEnter ID of the event you want to get: ')
    # PATH = f'http://vps758705.ovh.net:9090/export/event/{eventId}.json?occ=yes&pretty=yes'
    PATH = 'http://vps758705.ovh.net:9090/export/event/{}.json?occ=yes&pretty=yes'.format(eventId)

    indico_request = build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY)
    r = requests.get(indico_request)
    event = r.json()
    
    # If event was found
    if (event['results']):
        event = event['results'][0]
    
        display = '\n'

        if event['title']:
            title = event['title']
            display += 'Title: {}\n'.format(title)

        if event['startDate']['date']:
            startDate = event['startDate']['date']
            display += 'Start date: {}\n'.format(startDate)

        if event['endDate']['date']:
            endDate = event['endDate']['date']
            display += 'End date: {}\n'.format(endDate)

        if event['type']:
            eventType = event['type']
            display += 'Type: {}\n'.format(eventType)

        if event['description']:
            description = event['description']
            display += 'Description: {}'.format(description)

    else:
        display = 'No event matches the given id.'
        
def createEvent():
    try:
        import indico
    except ImportError as e:
        # Mon erreur (Guillaume)
        print(e)

if __name__ == '__main__':
    option = input(
'''
Enter number of your action (only meeting supported yet):
  - get an event: 1
  - create event: 2

Your choice: ''')

    if option == 1:
        getEvent()

    elif option == 2:
        createEvent()
