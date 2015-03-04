import os
import re
import csv


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



    
with open('output.csv', 'w') as f:
    w = csv.writer(f)

    for fname, entries in out.items():
        for entry in entries:
            w.writerow(entry.values())
