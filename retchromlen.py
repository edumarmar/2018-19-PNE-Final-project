import requests


server = "http://rest.ensembl.org"
resource = "/info/assembly/mouse?"
headers={ "Content-Type" : "application/json", "Accept" : "application/json"}

r = requests.get(server+resource, headers=headers)

decoded=r.json()
karyo=decoded['karyotype']
karyo.remove('MT')

chromosomes=decoded['top_level_region']
for chrom in chromosomes:
    if chrom['name'] in karyo:
        print(chrom['name'], chrom['length'])