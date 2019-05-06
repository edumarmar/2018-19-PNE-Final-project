import http.client
import json

#here is a list of endpoint that can be tested. More endpoints can be added
ENDPOINTS= ['http://localhost:8000/listSpecies?limit=5&json=1',
'http://localhost:8000/karyotype?specie=cat&json=1',
'http://localhost:8000/chromosomeLength?specie=mouse&chromo=3&json=1',
'http://localhost:8000/geneSeq?gene=FRAT1&json=1',
'http://localhost:8000/geneInfo?gene=PLCXD1&json=1',
'http://localhost:8000/geneCal?gene=FRAT2&json=1',
"http://localhost:8000/geneList?chromo=4&start=1&end=400000&json=1"
]

for ENDPOINT in ENDPOINTS:

    PATH= ENDPOINT[21:]
    PORT = 8000
    SERVER = 'localhost'

    try:
        # Connect with the server
        conn = http.client.HTTPConnection(SERVER, PORT)

        # -- Send the request message, using the GET method. We are
        # -- requesting the main page (/)
        conn.request("GET", PATH+'&json=1')

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Read the response's body
        data = r1.read().decode("utf-8")


        # -- Create a variable with the data,
        # -- form the JSON received
        results = json.loads(data)
        print("\n-------------------------------------------CONTENT FOR ",PATH,  '-------------------------------------------')
        print(results)
    except:
        print('***ERROR!!! That endpoint is not working in this server***')