import hashlib
import hmac
import time
import requests
import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

API_KEY = 'd672f1fd-d6f3-43cd-8579-0707b41730a2'
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
    PATH = f'http://localhost:9090/export/event/{eventId}.json?occ=yes&pretty=yes'

    indico_request = build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY)
    r = requests.get(indico_request)
    event = r.json()
    
    # If event was found
    if (event['results']):
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
    else:
        display = 'No event matches the given id.'
        
    print(display)

def writeEvent():
    eventTitle = input('Title: ') or 'Test'
    eventStartDate = input('Start date (dd/mm/yyyy): ') or '01/01/2020'
    eventStartHour = input('Start hour (hh:mm): ') or '16:00'
    eventEndDate = input('End date (dd/mm/yyyy): ') or '01/01/2020'
    eventEndHour = input('End hour (hh:mm): ') or '17:00'

    PATH = f'http://localhost:9090/event/create/meeting'
    data = json.dumps({
        'event-creation-title': eventTitle,
        'event-creation-start_dt': [eventStartDate, eventStartHour],
        'event-creation-end_dt': [eventEndDate, eventEndHour]
    })

    indico_request = build_indico_request(PATH, PARAMS, API_KEY, SECRET_KEY)
    r = requests.post(indico_request, data)
    print(r.status_code)
    

if __name__ == '__main__':
    option = input(
'''
Enter number of your action (only meeting supported yet):
  - get an event: 1
  - create event: 2

Your choice: ''')

    if option == '1':
        getEvent()

    elif option == '2':
        writeEvent()

