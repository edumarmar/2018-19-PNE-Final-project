
import requests

server = "http://rest.ensembl.org"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
info=[]

resource = "/sequence/id/ENSG00000157764?"
r = requests.get(server + resource, headers=headers)
decoded = r.json()
print(decoded)