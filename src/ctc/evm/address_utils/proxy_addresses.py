from .. import rpc_utils


eip_897_abi = [
    {
        'name': 'proxyType',
        'type': 'function',
        'inputs': [],
        'outputs': [
            {'name': 'proxyTypeId', 'type': 'uint256'},
        ],
    },
    {
        'name': 'implementation',
        'type': 'function',
        'inputs': [],
        'outputs': [
            {'name': 'codeAddr', 'type': 'address'},
        ],
    },
]


def get_eip897_proxy_type(contract_address):

    function_abi = eip_897_abi[0]
    assert function_abi['name'] == 'proxyType'

    return rpc_utils.eth_call(
        to_address=contract_address,
        function_abi=function_abi,
    )


def get_eip897_implementation(contract_address):

    function_abi = eip_897_abi[1]
    assert function_abi['name'] == 'implementation'

    return rpc_utils.eth_call(
        to_address=contract_address,
        function_abi=function_abi,
    )


def get_eip1967_proxy_logic_address(contract_address, block=None):
    """get a contract's logic address

    storage position obtained as:
        bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1)

    see https://eips.ethereum.org/EIPS/eip-1967
    """

    position = (
        '0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'
    )

    result = rpc_utils.eth_get_storage_at(
        address=contract_address,
        position=position,
        block_number=block,
    )

    return '0x' + result[-40:]


def get_eip1967_proxy_beacon_address(contract_address, block=None):
    """get a contract's logic address

    storage position obtained as:
        bytes32(uint256(keccak256('eip1967.proxy.beacon')) - 1)

    see https://eips.ethereum.org/EIPS/eip-1967
    """

    position = (
        '0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50'
    )

    result = rpc_utils.eth_get_storage_at(
        address=contract_address,
        position=position,
        block_number=block,
    )

    return '0x' + result[-40:]


def get_eip1967_proxy_admin_address(contract_address, block=None):
    """get a contract's logic address

    storage position obtained as:
        bytes32(uint256(keccak256('eip1967.proxy.admin')) - 1)

    see https://eips.ethereum.org/EIPS/eip-1967
    """

    position = (
        '0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50'
    )

    result = rpc_utils.eth_get_storage_at(
        address=contract_address,
        position=position,
        block_number=block,
    )

    return '0x' + result[-40:]
