from uuid import uuid4
from flask import Flask, jsonify, request
import blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-',' ')

@app.route('/transaction/new',methods=['POST'])
def new_transaction():

    values=request.get_json()
    required=['party1','party2','surveyno']
    if not all(k in values for k in required):
        return "missing data",400

    index = mchain.new_transaction(values['party1'],values['party2'],values['surveyno'])
    response={'message': f'transaction will be added to block {index}'}
    return jsonify(response),201

@app.route('/trans',methods=['GET'])
def get_trans():
    response={
        'transaction':mchain.transaction
    }
    return jsonify(response),200

@app.route('/mine',methods=['GET'])
def mine():
    mchain.get_trans()
    last_block=mchain.last_block()
    last_proof=last_block['proof']
    proof=mchain.proof_of_work(last_proof)
    previous_hash = mchain.h_ash(last_block)
    block = mchain.new_block(proof,previous_hash)
    response = {
        'message':"new block created",
        'index':block['index'],
        'transactions':block['transaction'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash'],
    }
    return jsonify(response),200

@app.route('/chain',methods=['GET'])
def full_chain():
    response={
        'chain':mchain.chain,
        'length':len(mchain.chain),
    }
    return jsonify(response),200

@app.route('/nodes/get',methods=['GET'])
def get_chain():
    response={
        "nodes":list(mchain.nodes)
    }
    return jsonify(response),200

@app.route('/nodes/register',methods=['POST'])
def register_nodes():
    values=request.get_json()
    nodes=values.get('nodes')
    if nodes == None:
        return 'error give correct node' , 400
    for node in nodes:
         mchain.register_node(node)
    response = {
        'message':'new nodes added',
        'total_nodes':list(mchain.nodes)
    }
    return jsonify(response),201

@app.route('/node/send',methods=['GET'])
def send():
    mchain.send_address()
    response={
        'message':'node shared'
    }
    return jsonify(response),201

@app.route('/nodes/conensus',methods=['GET'])
def consensus():
    replaced=mchain.resolve_conflict()
    if replaced:
        response ={
            'message':'chain is replaced',
            'newchaain': mchain.chain
        }
    else:
        response ={
            'message':'chain not replaced',
            'chain':mchain.chain
        }
    return jsonify(response),200

@app.route('/nodes/share',methods=['GET'])
def send_nodes():
    print("hello")
    response={
        'nodes': list(mchain.nodes)
    }
    return jsonify(response),200

@app.route('/nodes/obtain',methods=['GET'])
def obtain():
    obt=mchain.ob_nodes()
    if obt:
        response={
            'message':'new nodes obtained',
            'total nodes': list(mchain.nodes)
        }
    else:
        response = {
            'message': 'new nodes not obtained',
            'total nodes': list(mchain.nodes)
        }
    return jsonify(response),201

if __name__=='__main__':
    hos='127.0.0.1'
    port='5003'
    p=int(port)
    addr=hos+":"+port
    mchain = blockchain.blockchain(addr)
    app.run(host=hos,port=p)



