HACKxFDU DSharing
===

# Introduction
A renting platform based on block chain and iot. This repo consists of chain code built on hyperledger composer and a web application used as a interface. The demo is about renting houses or apartments.

# Dependencies
* ibm bluemix & blockchain service (cloud service)
* ibm hyperledger-composer environment
* python2.7 & package Flask
* jquery

# How to start
* Register ibm account and build blockchain service following tutorials. (bluemix CLI & kubectl CLI are needed)
* Connect to `playground` online or set up local hyperledger-composer environment.
* Modify the code and deploy the chain.
* Config restful api of blockchain on bluemix.
* Using http `POST` and `GET` to interact with blockchain.

# Contribution & future plan
Zero-knowledge-proof is a prospective extension. In addition, the privacy of users should be protected better. More properties, such as cryptology encryption on users' identity, limited admissions of ordinary users and the proof whether service provider is qualified to meet consumers' need, should be carefully considered. Also, we hope the platform could satisfy more services to deploy and create a safe, fast and easy access to solve common problems.

