import json
content={'caca':{'1':39, '2':324}}

with open('data.json', 'w') as outfile:
    json.dump(content, outfile)