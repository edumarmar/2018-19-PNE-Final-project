import requests


server = "http://rest.ensembl.org"
resource = "/info/species"
headers={ "Content-Type" : "application/json", "Accept" : "application/json"}

r = requests.get(server+resource, headers=headers)

decoded=r.json()
species=(decoded['species'])
for i in species:
    print(i['name'])
