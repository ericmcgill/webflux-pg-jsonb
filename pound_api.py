import json
import requests

number_of_records = 21
for i in range(int(number_of_records+1)):
    url = f"http://localhost:8888/api/thing/{i}"
    print(url)
    r = requests.get(url)
    # print(r.headers)
    if r.status_code == 200:
        if 'Content-Length' in r.headers:
            cl = int(r.headers['Content-Length'])
            actual = len(r.text)
            if cl != actual:
                print(f">>> MISMATCH: cl: {cl} / actual: {actual} for id: {i}")
            else:
                print(f"... good for id: {i}")
    else:
        print(f"XXX {r.status_code} for id: {i}")