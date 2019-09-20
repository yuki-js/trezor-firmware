from apps.ripple.binary_field import field as binfield
import apps.ripple.layout


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
