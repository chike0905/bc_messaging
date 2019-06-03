import json
import urllib.request

import keys

def postrequest(url, port, data):
    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url+":"+port, json.dumps(data).encode(), headers)

    try:
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
    except urllib.error.HTTPError as err:
        code = err.code
        return False, code
    except urllib.error.URLError as err:
        code = err.code
        return False, code
    return True, body


url = 'http://localhost'
port = "8545"

addr = keys.addr
pw = keys.pw

def sendTransaction(addr, pw):
    data = {
        "jsonrpc":"2.0",
        "method":"",
        "params":[],
        "id":1
        }
    # UnlockAccount
    data["method"] = "personal_unlockAccount"
    data["params"] = [addr, pw]
    result, response = postrequest(url, port, data)
    print(response)
    if not result:
        return 0

    # send Transaction
    data["method"] = "eth_sendTransaction"
    data["params"] = [{
                    "from": addr,
                    "data": "0x1111"
                    }]
    result, response = postrequest(url, port, data)
    print(response)
    if not result:
        return 0

    # LockAccount
    data["method"] = "personal_lockAccount"
    data["params"] = [addr]
    result, response = postrequest(url, port, data)
    print(response)
    if not result:
        return 0

sendTransaction(addr, pw)
