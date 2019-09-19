field = {
    "TYPES": {
        "Validation": 10003,
        "Done": -1,
        "Hash128": 4,
        "Blob": 7,
        "AccountID": 8,
        "Amount": 6,
        "Hash256": 5,
        "UInt8": 16,
        "Vector256": 19,
        "STObject": 14,
        "Unknown": -2,
        "Transaction": 10001,
        "Hash160": 17,
        "PathSet": 18,
        "LedgerEntry": 10002,
        "UInt16": 1,
        "NotPresent": 0,
        "UInt64": 3,
        "UInt32": 2,
        "STArray": 15
    },
    "LEDGER_ENTRY_TYPES": {
        "Any": -3,
        "Child": -2,
        "Invalid": -1,
        "AccountRoot": 97,
        "DirectoryNode": 100,
        "RippleState": 114,
        "Ticket": 84,
        "SignerList": 83,
        "Offer": 111,
        "LedgerHashes": 104,
        "Amendments": 102,
        "FeeSettings": 115,
        "Escrow": 117,
        "PayChannel": 120,
        "DepositPreauth": 112,
        "Check": 67,
        "Nickname": 110,
        "Contract": 99,
        "GeneratorMap": 103
    },
    "FIELDS": {
        "Generic": {
            "nth": 0,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": -2
        },
        "Invalid": {
            "nth": -1,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": -2
        },
        "LedgerEntryType": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 1
        },
        "TransactionType": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 1
        },
        "SignerWeight": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 1
        },
        "Flags": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "SourceTag": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "Sequence": {
            "nth": 4,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "PreviousTxnLgrSeq": {
            "nth": 5,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "LedgerSequence": {
            "nth": 6,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "CloseTime": {
            "nth": 7,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "ParentCloseTime": {
            "nth": 8,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "SigningTime": {
            "nth": 9,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "Expiration": {
            "nth": 10,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "TransferRate": {
            "nth": 11,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "WalletSize": {
            "nth": 12,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "OwnerCount": {
            "nth": 13,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "DestinationTag": {
            "nth": 14,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "HighQualityIn": {
            "nth": 16,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "HighQualityOut": {
            "nth": 17,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "LowQualityIn": {
            "nth": 18,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "LowQualityOut": {
            "nth": 19,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "QualityIn": {
            "nth": 20,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "QualityOut": {
            "nth": 21,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "StampEscrow": {
            "nth": 22,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "BondAmount": {
            "nth": 23,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "LoadFee": {
            "nth": 24,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "OfferSequence": {
            "nth": 25,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "FirstLedgerSequence": {
            "nth": 26,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "LastLedgerSequence": {
            "nth": 27,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "TransactionIndex": {
            "nth": 28,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "OperationLimit": {
            "nth": 29,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "ReferenceFeeUnits": {
            "nth": 30,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "ReserveBase": {
            "nth": 31,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "ReserveIncrement": {
            "nth": 32,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "SetFlag": {
            "nth": 33,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "ClearFlag": {
            "nth": 34,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "SignerQuorum": {
            "nth": 35,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "CancelAfter": {
            "nth": 36,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "FinishAfter": {
            "nth": 37,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "IndexNext": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "IndexPrevious": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "BookNode": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "OwnerNode": {
            "nth": 4,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "BaseFee": {
            "nth": 5,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "ExchangeRate": {
            "nth": 6,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "LowNode": {
            "nth": 7,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "HighNode": {
            "nth": 8,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        },
        "EmailHash": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 4
        },
        "LedgerHash": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "ParentHash": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "TransactionHash": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "AccountHash": {
            "nth": 4,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "PreviousTxnID": {
            "nth": 5,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "LedgerIndex": {
            "nth": 6,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "WalletLocator": {
            "nth": 7,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "RootIndex": {
            "nth": 8,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "AccountTxnID": {
            "nth": 9,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "BookDirectory": {
            "nth": 16,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "InvoiceID": {
            "nth": 17,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "Nickname": {
            "nth": 18,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "Amendment": {
            "nth": 19,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "TicketID": {
            "nth": 20,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "Digest": {
            "nth": 21,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "hash": {
            "nth": 257,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": 5
        },
        "index": {
            "nth": 258,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": 5
        },
        "Amount": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "Balance": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "LimitAmount": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "TakerPays": {
            "nth": 4,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "TakerGets": {
            "nth": 5,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "LowLimit": {
            "nth": 6,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "HighLimit": {
            "nth": 7,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "Fee": {
            "nth": 8,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "SendMax": {
            "nth": 9,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "DeliverMin": {
            "nth": 10,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "MinimumOffer": {
            "nth": 16,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "RippleEscrow": {
            "nth": 17,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "DeliveredAmount": {
            "nth": 18,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 6
        },
        "taker_gets_funded": {
            "nth": 258,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": 6
        },
        "taker_pays_funded": {
            "nth": 259,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": 6
        },
        "PublicKey": {
            "nth": 1,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "MessageKey": {
            "nth": 2,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "SigningPubKey": {
            "nth": 3,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "TxnSignature": {
            "nth": 4,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": False,
            "type": 7
        },
        "Generator": {
            "nth": 5,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "Signature": {
            "nth": 6,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": False,
            "type": 7
        },
        "Domain": {
            "nth": 7,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "FundCode": {
            "nth": 8,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "RemoveCode": {
            "nth": 9,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "ExpireCode": {
            "nth": 10,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "CreateCode": {
            "nth": 11,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "MemoType": {
            "nth": 12,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "MemoData": {
            "nth": 13,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "MemoFormat": {
            "nth": 14,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "Fulfillment": {
            "nth": 16,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "Condition": {
            "nth": 17,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 7
        },
        "MasterSignature": {
            "nth": 18,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": False,
            "type": 7
        },
        "Account": {
            "nth": 1,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "Owner": {
            "nth": 2,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "Destination": {
            "nth": 3,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "Issuer": {
            "nth": 4,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "Authorize": {
            "nth": 5,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "Unauthorize": {
            "nth": 6,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "Target": {
            "nth": 7,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "RegularKey": {
            "nth": 8,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 8
        },
        "ObjectEndMarker": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "TransactionMetaData": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "CreatedNode": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "DeletedNode": {
            "nth": 4,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "ModifiedNode": {
            "nth": 5,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "PreviousFields": {
            "nth": 6,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "FinalFields": {
            "nth": 7,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "NewFields": {
            "nth": 8,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "TemplateEntry": {
            "nth": 9,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "Memo": {
            "nth": 10,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "SignerEntry": {
            "nth": 11,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "Signer": {
            "nth": 16,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "Majority": {
            "nth": 18,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 14
        },
        "ArrayEndMarker": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "Signers": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": False,
            "type": 15
        },
        "SignerEntries": {
            "nth": 4,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "Template": {
            "nth": 5,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "Necessary": {
            "nth": 6,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "Sufficient": {
            "nth": 7,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "AffectedNodes": {
            "nth": 8,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "Memos": {
            "nth": 9,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "Majorities": {
            "nth": 16,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 15
        },
        "CloseResolution": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 16
        },
        "Method": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 16
        },
        "TransactionResult": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 16
        },
        "TakerPaysCurrency": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 17
        },
        "TakerPaysIssuer": {
            "nth": 2,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 17
        },
        "TakerGetsCurrency": {
            "nth": 3,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 17
        },
        "TakerGetsIssuer": {
            "nth": 4,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 17
        },
        "Paths": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 18
        },
        "Indexes": {
            "nth": 1,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 19
        },
        "Hashes": {
            "nth": 2,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 19
        },
        "Amendments": {
            "nth": 3,
            "isVLEncoded": True,
            "isSerialized": True,
            "isSigningField": True,
            "type": 19
        },
        "Transaction": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": 10001
        },
        "LedgerEntry": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": 10002
        },
        "Validation": {
            "nth": 1,
            "isVLEncoded": False,
            "isSerialized": False,
            "isSigningField": False,
            "type": 10003
        },
        "SignerListID": {
            "nth": 38,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "SettleDelay": {
            "nth": 39,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 2
        },
        "Channel": {
            "nth": 22,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "ConsensusHash": {
            "nth": 23,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "CheckID": {
            "nth": 24,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 5
        },
        "TickSize": {
            "nth": 16,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 16
        },
        "DestinationNode": {
            "nth": 9,
            "isVLEncoded": False,
            "isSerialized": True,
            "isSigningField": True,
            "type": 3
        }
    },
    "TRANSACTION_TYPES": {
        "Invalid": -1,
        "Payment": 0,
        "EscrowCreate": 1,
        "EscrowFinish": 2,
        "AccountSet": 3,
        "EscrowCancel": 4,
        "SetRegularKey": 5,
        "NickNameSet": 6,
        "OfferCreate": 7,
        "OfferCancel": 8,
        "Contract": 9,
        "TicketCreate": 10,
        "TicketCancel": 11,
        "SignerListSet": 12,
        "PaymentChannelCreate": 13,
        "PaymentChannelFund": 14,
        "PaymentChannelClaim": 15,
        "CheckCreate": 16,
        "CheckCash": 17,
        "CheckCancel": 18,
        "DepositPreauth": 19,
        "TrustSet": 20,
        "EnableAmendment": 100,
        "SetFee": 101
    }
}
