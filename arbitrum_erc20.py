import time
from web3 import Web3

ARBITRUM_RPC_URL = 'https://arbitrum.llamarpc.com'
web3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC_URL))

ERC20_ABI = [{
    "constant": True,
    "inputs": [],
    "name": "name",
    "outputs": [{"name": "", "type": "string"}],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
}]

def is_erc20_contract(address):
    contract = web3.eth.contract(address=address, abi=ERC20_ABI)
    try:
        return contract.functions.name().call() is not None
    except:
        return False

def main():
    last_checked_block = web3.eth.get_block('latest')['number']

    while True:
        current_block = web3.eth.get_block(last_checked_block)
        transactions = current_block['transactions']

        print(f"Checking block {current_block['number']} with {len(transactions)} transactions...")

        found_erc20 = False
        for tx_hash in transactions:
            tx = web3.eth.get_transaction(tx_hash)
            if tx['to'] is None:  # Possible contract creation
                receipt = web3.eth.get_transaction_receipt(tx_hash)
                contract_address = receipt['contractAddress']
                if is_erc20_contract(contract_address):
                    print(f"ERC-20 Token Contract deployed at {contract_address}")
                    found_erc20 = True

        if not found_erc20:
            print("No ERC-20 contracts found in this block.")

        last_checked_block += 1  # Move to the next block
        time.sleep(3)  # Wait for 3 seconds before checking the next block

if __name__ == '__main__':
    main()
