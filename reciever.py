import json
import urllib.request
import binascii
import sys

import cfg


# TODO: create common function and remove / original in main.py 
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


def pollingchain(addr): 
    print("Searching Meassage to %s" % addr)
    prms = {
        "jsonrpc":"2.0",
        "method":"",
        "params":[],
        "id":1
        }

    counter = 0
    flag = True
    while(flag): 
      prms["method"] = "eth_getBlockByNumber"
      prms["params"] = [hex(counter), True]
      result, response = postrequest(cfg.url, cfg.port, prms)
      if not result:
         return 0
      
      if not response["result"]:
         flag = False 
      else:
         if len(response["result"]["transactions"]):
            for tx in response["result"]["transactions"]:
               if tx["to"] == addr:
                  print("----------------------")
                  print("Message is found in Block %s" % response["result"]["hash"])
                  bytemsg = binascii.unhexlify(tx["input"][2:])
                  msg = bytemsg.decode("utf-8")
                  print("TxID: %s" % tx["hash"])
                  print("From: %s" % tx["from"])
                  print("Message: %s" % msg)
         counter += 1 

if __name__ == '__main__':
   args = sys.argv
   addr = args[1]
   pollingchain(addr)
   
