from apps.ripple.binary_field import field as binfield


def payment(msg):
    if not msg.payment:
        return
    field = {
        "TransactionType": "Payment",
        "DestinationTag": msg.payment.destination_tag,
        "LastLedgerSequence": msg.last_ledger_sequence,
        "Destination": msg.payment.destination,
    }
    if msg.payment.amount:
        field["Amount"] = msg.payment.amount
    elif msg.payment.issued_amount:
        field["Amount"] = {
            "currency": msg.issued_amount.currency,
            "value": msg.issued_amount.value,
            "issuer": msg.issued_amount.issuer
        }
    else:
        return
    return field


def signer_list_set(msg):
    if not msg.signer_list_set:
        return

    field = {
        "TransactionType": "SignerListSet",
        "SignerQuorum": msg.signer_list_set.signer_quorum,
    }
    entries = []
    for signerEntry in msg.signer_list_set.signer_entries:
        entries.append({
            "SignerEntry": {
                "Account": signerEntry.account,
                "SignerWeight": signerEntry.signer_weight,
            }
        })
    field["SignerEntries"] = entries
    return field


def account_set(msg):
    if not msg.account_set:
        return

    field = {
        "TransactionType": "AccountSet",
        "SetFlag": msg.account_set.set_flag,
        "ClearFlag": msg.account_set.clear_flag,
        "TransferRate": msg.account_set.transfer_rate,
        "TickSize": msg.account_set.tick_size,
        "Domain": msg.account_set.domain,
        "EmailHash": msg.account_set.email_hash
    }
    return field
