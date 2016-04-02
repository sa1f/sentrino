import requests
import json
import os.path
import os

if not os.path.isfile('info.json'):
    print "Please give information. This will be saved in info.json and used for future requests"
    username = raw_input("Enter your username: ")
    password = raw_input("Enter your passowrd: ")
    did = raw_input("Enter your did number: ")
    dst = raw_input("Enter your destination number: ")
    message = raw_input("Enter your message: ")
    infoIn = {"api_username": username, "api_password": password, "did": did, "dst": dst, "message": message,
            'method' : 'sendSMS'}
    with open('info.json', 'w') as outfile:
        json.dump(infoIn, outfile)

with open('info.json', 'r') as infile:
    info = json.load(infile)

r = requests.get('https://voip.ms/api/v1/rest.php', params=info)
print r.text
