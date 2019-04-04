
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

info=[]
for i in decoded:
    name=i['assembly_name']
    gene_id=i['gene_id']
    info1=('Gene name: '+ str(name)+'     Gene id: '+str(gene_id))
    print(info1)
    try:
        info=info.append(info1)
    except:
        pass

info = '<p></p>'.join(info)



