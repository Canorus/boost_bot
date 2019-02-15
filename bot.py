import requests
import json
from credential import retrieve
import os
import re

base = os.path.dirname(os.path.abspath(__file__))
instance = input('Please input your instance: ')
if instance[:5] !='https':
    instance = 'https://'+instance
user_name = input('Please input your username: ')

acc = retrieve(user_name, instance)
head = {'Authorization':'Bearer '+acc}
uri = instance+'/api/v1/streaming/user'
r_user = requests.get(uri,headers=head,stream=True)

def boost(toot_id):
    requests.post(instance+'/api/v1/statuses/'+toot_id+'/reblog',headers=head)

with open(base+'/boost_list.txt','r') as f:
    boost_list = f.read().split('\n')

for l in r_user.iter_lines():
    dec = l.decode('utf-8')
    try:
        newdec = json.loads(re.sub('data: ','',dec))
        print(newdec)
        if newdec['reblog']:
            user_name = newdec['reblog']['account']['acct']
        else:
            user_name = newdec['account']['acct']
        print('user_name is '+user_name)
        if user_name in boost_list:
            print('id in list')
            id = str(newdec['id'])
            boost(id)
    except:
        print(dec)
