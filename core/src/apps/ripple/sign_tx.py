from trezor.crypto import der
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha512
from trezor.messages.RippleSignedTx import RippleSignedTx
from trezor.messages.RippleSignTx import RippleSignTx
from trezor.wire import ProcessError

from apps.common import paths
from apps.ripple import CURVE, helpers, layout
from apps.ripple.serialize import serialize

from .binary_field import field as binfield


async def sign_tx(ctx, msg: RippleSignTx, keychain):
    validate(msg)

    await paths.validate_path(ctx, helpers.validate_full_path, keychain,
                              msg.address_n, CURVE)

    node = keychain.derive(msg.address_n)
    source_address = helpers.address_from_public_key(node.public_key())

    fields = {
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

    set_canonical_flag(msg)
    tx = serialize(msg, fields, False, pubkey=node.public_key())
    to_sign = get_network_prefix() + tx

    check_fee(msg.fee)
    if msg.payment.destination_tag is not None:
        await layout.require_confirm_destination_tag(
            ctx, msg.payment.destination_tag)
    await layout.require_confirm_fee(ctx, msg.fee)
    await layout.require_confirm_tx(ctx, msg.payment.destination,
                                    msg.payment.amount)

    signature = ecdsa_sign(node.private_key(), first_half_of_sha512(to_sign))
    tx = serialize(msg,
                   fields,
                   False,
                   pubkey=node.public_key(),
                   signature=signature)
    return RippleSignedTx(signature, tx)


def check_fee(fee: int):
    if fee < helpers.MIN_FEE or fee > helpers.MAX_FEE:
        raise ProcessError("Fee must be in the range of 10 to 10,000 drops")


def get_network_prefix():
    """Network prefix is prepended before the transaction and public key is included"""
    return helpers.HASH_TX_SIGN.to_bytes(4, "big")


def first_half_of_sha512(b):
    """First half of SHA512, which Ripple uses"""
    hash = sha512(b)
    return hash.digest()[:32]


def ecdsa_sign(private_key: bytes, digest: bytes) -> bytes:
    """Signs and encodes signature into DER format"""
    signature = secp256k1.sign(private_key, digest)
    sig_der = der.encode_seq((signature[1:33], signature[33:65]))
    return sig_der


def set_canonical_flag(msg: RippleSignTx):
    """
    Our ECDSA implementation already returns fully-canonical signatures,
    so we're enforcing it in the transaction using the designated flag
    - see https://wiki.ripple.com/Transaction_Malleability#Using_Fully-Canonical_Signatures
    - see https://github.com/trezor/trezor-crypto/blob/3e8974ff8871263a70b7fbb9a27a1da5b0d810f7/ecdsa.c#L791
    """
    if msg.flags is None:
        msg.flags = 0
    msg.flags |= helpers.FLAG_FULLY_CANONICAL


def validate(msg: RippleSignTx):
    if None in (msg.fee, msg.sequence, msg.payment) or (
            msg.payment
            and None in (msg.payment.amount, msg.payment.destination)):
        raise ProcessError(
            "Some of the required fields are missing (fee, sequence, payment.amount, payment.destination)"
        )
