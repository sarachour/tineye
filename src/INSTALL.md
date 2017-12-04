## Installation Guide

Tineye is a python utility that enables downloading code from the blockchain.
Tineye depends on several python packages. We recommend the following package versions:
    
    web3 3.16.4


### Python 2.7
`tineye` requires `python-2.7`. 
Install the following packages with pip:

    pip install web3 matplotlib colormap easydev
   
    
### Python 3
`tineye` has been developed with the following versions of the packages:

    pip3 install web3 matplotlib colormap easydev
    
installing `web3` might require an upgrade of setuptools:
    
    pip3 install --upgrade setuptools
    
We recommend the following package versions.


  
## Downloading from the Blockchain

First, execute the `geth` server and allow it to start.

    geth --rpc --rpcapi "eth,net,web3,debug" --cache=1024 --syncmode full

`tineye` requires the programmer specify the starting block and the number of blocks to download. By default, `tineye` stores the downloaded data in the `.db/ethereum.db`. For example, the following command downloads contracts from blocks 620,000 to 620,099.

    python3 tineye.py download --start 620000 --n 100
   
   
## Inspecting contracts on the blockchain 

The smart contracts are organized by the contract id, which is the hash of the source code. To retrieve the list of contracts, and the number transactions involving each contract, use the following command:

    python3 tineye.py stats --metric usage

To retrieve the list of contracts and their size, use the following command:

    python3 tineye.py stats --metric size
  
To retrieve the list of contracts, and how many times the contract has been copied, use the following command:

    python3 tineye.py stats --metric dups
   
Each of these commands will return a tab-delimited list of the form:

    007d5a5af7225b77a49c4ccb214edb50862480d5	9928
    aaa47b2a0275e2d22d8cad58594264d41e6a59c8	2434
    f625028de562d2de7316af6c042d9bbb20511bd3	1530
    d8f963ca3bdada6f1c1ffa36da8037bbeba83e12	11348
    89d9b8ee82b61a531a35081bb17c6c9618d5fbf1	100
    87d5899da0de5a6590c0b065a8ef0374dadddb07	3648

Where the first number is the hash of the code, and the second number is the metric specified (size/usage/dups).

## Inspecting the contract code

`tineye` supports retrieving the code of smart contracts. To do so, find the program id (the hash of the code) of the contract of interest, and execute the following command:


