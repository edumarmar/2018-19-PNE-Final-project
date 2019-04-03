
import requests

server = "http://rest.ensembl.org"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
info=[]


resource = "/xrefs/symbol/homo_sapiens/"+ 'FRAT1'+'?'
print(resource)
r = requests.get(server + resource, headers=headers)
decoded = r.json()
id = decoded[0]['id']
print(id)

resource="/sequence/id/"+str(id)
print(resource)
r = requests.get(server + resource, headers=headers)
decoded = r.json()
seq=decoded['seq']

resource = "/lookup/id/" + id
r = requests.get(server + resource, headers=headers)
decoded = r.json()
print(decoded['start'], decoded['end'], len(seq), id)