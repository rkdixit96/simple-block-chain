# Simple Block Chain/ Motu Coin
This is a simple implementation of a block chain created as a part of this [udemy course](https://udemy.com/course/build-your-blockchain-az). It has also been extended to implement a crypto currency called motu coin. A simulation of the multiple nodes in the motu coin network and their interaction is done using docker-compose.

## Local setup of generic block chain
1. Create python virtual environment  
`virtualenv -p python3.9 simple-block-chain`
2. Activate the virtual environment  
`source ./simple-block-chain/bin/activate` 
3. Install poetry  
`pip install poetry`
4. Install packages  
`poetry install`
5. Run the api server  
`python api.py`

## Local setup of motu coin network
1. Bring up all the nodes in coin network  
`docker-compose up`
2. Connect all  nodes to each other. This is the curl to connect node1 to the other 2 nodes. Run corresponding curls for the other nodes
```
curl --location --request POST 'localhost:5001/connect_node' \
--header 'Content-Type: application/json' \
--data-raw '{
    "nodes": [
        "http://node2:5000",
        "http://node3:5000"
    ]
}'
```
3. Mine the block from `node1`
```
curl --location --request GET 'localhost:5001/mine_block'
```
4. Make a transaction from `user1` to `user3` on `node1`
```
curl --location --request POST 'localhost:5001/add_transaction' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sender": "user1",
    "receiver": "user3",
    "amount": 3
}'
```
5. Mine a block from `node1` again to add the transaction to the blockchain
```
curl --location --request GET 'localhost:5001/mine_block'
```
6. Mine a block from `node2`
```
curl --location --request GET 'localhost:5002/mine_block'
```
7. Sync chains across chain and observe that the current chain is replaced by the longest chain 
```
curl --location --request GET 'localhost:5002/replace_chain'
```


