import os
import re
import csv
import requests
import json

default_region = '55281ecfff0036363ab0eba0'

## import result data, like
# 'name' : 'a name',
# 'event' : '200 fly',
# 'time' : 60.25,
# 'splits' : [30.20, 30.05],
# 'team' : 'a team',
# 'place': 10,
# 'prelims' : true

reg_event = re.compile(r'Event\s+\d{1,3}\s+(?P<event>[a-zA-Z 0-9]+)')

reg_entry = re.compile(r'(?P<place>\d{1,2}|[-]{2}).+(?P<first>\b[A-Za-z]+)[,]\s(?P<last>\w+)\s+(?P<middle>\w{1}|)\s+(?P<grade>\w{2}|\s)\s+(?P<school>[^\s]+).+(?P<prelim>\d:\d{2}.\d{2}|NT\s+).+\s(?P<final>(X|)\d{1,2}:\d{2}.\d{2}|\d{2}.\d{2})\s+\n\s+(?P<splits>(((\d{2}.\d{2}|\d{1,2}:\d{2}.\d{2})\s+){1,2}.+(\n\s+|))+)')

out = {}




def procHtm(fname):
    length = 0
    print(fname)
    out[fname] = []
    with open(fname, 'r') as f:
        temp = str(f.read())

    #for each in eventNumberAndName.finditer(temp):
    #    number = each.group('eventNumber')
    #    name = each.group('eventName')
    #    print(number, name)
    e = reg_event.search(temp)
    event = e.groupdict()['event']
    r = reg_entry.finditer(temp)
    if r is not None:
        for each in r:
            splits = [x.strip() for x in each.groupdict()['splits'].split() if x is not '' and x[0]!='(' and x[-1]!=')']
#            if len(splits) != length:
#                print(each.groupdict()['splits'])
#                length = len(splits)

            d = each.groupdict()
            d['splits'] = splits
            d['event'] = event
            out[fname].append(d)
   



# which function handles which filetype
filesbytype = {
        'htm' : procHtm
        }


# walk current directory for files of appropriate type
f = os.walk('./')
for root, dirs, files in f:
    for _file in files:
        _type = _file.split('.')[-1]
        if _type in filesbytype:
            filesbytype[_type](_file)
        else:
            pass


url = "http://zagrobelny.us/api/team"
req = requests.get(url)
teams = req.json()
team_id = {}
for each in teams:
    team_id[str(each['name'])] = str(each['_id'])

url = "http://zagrobelny.us/api/player"
req = requests.get(url)
players = req.json()
player_id = {}
for each in players:
    name = each['name']
    team = each['team']
    tup = (str(name['first']), str(name['last']), str(team))

    player_id[tup] = str(each['_id'])


    
purl = "http://zagrobelny.us/api/record/"

with open('output.csv', 'w') as f:
    w = csv.writer(f)

    unique_names = set([])
    unique_teams = set([])
    name_index = {}
    for fname, entries in out.items():
        for entry in entries:
            q = {}
            # first, last
            n = (entry['last'], entry['first'], team_id[entry['school']]) # first, last, teamid

            unique_names.update([n])
            unique_teams.update([entry['school']]);

            _id = player_id[n] # get the player with those props
            t = {}
            t['event'] = entry['event']
            t['prelim'] = entry['prelim']
            t['final'] = entry['final']
            t['place'] = entry['place']

            q['parent'] = _id;
            q['value'] = t

            req = requests.post(purl, data=json.dumps(q), headers={"Content-Type": "application/json"})
            req.json()

            #q['time'] = t;
            #w.writerow(entry.values())

    # get ids of teams
    url = 'http://zagrobelny.us/api/team/'
    #d = list([{'name': x} for x in unique_teams])
    #id_name = {}
    #for team in d:
    #  req = requests.post(url, data=team)
    #  res = req.json()
    #  name = res['name']
    #  _id = res['_id']
    #  id_name[name] = _id

    #with open('json.out', 'w') as f:
    #    f.write(json.dumps(id_name))

    #purl = 'http://zagrobelny.us/api/player/'
    #player_byname = {}
    #for player in unique_names:
    #    n = {'first': player[0], 'last': player[1]}
    #    obj = {'name' : n, 'team': team_id[player[2]], 'region': default_region}
    #    #print(obj)
    #    req = requests.post(purl, data=json.dumps(obj), headers={"Content-Type": "application/json"})
    #    res = req.json()
    #    print(res)

