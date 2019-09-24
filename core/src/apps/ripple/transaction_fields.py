from apps.ripple.binary_field import field as binfield


def payment(msg):
    if not msg.payment:
        return
    return {
        "TransactionType": binfield["TRANSACTION_TYPES"]["Payment"],
        "DestinationTag": msg.payment.destination_tag,
        "LastLedgerSequence": msg.last_ledger_sequence,
        "Amount": msg.payment.amount,
        "Destination": msg.payment.destination
    }


def signer_list_set(msg):
    if not msg.signer_list_set:
        return

    field = {
        "TransactionType": binfield["TRANSACTION_TYPES"]["SignerListSet"],
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
    return field


def account_set(msg):
    if not msg.account_set:
        return

    field = {
        "TransactionType": binfield["TRANSACTION_TYPES"]["AccountSet"],
    }
    if msg.account_set.set_flag:
        field["SetFlag"] = msg.account_set.set_flag
    if msg.account_set.clear_flag:
        field["ClearFlag"] = msg.account_set.clear_flag
    # wip
    return field
