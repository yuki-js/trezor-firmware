from apps.ripple.binary_field import field as binfield


def payment(msg, source_address):
    return {
        "TransactionType": binfield["TRANSACTION_TYPES"]["Payment"],
        "Flags": msg.flags,
        "Sequence": msg.sequence,
        "DestinationTag": msg.payment.destination_tag,
        "LastLedgerSequence": msg.last_ledger_sequence,
        "Amount": msg.payment.amount,
        "Fee": msg.fee,
        "Account": source_address,
        "Destination": msg.payment.destination
    }


def signerListSet(msg, source_address):
    field = {
        "Flags": msg.flags,
        "TransactionType": binfield["TRANSACTION_TYPES"]["SignerListSet"],
        "Account": source_address,
        "Fee": msg.fee,
        "SignerQuorum": msg.signer_list_set.signer_quorum
    }
    entries = []
    for signerEntry in msg.signer_list_set.signer_entries:
        entries.append({
            "SignerEntry": {
                "Account": signerEntry.account,
                "SignerWeight": signerEntry.signer_weight
            }
        })
    field["SignerEntries"] = entries
