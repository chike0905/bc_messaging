import json
import urllib.request
import binascii
import cfg 
import sys
from getpass import getpass


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
    if result != True or "error" in response.keys():
      print("%s:%s" % (response["error"]["code"], response["error"]["message"]))
      return 0
    print("Account %s is unlocked." % fromaddr)
    
    # send Transaction
    hexdata = binascii.hexlify(data.encode("utf-8")).decode("utf-8") 
    prms["method"] = "eth_sendTransaction"
    prms["params"] = [{
                    "from": fromaddr,
                    "to": toaddr,
                    "data": "0x" + hexdata
                    }]
    result, response = postrequest(cfg.url, cfg.port, prms)
    if result != True or "error" in response.keys():
      print("%s:%s" % (response["error"]["code"], response["error"]["message"]))
      return 0
    print("Message TX is created (%s)." % response["result"])

    # LockAccount
    prms["method"] = "personal_lockAccount"
    prms["params"] = [fromaddr]
    result, response = postrequest(cfg.url, cfg.port, prms)
    if result != True or "error" in response.keys():
      print("%s:%s" % (response["error"]["code"], response["error"]["message"]))
      return 0
    print("Account %s is locked." % fromaddr)

if __name__ == '__main__':
   args = sys.argv
   fromaddr = args[1]
   toaddr = args[2]
   senddata = args[3]
   
   pw = getpass('your password for %s: ' % fromaddr)
   sendMsgTransaction(fromaddr, toaddr, senddata, pw)
