# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server

# -- This file is only to check that the information(json) can be
# -- received with a client.

import http.client
import json


ENDPOINT= 'http://localhost:8000/gengene=PLCXD1&json=1'
PATH= ENDPOINT[21:]
PORT = 8000
SERVER = 'localhost'


try:
    print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

    # Connect with the server
    conn = http.client.HTTPConnection(SERVER, PORT)

    # -- Send the request message, using the GET method. We are
    # -- requesting the main page (/)
    conn.request("GET", PATH+'&json=1')

    # -- Read the response message from the server
    r1 = conn.getresponse()

    # -- Print the status line
    print("Response received!: {} {}\n".format(r1.status, r1.reason))

    # -- Read the response's body
    data = r1.read().decode("utf-8")


    # -- Create a variable with the data,
    # -- form the JSON received
    results = json.loads(data)
    print("CONTENT: ")
    print(results)
except:
    print('***ERROR!!! That endpoint is not working in this server***')