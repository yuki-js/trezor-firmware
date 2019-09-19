# Serializes into the Ripple Format
#
# Inspired by https://github.com/miracle2k/ripple-python and https://github.com/ripple/ripple-lib
# Docs at https://wiki.ripple.com/Binary_Format and https://developers.ripple.com/transaction-common-fields.html
#
# The first four bits specify the field type (int16, int32, account..)
# the other four the record type (amount, fee, destination..) and then
# the actual data follow. This currently only supports the Payment
# transaction type and the fields that are required for it.

from trezor.messages.RippleSignTx import RippleSignTx

from . import helpers

from .binary_field import field as binfield
from trezor import log


def serialize(msg: RippleSignTx,
              fields: dict,
              multisig: bool,
              pubkey=None,
              signature=None) -> bytearray:

    if multisig:
        None
    else:
        if signature:
            fields["TxnSignature"] = signature
        if pubkey:
            fields["SigningPubKey"] = pubkey
    # must be sorted numerically first by type and then by name
    return serialize_raw(fields)


def serialize_raw(fields: dict) -> bytearray:
    w = bytearray()
    farr = list(fields.keys())
    n = len(fields)
    for i in range(0, n):
        for j in range(n - 1, i, -1):
            if farr[j - 1] == "Invalid" or binfield["FIELDS"][farr[j]][
                    "type"] < binfield["FIELDS"][farr[j - 1]]["type"] or (
                        binfield["FIELDS"][farr[j]]["type"] ==
                        binfield["FIELDS"][farr[j - 1]]["type"]
                        and binfield["FIELDS"][farr[j]]["nth"] <
                        binfield["FIELDS"][farr[j - 1]]["nth"]):
                farr[j - 1], farr[j] = farr[j], farr[j - 1]

    for k in farr:
        log.debug("ripple", k)
        write(w, binfield["FIELDS"][k], fields[k])
    return w


def write(w: bytearray, field: dict, value):
    if value is None:
        return
    write_type(w, field)
    if field["type"] == binfield["TYPES"]["UInt16"]:
        w.extend(value.to_bytes(2, "big"))
    elif field["type"] == binfield["TYPES"]["UInt32"]:
        w.extend(value.to_bytes(4, "big"))
    elif field["type"] == binfield["TYPES"]["Amount"]:
        w.extend(serialize_amount(value))
    elif field["type"] == binfield["TYPES"]["AccountID"]:
        write_bytes(w, helpers.decode_address(value))
    elif field["type"] == binfield["TYPES"]["Blob"]:
        write_bytes(w, value)
    elif field["type"] == binfield["TYPES"]["STArray"]:
        None
    elif field["type"] == binfield["TYPES"]["STObject"]:
        w.extend(serialize_raw(value) +
                 b'\xe1')  # STObject end with 0xe1(ObjectEndMarker)
    else:
        raise ValueError("Unknown field type")


def write_type(w: bytearray, field: dict):
    fcode = field["nth"]
    ftype = field["type"]

    if ftype < 16 and fcode < 16:
        w.append((ftype << 4) | fcode)
    elif ftype >= 16 and fcode < 16:
        w.append(fcode)
        w.append(ftype)
    elif ftype < 16 and fcode >= 16:
        w.append(ftype << 4)
        w.append(fcode)
    else:
        w.append(0)
        w.append(fcode)
        w.append(ftype)


def serialize_amount(value: int) -> bytearray:
    if value < 0:
        raise ValueError("Only non-negative integers are supported")
    if value > helpers.MAX_ALLOWED_AMOUNT:
        raise ValueError("Value is too large")

    b = bytearray(value.to_bytes(8, "big"))
    b[0] &= 0x7F  # clear first bit to indicate XRP
    b[0] |= 0x40  # set second bit to indicate positive number
    return b


def write_bytes(w: bytearray, value: bytes):
    """Serialize a variable length bytes."""
    write_varint(w, len(value))
    w.extend(value)


def write_varint(w: bytearray, val: int):
    """
    Implements variable-length int encoding from Ripple.
    See: https://ripple.com/wiki/Binary_Format#Variable_Length_Data_Encoding
    """
    if val < 0:
        raise ValueError("Only non-negative integers are supported")
    elif val < 192:
        w.append(val)
    elif val <= 12480:
        val -= 193
        w.append(193 + rshift(val, 8))
        w.append(val & 0xFF)
    elif val <= 918744:
        val -= 12481
        w.append(241 + rshift(val, 16))
        w.append(rshift(val, 8) & 0xFF)
        w.append(val & 0xFF)
    else:
        raise ValueError("Value is too large")


def rshift(val, n):
    """
    Implements signed right-shift.
    See: http://stackoverflow.com/a/5833119/15677
    """
    return (val % 0x100000000) >> n
