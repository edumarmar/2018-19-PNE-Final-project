import requests

server = "http://rest.ensembl.org"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
info=[]

chromo='7'
start='0'
end='90000'

resource = "/overlap/region/human/"+chromo+":"+start+'-'+end+'?feature=gene;'
print(resource)
r = requests.get(server + resource, headers=headers)
decoded = r.json()

info=''
for i in range(len(decoded)):
    name=decoded[i]['external_name']
    info+='<p></p>'+str(name)


print(info)