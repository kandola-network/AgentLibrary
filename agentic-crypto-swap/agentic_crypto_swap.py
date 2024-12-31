from web3 import Web3
from eth_account import Account
from decimal import Decimal
from typing import Optional
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_typing import Address

def perform_token_swap(
    web3: Web3,
    private_key: str,
    token_in_address: str,
    token_out_address: str,
    amount_in: Decimal,
    router_address: str,
    slippage_percentage: float = 0.5
) -> dict:
    """
    Perform a token swap on Uniswap V3.
    
    Args:
        web3: Web3 instance connected to the network
        private_key: Private key of the wallet (with 0x prefix)
        token_in_address: Address of token to swap from
        token_out_address: Address of token to swap to
        amount_in: Amount of input token to swap
        router_address: Uniswap V3 router address
        slippage_percentage: Maximum allowed slippage (default 0.5%)
        
    Returns:
        dict: Transaction receipt
    """
    # Setup account
    account = Account.from_key(private_key)
    web3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    
    # Load token contracts
    erc20_abi = [
        {
            "constant": False,
            "inputs": [
                {"name": "_spender", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "approve",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        }
    ]
    
    token_in = web3.eth.contract(address=Web3.to_checksum_address(token_in_address), abi=erc20_abi)
    
    # Get token decimals
    decimals = token_in.functions.decimals().call()
    
    # Convert amount to raw
    amount_raw = int(amount_in * (10 ** decimals))
    
    # Check balance
    balance = token_in.functions.balanceOf(account.address).call()
    if balance < amount_raw:
        raise ValueError(f"Insufficient balance. Have: {balance / (10 ** decimals)}, Need: {amount_in}")
    
    # Approve router
    approve_tx = token_in.functions.approve(
        Web3.to_checksum_address(router_address),
        amount_raw
    ).build_transaction({
        'from': account.address,
        'gas': 150000,
        'nonce': web3.eth.get_transaction_count(account.address),
    })
    
    # Sign and send approval
    signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
    approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
    
    # Wait for approval to complete
    approve_receipt = web3.eth.wait_for_transaction_receipt(approve_tx_hash)
    if approve_receipt['status'] != 1:
        raise Exception("Approval transaction failed")
    
    # Build swap transaction
    router_abi = [
        {
            "inputs": [
                {
                    "components": [
                        {"internalType": "address", "name": "tokenIn", "type": "address"},
                        {"internalType": "address", "name": "tokenOut", "type": "address"},
                        {"internalType": "uint24", "name": "fee", "type": "uint24"},
                        {"internalType": "address", "name": "recipient", "type": "address"},
                        {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                        {"internalType": "uint256", "name": "amountOutMinimum", "type": "uint256"},
                        {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
                    ],
                    "internalType": "struct ISwapRouter.ExactInputSingleParams",
                    "name": "params",
                    "type": "tuple"
                }
            ],
            "name": "exactInputSingle",
            "outputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"}],
            "stateMutability": "payable",
            "type": "function"
        }
    ]
    
    router = web3.eth.contract(address=Web3.to_checksum_address(router_address), abi=router_abi)
    
    # Prepare swap parameters
    params = {
        'tokenIn': Web3.to_checksum_address(token_in_address),
        'tokenOut': Web3.to_checksum_address(token_out_address),
        'fee': 3000,  # 0.3% fee tier
        'recipient': account.address,
        'amountIn': amount_raw,
        'amountOutMinimum': 0,  # In production, calculate this based on slippage
        'sqrtPriceLimitX96': 0
    }
    
    # Build swap transaction
    swap_tx = router.functions.exactInputSingle(params).build_transaction({
        'from': account.address,
        'gas': 350000,
        'nonce': web3.eth.get_transaction_count(account.address),
        'value': 0
    })
    
    # Sign and send swap
    signed_swap_tx = web3.eth.account.sign_transaction(swap_tx, private_key)
    swap_tx_hash = web3.eth.send_raw_transaction(signed_swap_tx.rawTransaction)
    
    # Wait for swap to complete
    swap_receipt = web3.eth.wait_for_transaction_receipt(swap_tx_hash)
    if swap_receipt['status'] != 1:
        raise Exception("Swap transaction failed")
    
    return swap_receipt