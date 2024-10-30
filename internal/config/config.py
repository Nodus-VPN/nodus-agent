from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    db_user = "postgres"
    db_pass = "postgres"
    db_host = "nodus-db"
    db_port = 5432
    db_name = "postgres"

    owner_address = "0xBb35CB00d1e54A98b6a44E4F42faBedD43660293"
    owner_private_key = "2dca2cd0db77495ca32f08e601457bb75fc0b8d92d6f4e654792334554d80f85"

    vpn_contract_address: str = "0x0DAbB195Fc92fAb4f413Bd1Fb885d854a5802B88"
    vpn_contract_abi: str = """[
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_nds_address",
                        "type": "address"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "owner",
                        "type": "address"
                    }
                ],
                "name": "OwnableInvalidOwner",
                "type": "error"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "account",
                        "type": "address"
                    }
                ],
                "name": "OwnableUnauthorizedAccount",
                "type": "error"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "previousOwner",
                        "type": "address"
                    },
                    {
                        "indexed": true,
                        "internalType": "address",
                        "name": "newOwner",
                        "type": "address"
                    }
                ],
                "name": "OwnershipTransferred",
                "type": "event"
            },
            {
                "anonymous": false,
                "inputs": [
                    {
                        "indexed": false,
                        "internalType": "uint256",
                        "name": "node_id",
                        "type": "uint256"
                    },
                    {
                        "indexed": false,
                        "internalType": "string",
                        "name": "node_ip",
                        "type": "string"
                    },
                    {
                        "indexed": false,
                        "internalType": "address",
                        "name": "node_owner",
                        "type": "address"
                    }
                ],
                "name": "SetNode",
                "type": "event"
            },
            {
                "inputs": [],
                "name": "NDS",
                "outputs": [
                    {
                        "internalType": "contract IERC20",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "name": "allNode",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "nodeIP",
                        "type": "string"
                    }
                ],
                "name": "calculateNodeScore",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "calculateReward",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "name": "clients",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "hashedKey",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "subscriptionExpirationDate",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getAllClientAddress",
                "outputs": [
                    {
                        "internalType": "address[]",
                        "name": "",
                        "type": "address[]"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getAllNode",
                "outputs": [
                    {
                        "internalType": "string[]",
                        "name": "",
                        "type": "string[]"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_clientAddress",
                        "type": "address"
                    }
                ],
                "name": "getClient",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "string",
                                "name": "hashedKey",
                                "type": "string"
                            },
                            {
                                "internalType": "uint256",
                                "name": "subscriptionExpirationDate",
                                "type": "uint256"
                            }
                        ],
                        "internalType": "struct NodusVPN.Client",
                        "name": "",
                        "type": "tuple"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getClientBalance",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "_nodeIP",
                        "type": "string"
                    }
                ],
                "name": "getNodeMetrics",
                "outputs": [
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "okResponse",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "failedResponse",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "wgDownloadSpeedRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "wgUploadSpeedRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "wgPackageLossRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "wgPingRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "wgDownloadSpeedTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "wgUploadSpeedTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "wgPackageLossTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "wgPingTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256",
                                "name": "ovpnDownloadSpeedRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "ovpnUploadSpeedRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "ovpnPackageLossRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "ovpnPingRN",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "ovpnDownloadSpeedTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "ovpnUploadSpeedTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "ovpnPackageLossTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256[]",
                                "name": "ovpnPingTS",
                                "type": "uint256[]"
                            },
                            {
                                "internalType": "uint256",
                                "name": "reward",
                                "type": "uint256"
                            }
                        ],
                        "internalType": "struct NodusVPN.Node",
                        "name": "",
                        "type": "tuple"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "name": "nodeMetrics",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "okResponse",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "failedResponse",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "wgDownloadSpeedRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "wgUploadSpeedRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "wgPackageLossRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "wgPingRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "ovpnDownloadSpeedRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "ovpnUploadSpeedRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "ovpnPackageLossRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "ovpnPingRN",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "reward",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "name": "nodeOwners",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "owner",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "renounceOwnership",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "_nodeIP",
                        "type": "string"
                    }
                ],
                "name": "setNodeIP",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_subscriptionDuration",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "_hashedKey",
                        "type": "string"
                    }
                ],
                "name": "subscribe",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "subscriptionMounthPrice",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "newOwner",
                        "type": "address"
                    }
                ],
                "name": "transferOwnership",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string[]",
                        "name": "_nodeIP",
                        "type": "string[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_ovpnDownloadSpeed",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_ovpnUploadSpeed",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_ovpnPackageLoss",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_ovpnPing",
                        "type": "uint256[]"
                    }
                ],
                "name": "updateNodeOvpnMetrics",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string[]",
                        "name": "_nodeIP",
                        "type": "string[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_okResponse",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_failedResponse",
                        "type": "uint256[]"
                    }
                ],
                "name": "updateNodeUptime",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "string[]",
                        "name": "_nodeIP",
                        "type": "string[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_wgDownloadSpeed",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_wgUploadSpeed",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_wgPackageLoss",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "_wgPing",
                        "type": "uint256[]"
                    }
                ],
                "name": "updateNodeWgMetrics",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]"""

    nds_contract_address: str = "0xF0314d84BBca78524d4F555441911211E4420e2e"
    nds_contract_abi = """[
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "value",
                    "type": "uint256"
                }
            ],
            "name": "approve",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "allowance",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "needed",
                    "type": "uint256"
                }
            ],
            "name": "ERC20InsufficientAllowance",
            "type": "error"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "sender",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "balance",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "needed",
                    "type": "uint256"
                }
            ],
            "name": "ERC20InsufficientBalance",
            "type": "error"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "approver",
                    "type": "address"
                }
            ],
            "name": "ERC20InvalidApprover",
            "type": "error"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "receiver",
                    "type": "address"
                }
            ],
            "name": "ERC20InvalidReceiver",
            "type": "error"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "sender",
                    "type": "address"
                }
            ],
            "name": "ERC20InvalidSender",
            "type": "error"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address"
                }
            ],
            "name": "ERC20InvalidSpender",
            "type": "error"
        },
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "owner",
                    "type": "address"
                },
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "spender",
                    "type": "address"
                },
                {
                    "indexed": false,
                    "internalType": "uint256",
                    "name": "value",
                    "type": "uint256"
                }
            ],
            "name": "Approval",
            "type": "event"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "to",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "value",
                    "type": "uint256"
                }
            ],
            "name": "transfer",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "from",
                    "type": "address"
                },
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "to",
                    "type": "address"
                },
                {
                    "indexed": false,
                    "internalType": "uint256",
                    "name": "value",
                    "type": "uint256"
                }
            ],
            "name": "Transfer",
            "type": "event"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "from",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "to",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "value",
                    "type": "uint256"
                }
            ],
            "name": "transferFrom",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "owner",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "spender",
                    "type": "address"
                }
            ],
            "name": "allowance",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "account",
                    "type": "address"
                }
            ],
            "name": "balanceOf",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "decimals",
            "outputs": [
                {
                    "internalType": "uint8",
                    "name": "",
                    "type": "uint8"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "symbol",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "totalSupply",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]"""

    node_metric_port = 7001
    admin_address: str = "0xBb35CB00d1e54A98b6a44E4F42faBedD43660293"
