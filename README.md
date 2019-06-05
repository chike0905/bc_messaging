# BC Messaging
Massaging over Blcokchain

- inspired from [This paper](https://ieeexplore.ieee.org/document/8029983)

## Enviroment
- Python 3.6.0
- Geth 1.8.27-stable

## Operation summary
![sequence](https://github.com/chike0905/bc_messaging/blob/img/sequence.png)
- Message is emmbeded to TX and included to Blockchain.
- Since it is difficult to rewrite the blockchain, you can take the TX in the blockchain as proof that the messaging existed.

## How to Use
- You should setup sender's ethereum account in geth node that this script connects.
   - Default is localhost (configured in cfg.py). 

### Send Message
```
python sender.py "sender's ethereum address" "reciever's ethereum address" message
```
- You are asked password for the sender's account on geth node.

### Recieve Message
- In recieving message, you don't need to setup reciever's address.
   - just input address as parameter
```
python reciever.py "reciever's ethereum address"
```
