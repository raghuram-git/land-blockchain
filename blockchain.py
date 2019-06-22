import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests
class blockchain(object):

    def __init__(self,addr):
        self.chain = []
        self.transaction = []
        self.nodes = set()
        self.new_block(previous_hash=1,proof=100)
        self.address=addr
    def new_block(self, proof, previous_hash=None):
        block = {'index' : len(self.chain)+1,
                 'timestamp': time(),
                 'transaction': self.transaction,
                 'proof': proof,
                 'previous_hash': previous_hash or self.h_ash(self.chain[-1]),
                 }
        self.transaction = []
        self.chain.append(block)
        return block

    def new_transaction(self, party1, party2, surveyno):
        self.transaction.append({'party1': party1,
                                 'party2': party2,
                                 'surveyno':surveyno,
                                })
        c=self.last_block()
        return c['index']+1

    def h_ash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def last_block(self):
        b=self.chain[-1]
        return b

    def proof_of_work(self,last_proof):
        proof=0
        while self.proof_val(last_proof, proof) is False:
            proof+=1
        return proof

    def proof_val(self,last_proof,proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self,address):
        parse_url=urlparse(address)
        self.nodes.add(parse_url.netloc)

    def valid_chain(self,chain):
        last_block = chain[0]
        current_index=1
        while(current_index<len(chain)):
            block=chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            if block['previous_hash'] != self.h_ash(last_block):
                return False
            if  not self.proof_val(last_block['proof'],block['proof']):
                return False

            last_block=block
            current_index+=1

        return True

    def resolve_conflict(self):
        neighbours=self.nodes
        new_chain=None
        max_length=len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code  == 200:
                length=response.json()['length']
                chain = response.json()['chain']
                if length > max_length and  self.valid_chain(chain):
                    max_length=length
                    new_chain=chain

        if new_chain:
            self.chain = new_chain
            return True
        return False

    def get_trans(self):
        neighbours=self.nodes
        new_trans=None
        for node in neighbours:
            response = requests.get(f'http://{node}/trans')
            if response.status_code == 200:
                trans=response.json()['transaction']
                if(len(trans)>0):
                    self.transaction.append(trans)
    '''
    def send_nodes(self,nod):
        y=[]
        for x in self.nodes:
            y.append("http://"+x)
        payload={"nodes":y}
        for n in nod:
            url=n+'/nodes/register'
            headers={'content-type': 'application/json'}
            r=requests.post(url,json.dumps(payload),headers=headers)
        nop={"nodes":nod}
        for g in y:
            url=g+'/nodes/register'
            headers={'content-type': 'application/json'}
            r=requests.post(url,json.dumps(nop),headers=headers)
    '''
    def send_address(self):
        payload={"nodes":["http://127.0.0.1:5000"]}
        for n in self.nodes:
            url = 'http://'+n+'/nodes/register'
            headers = {'content-type': 'application/json'}
            r = requests.post(url, json.dumps(payload), headers=headers)

    def ob_nodes(self):
        count=0
        extra_nodes= set()
        for n in self.nodes:
            print("hello")
            response=requests.get(f'http://{n}/nodes/share')
            if response.status_code ==200:
                new_nodes = response.json()['nodes']
                if len(new_nodes) > 0:
                    count=count+1
                    for p in new_nodes:
                        if(p != self.address):
                            extra_nodes.add(p)
        if(count>0):
            for k in extra_nodes:
                self.nodes.add(k)
            return True
        else:
            return False