import requests

server = "http://rest.ensembl.org"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
resource = "/info/species"
r = requests.get(server + resource, headers=headers)



decoded=r.json()
species = (decoded['species'])
print(len(species))
for i in species:
    print(i)