import json
import urllib.request
import binascii
import cfg 

# for debug
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
        print(err.reason)
        return False, None
    except urllib.error.URLError as err:
        print(err.reason)
        return False, None
    return True, body

'''
sendMsgTransaction - Sending Message Transation via Geth JSON-RPC API

input:
   fromaddr(str)  : sender's ethereum address
   toaddr(str)    : reciever's ethereum address
   data(str)      : sending string data
   pw(str)        : password for sender's private key on geth 
'''
def sendMsgTransaction(fromaddr, toaddr, data, pw):
    prms = {
        "jsonrpc":"2.0",
        "method":"",
        "params":[],
        "id":1
        }
    # UnlockAccount
    prms["method"] = "personal_unlockAccount"
    prms["params"] = [fromaddr, pw]
    result, response = postrequest(cfg.url, cfg.port, prms)
    if not result:
        return 0
    print(response)
    
    # send Transaction
    hexdata = binascii.hexlify(data.encode("utf-8")).decode("utf-8") 
    prms["method"] = "eth_sendTransaction"
    prms["params"] = [{
                    "from": fromaddr,
                    "to": toaddr,
                    "data": "0x" + hexdata
                    }]
    result, response = postrequest(cfg.url, cfg.port, prms)
    if not result:
        return 0
    print(response)

    # LockAccount
    prms["method"] = "personal_lockAccount"
    prms["params"] = [fromaddr]
    result, response = postrequest(cfg.url, cfg.port, prms)
    if not result:
        return 0
    print(response)

addr = keys.addr
pw = keys.pw

senddata = "Hello from blockchain!"
sendMsgTransaction(addr, "0x0000000000000000000000000000000000000000", senddata, pw)
