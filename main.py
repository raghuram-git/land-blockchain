import blockchain

chain=blockchain.blockchain()
print("Enter no of transactions")
n=int(input())
for i in range(1,n):
    print("enter sender,receiver,survey")
    p1=input()
    p2=input()
    s=input()
    chain.new_transaction(p1,p2,s)
lastproof=5
lastproof=chain.proof_of_work(lastproof)
block=chain.new_block(lastproof)
final=chain.h_ash(block)
print(final)