import requests
import json
from credential import retrieve
import os
import re

base = os.path.dirname(os.path.abspath(__file__))
instance = input('Please input your instance: ')
user_name = input('Please input your username: ')

acc = retrieve(user_name, instance)
head = {'Authorization':'Bearer '+acc}
uri = instance+'/api/v1/streaming/user'
r_user = requests.get(uri,headers=head,stream=True)

def boost(toot_id):
    requests.post(instance+'/api/v1/statuses/'+toot_id+'/reblog',headers=head)

with open(base+'/boostlist.txt','r') as f:
    boost_list = f.read().split(',')

for l in r_user.iter_lines():
    dec = l.decode('utf-8')
    try:
        newdec=json.loads(re.sub('data: ','',dec))
        if newdec['reblog']:
            user_name = newdec['reblog']['account']['acct']
        else:
            user_name = newdec['account']['acct']
        id = str(newdec['id'])
        if user_name in boost_list:
            boost(id)
