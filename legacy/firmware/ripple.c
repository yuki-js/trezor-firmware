/*
 * This file is part of the Trezor project, https://trezor.io/
 *
 * Copyright (C) 2017 Saleem Rashid <trezor@saleemrashid.com>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include "base58_ripple.h"
#include "bip32.h"
#include "bitmaps.h"
#include "ecdsa.h"
#include "fsm.h"
#include "gettext.h"
#include "layout.h"
#include "layout2.h"
#include "messages-ripple.pb.h"
#include "messages.pb.h"
#include "protect.h"
#include "ripple.h"
#include "sha2.h"
#include "util.h"

struct RippleField rippleFields[] = {
    {"Generic", 0, false, false, false, RippleType_Unknown},
    {"Invalid", -1, false, false, false, RippleType_Unknown},
    {"LedgerEntryType", 1, false, true, true, RippleType_UInt16},
    {"TransactionType", 2, false, true, true, RippleType_UInt16},
    {"SignerWeight", 3, false, true, true, RippleType_UInt16},
    {"Flags", 2, false, true, true, RippleType_UInt32},
    {"SourceTag", 3, false, true, true, RippleType_UInt32},
    {"Sequence", 4, false, true, true, RippleType_UInt32},
    {"PreviousTxnLgrSeq", 5, false, true, true, RippleType_UInt32},
    {"LedgerSequence", 6, false, true, true, RippleType_UInt32},
    {"CloseTime", 7, false, true, true, RippleType_UInt32},
    {"ParentCloseTime", 8, false, true, true, RippleType_UInt32},
    {"SigningTime", 9, false, true, true, RippleType_UInt32},
    {"Expiration", 10, false, true, true, RippleType_UInt32},
    {"TransferRate", 11, false, true, true, RippleType_UInt32},
    {"WalletSize", 12, false, true, true, RippleType_UInt32},
    {"OwnerCount", 13, false, true, true, RippleType_UInt32},
    {"DestinationTag", 14, false, true, true, RippleType_UInt32},
    {"HighQualityIn", 16, false, true, true, RippleType_UInt32},
    {"HighQualityOut", 17, false, true, true, RippleType_UInt32},
    {"LowQualityIn", 18, false, true, true, RippleType_UInt32},
    {"LowQualityOut", 19, false, true, true, RippleType_UInt32},
    {"QualityIn", 20, false, true, true, RippleType_UInt32},
    {"QualityOut", 21, false, true, true, RippleType_UInt32},
    {"StampEscrow", 22, false, true, true, RippleType_UInt32},
    {"BondAmount", 23, false, true, true, RippleType_UInt32},
    {"LoadFee", 24, false, true, true, RippleType_UInt32},
    {"OfferSequence", 25, false, true, true, RippleType_UInt32},
    {"FirstLedgerSequence", 26, false, true, true, RippleType_UInt32},
    {"LastLedgerSequence", 27, false, true, true, RippleType_UInt32},
    {"TransactionIndex", 28, false, true, true, RippleType_UInt32},
    {"OperationLimit", 29, false, true, true, RippleType_UInt32},
    {"ReferenceFeeUnits", 30, false, true, true, RippleType_UInt32},
    {"ReserveBase", 31, false, true, true, RippleType_UInt32},
    {"ReserveIncrement", 32, false, true, true, RippleType_UInt32},
    {"SetFlag", 33, false, true, true, RippleType_UInt32},
    {"ClearFlag", 34, false, true, true, RippleType_UInt32},
    {"SignerQuorum", 35, false, true, true, RippleType_UInt32},
    {"CancelAfter", 36, false, true, true, RippleType_UInt32},
    {"FinishAfter", 37, false, true, true, RippleType_UInt32},
    {"IndexNext", 1, false, true, true, RippleType_UInt64},
    {"IndexPrevious", 2, false, true, true, RippleType_UInt64},
    {"BookNode", 3, false, true, true, RippleType_UInt64},
    {"OwnerNode", 4, false, true, true, RippleType_UInt64},
    {"BaseFee", 5, false, true, true, RippleType_UInt64},
    {"ExchangeRate", 6, false, true, true, RippleType_UInt64},
    {"LowNode", 7, false, true, true, RippleType_UInt64},
    {"HighNode", 8, false, true, true, RippleType_UInt64},
    {"EmailHash", 1, false, true, true, RippleType_Hash128},
    {"LedgerHash", 1, false, true, true, RippleType_Hash256},
    {"ParentHash", 2, false, true, true, RippleType_Hash256},
    {"TransactionHash", 3, false, true, true, RippleType_Hash256},
    {"AccountHash", 4, false, true, true, RippleType_Hash256},
    {"PreviousTxnID", 5, false, true, true, RippleType_Hash256},
    {"LedgerIndex", 6, false, true, true, RippleType_Hash256},
    {"WalletLocator", 7, false, true, true, RippleType_Hash256},
    {"RootIndex", 8, false, true, true, RippleType_Hash256},
    {"AccountTxnID", 9, false, true, true, RippleType_Hash256},
    {"BookDirectory", 16, false, true, true, RippleType_Hash256},
    {"InvoiceID", 17, false, true, true, RippleType_Hash256},
    {"Nickname", 18, false, true, true, RippleType_Hash256},
    {"Amendment", 19, false, true, true, RippleType_Hash256},
    {"TicketID", 20, false, true, true, RippleType_Hash256},
    {"Digest", 21, false, true, true, RippleType_Hash256},
    {"hash", 1, false, false, false, RippleType_Hash256},   // overflown
    {"index", 2, false, false, false, RippleType_Hash256},  // overflown
    {"Amount", 1, false, true, true, RippleType_Amount},
    {"Balance", 2, false, true, true, RippleType_Amount},
    {"LimitAmount", 3, false, true, true, RippleType_Amount},
    {"TakerPays", 4, false, true, true, RippleType_Amount},
    {"TakerGets", 5, false, true, true, RippleType_Amount},
    {"LowLimit", 6, false, true, true, RippleType_Amount},
    {"HighLimit", 7, false, true, true, RippleType_Amount},
    {"Fee", 8, false, true, true, RippleType_Amount},
    {"SendMax", 9, false, true, true, RippleType_Amount},
    {"DeliverMin", 10, false, true, true, RippleType_Amount},
    {"MinimumOffer", 16, false, true, true, RippleType_Amount},
    {"RippleEscrow", 17, false, true, true, RippleType_Amount},
    {"DeliveredAmount", 18, false, true, true, RippleType_Amount},
    {"taker_gets_funded", 2, false, false, false,
     RippleType_Amount},  // what is it? overflown
    {"taker_pays_funded", 3, false, false, false,
     RippleType_Amount},  // what is it? overflown
    {"PublicKey", 1, true, true, true, RippleType_Blob},
    {"MessageKey", 2, true, true, true, RippleType_Blob},
    {"SigningPubKey", 3, true, true, true, RippleType_Blob},
    {"TxnSignature", 4, true, true, false, RippleType_Blob},
    {"Generator", 5, true, true, true, RippleType_Blob},
    {"Signature", 6, true, true, false, RippleType_Blob},
    {"Domain", 7, true, true, true, RippleType_Blob},
    {"FundCode", 8, true, true, true, RippleType_Blob},
    {"RemoveCode", 9, true, true, true, RippleType_Blob},
    {"ExpireCode", 10, true, true, true, RippleType_Blob},
    {"CreateCode", 11, true, true, true, RippleType_Blob},
    {"MemoType", 12, true, true, true, RippleType_Blob},
    {"MemoData", 13, true, true, true, RippleType_Blob},
    {"MemoFormat", 14, true, true, true, RippleType_Blob},
    {"Fulfillment", 16, true, true, true, RippleType_Blob},
    {"Condition", 17, true, true, true, RippleType_Blob},
    {"MasterSignature", 18, true, true, false, RippleType_Blob},
    {"Account", 1, true, true, true, RippleType_AccountID},
    {"Owner", 2, true, true, true, RippleType_AccountID},
    {"Destination", 3, true, true, true, RippleType_AccountID},
    {"Issuer", 4, true, true, true, RippleType_AccountID},
    {"Authorize", 5, true, true, true, RippleType_AccountID},
    {"Unauthorize", 6, true, true, true, RippleType_AccountID},
    {"Target", 7, true, true, true, RippleType_AccountID},
    {"RegularKey", 8, true, true, true, RippleType_AccountID},
    {"ObjectEndMarker", 1, false, true, true, RippleType_STObject},
    {"TransactionMetaData", 2, false, true, true, RippleType_STObject},
    {"CreatedNode", 3, false, true, true, RippleType_STObject},
    {"DeletedNode", 4, false, true, true, RippleType_STObject},
    {"ModifiedNode", 5, false, true, true, RippleType_STObject},
    {"PreviousFields", 6, false, true, true, RippleType_STObject},
    {"FinalFields", 7, false, true, true, RippleType_STObject},
    {"NewFields", 8, false, true, true, RippleType_STObject},
    {"TemplateEntry", 9, false, true, true, RippleType_STObject},
    {"Memo", 10, false, true, true, RippleType_STObject},
    {"SignerEntry", 11, false, true, true, RippleType_STObject},
    {"Signer", 16, false, true, true, RippleType_STObject},
    {"Majority", 18, false, true, true, RippleType_STObject},
    {"ArrayEndMarker", 1, false, true, true, RippleType_STArray},
    {"Signers", 3, false, true, false, RippleType_STArray},
    {"SignerEntries", 4, false, true, true, RippleType_STArray},
    {"Template", 5, false, true, true, RippleType_STArray},
    {"Necessary", 6, false, true, true, RippleType_STArray},
    {"Sufficient", 7, false, true, true, RippleType_STArray},
    {"AffectedNodes", 8, false, true, true, RippleType_STArray},
    {"Memos", 9, false, true, true, RippleType_STArray},
    {"Majorities", 16, false, true, true, RippleType_STArray},
    {"CloseResolution", 1, false, true, true, RippleType_UInt8},
    {"Method", 2, false, true, true, RippleType_UInt8},
    {"TransactionResult", 3, false, true, true, RippleType_UInt8},
    {"TakerPaysCurrency", 1, false, true, true, RippleType_Hash160},
    {"TakerPaysIssuer", 2, false, true, true, RippleType_Hash160},
    {"TakerGetsCurrency", 3, false, true, true, RippleType_Hash160},
    {"TakerGetsIssuer", 4, false, true, true, RippleType_Hash160},
    {"Paths", 1, false, true, true, RippleType_PathSet},
    {"Indexes", 1, true, true, true, RippleType_Vector256},
    {"Hashes", 2, true, true, true, RippleType_Vector256},
    {"Amendments", 3, true, true, true, RippleType_Vector256},
    {"Transaction", 1, false, false, false, RippleType_Transaction},
    {"LedgerEntry", 1, false, false, false, RippleType_LedgerEntry},
    {"Validation", 1, false, false, false, RippleType_Validation},
    {"SignerListID", 38, false, true, true, RippleType_UInt32},
    {"SettleDelay", 39, false, true, true, RippleType_UInt32},
    {"Channel", 22, false, true, true, RippleType_Hash256},
    {"ConsensusHash", 23, false, true, true, RippleType_Hash256},
    {"CheckID", 24, false, true, true, RippleType_Hash256},
    {"TickSize", 16, false, true, true, RippleType_UInt8},
    {"DestinationNode", 9, false, true, true, RippleType_UInt64}};

static void encodeAmount(uint64_t amount, uint8_t buf[8]) {
  for (int i = 0; i < 8; i++) {
    buf[7 - i] = amount & 0x00000000000000FF;
    amount = amount >> 8;
  }
  buf[0] = buf[0] & 0x7f;  // first bit to be zero: indicates XRP amount
  buf[0] = buf[0] | 0x40;  // second bit to be one: indicates positive value
}
// static void encodeAmount(double amount, char curCode[4], uint8_t
// accountId[20], uint8_t buf[48]);

static uint32_t setFlags(const RippleSignTx *msg) {
  uint32_t flags = 0;
  if (!msg->has_flags) {
    flags = msg->flags;
  }
  flags = flags | FLAG_FULLY_CANONICAL;
  return flags;
}

static bool checkFee(const uint64_t fee) {
  return (fee > MIN_FEE && fee < MAX_FEE);
}
bool confirmRipplePayment(const HDNode *node, const RippleSignTx *msg,
                          RippleSignedTx *resp) {
  layoutRipplePayment(msg->payment.destination, msg->payment.amount,
                      msg->payment.destination_tag);
  if (!protectButton(ButtonRequestType_ButtonRequest_SignTx, false)) {
    fsm_sendFailure(FailureType_Failure_ActionCancelled, "Signing cancelled");
    return false;
  }
  layoutConfirmRippleFee(msg->fee);
  if (!protectButton(ButtonRequestType_ButtonRequest_SignTx, false)) {
    fsm_sendFailure(FailureType_Failure_ActionCancelled, "Signing cancelled");
    return false;
  }

  layoutProgress(_("Preparing Transaction"), 0);

  uint32_t flags = setFlags(msg);

  uint8_t amountBuf[8];
  if (msg->payment.has_issued_amount) {
    fsm_sendFailure(FailureType_Failure_UnexpectedMessage,
                    "Non-XRP currency isn't supported for now.");
    return false;
  } else {
    encodeAmount(msg->payment.amount, amountBuf);
  }

  if (!checkFee(msg->fee)) {
    fsm_sendFailure(FailureType_Failure_ProcessError,
                    "Fee must be in the range of 10 to 10,000 drops");
    return false;
  }
  uint8_t feeBuf[8];
  encodeAmount(msg->fee, feeBuf);

  uint8_t sourceAccount[20] = {0};
  hdnode_get_ripple_address_raw(node, sourceAccount);

  uint8_t destAccount[21];
  int alen = base58r_decode_check(msg->payment.destination, HASHER_SHA2D,
                                  destAccount, 21);
  if (alen != 21) {
    fsm_sendFailure(FailureType_Failure_ProcessError,
                    _("The length of destination is not 21."));
    return false;
  }

  TransactionField_t tf_payment[] = {
      {TransactionField_Flags, UL2B(flags), 4},
      {TransactionField_TransactionType, US2B(TransactionType_Payment), 2},
      {TransactionField_Sequence, UL2B(msg->sequence), 4},
      {TransactionField_LastLedgerSequence, UL2B(msg->last_ledger_sequence), 4},
      {TransactionField_DestinationTag, UL2B(msg->payment.destination_tag), 4},
      {TransactionField_Amount, amountBuf, 8},
      {TransactionField_Fee, feeBuf, 8},
      {TransactionField_Account, sourceAccount, 20},
      {TransactionField_Destination, destAccount + 1, 20},
      {TransactionField_TxnSignature, NULL, 0},
      {TransactionField_SigningPubKey, node->public_key, 33}};
  size_t tf_payment_length = sizeof(tf_payment) / sizeof(tf_payment[0]);

  if (createRippleSignedTx(node, tf_payment, tf_payment_length, resp) < 0) {
    fsm_sendFailure(FailureType_Failure_ProcessError,
                    _("An error occured during creating signed transaction."));
    return false;
  }

  return true;
}

bool confirmRippleSignerListSet(const HDNode *node, const RippleSignTx *msg,
                                RippleSignedTx *resp) {
  layoutRippleSignerListSet();
  if (!protectButton(ButtonRequestType_ButtonRequest_SignTx, false)) {
    fsm_sendFailure(FailureType_Failure_ActionCancelled, "Signing cancelled");
    return false;
  }
  layoutConfirmRippleFee(msg->fee);
  if (!protectButton(ButtonRequestType_ButtonRequest_SignTx, false)) {
    fsm_sendFailure(FailureType_Failure_ActionCancelled, "Signing cancelled");
    return false;
  }

  uint32_t flags = setFlags(msg);

  uint8_t feeBuf[8];
  encodeAmount(msg->fee, feeBuf);

  uint8_t sourceAccount[20] = {0};
  hdnode_get_ripple_address_raw(node, sourceAccount);

  TransactionField_t tf_signerlistset[] = {
      {TransactionField_Flags, UL2B(flags), 4},
      {TransactionField_TransactionType, US2B(TransactionType_SignerListSet),
       2},
      {TransactionField_Sequence, UL2B(msg->sequence), 4},
      {TransactionField_LastLedgerSequence, UL2B(msg->last_ledger_sequence), 4},
      {TransactionField_Fee, feeBuf, 8},
      {TransactionField_Account, sourceAccount, 20},
      {TransactionField_TxnSignature, NULL, 0},
      {TransactionField_SigningPubKey, node->public_key, 33},
      {TransactionField_SignerQuorum, UL2B(msg->signer_list_set.signer_quorum),
       4},
      {TransactionField_SignerEntries, NULL, 0}};
  size_t tf_signerlistset_length =
      sizeof(tf_signerlistset) / sizeof(tf_signerlistset[0]);
  if (createRippleSignedTx(node, tf_signerlistset, tf_signerlistset_length,
                           resp) < 0) {
    fsm_sendFailure(FailureType_Failure_ProcessError,
                    _("An error occured during creating signed transaction."));
    return false;
  }
  return true;
}

int createRippleSignedTx(const HDNode *node, TransactionField_t *tf,
                         size_t nField, RippleSignedTx *resp) {
  uint8_t tx_unsigned[1024] = {0};
  tx_unsigned[0] = 0x53;
  tx_unsigned[1] = 0x54;
  tx_unsigned[2] = 0x58;
  tx_unsigned[3] = 0x00;
  int serializedSize =
      serializeRippleTx(tf, nField, false, tx_unsigned + 4, 1024 - 4);
  if (serializedSize <= 0) {
    return -1;
  }
  uint8_t txHash[SHA512_DIGEST_LENGTH] = {0};
  sha512_Raw(tx_unsigned, serializedSize + 4,
             txHash);  // length of (serialized transaction + prefix)
  uint8_t signature[64] = {0};
  ecdsa_sign_digest(node->curve->params, node->private_key, txHash, signature,
                    NULL, NULL);
  uint8_t derSig[72] = {0};
  int sigLen = ecdsa_sig_to_der(signature, derSig);
  if (sigLen <= 0) {
    return -2;
  }
  resp->has_signature = true;
  resp->signature.size = sigLen;
  memcpy(resp->signature.bytes, derSig, sigLen);
  for (int i = 0; i < (int)nField; ++i) {
    if (tf[i].field == TransactionField_TxnSignature) {
      tf[i].buf = derSig;
      tf[i].vlSize = sigLen;
    }
  }

  memset(tx_unsigned, 0, 1024);  // reinitialize and reuse tx_unsigned buffer
  serializedSize = serializeRippleTx(tf, nField, true, tx_unsigned, 1024);

  if (serializedSize <= 0) {
    return -3;
  }

  resp->has_serialized_tx = true;
  memcpy(resp->serialized_tx.bytes, tx_unsigned, serializedSize);
  resp->serialized_tx.size = serializedSize;
  return 0;
}

#define COPY_BUF(BYTELEN)                         \
  memcpy(&serialized[serSz], tf[i].buf, BYTELEN); \
  serSz += BYTELEN;

int serializeRippleTx(TransactionField_t *tf, size_t nField, bool hasSignature,
                      uint8_t *serialized, int maxSerializedSize) {
  int serSz = 0;

  // bubble sort by type code then field code
  for (int i = 0; i < (int)nField; i++) {
    for (int j = ((int)nField) - 1; j > i; j--) {
      struct RippleField left =
          rippleFields[tf[j - 1].field];  // this is not pointer
      struct RippleField right = rippleFields[tf[j].field];

      if (tf[j - 1].field == TransactionField_Invalid ||
          right.type < left.type ||
          (right.type == left.type && right.nth < left.nth)) {
        TransactionField_t temp = tf[j - 1];
        tf[j - 1] = tf[j];
        tf[j] = temp;
      }
    }
  }
  // sort end
  for (int i = 0; i < (int)nField; ++i) {
    layoutProgress(_("Serializing Transaction"), 30 + i * 30);
    struct RippleField fieldInfo = rippleFields[tf[i].field];
    if (!fieldInfo.isSerialized ||
        (!hasSignature && !fieldInfo.isSigningField)) {
      continue;
    }

    // write fieldId

    if (fieldInfo.type < 16 && fieldInfo.nth < 16) {
      serialized[serSz] = ((fieldInfo.type << 4) | fieldInfo.nth);
      serSz += 1;
    } else if (fieldInfo.type >= 16 && fieldInfo.nth < 16) {
      serialized[serSz] = fieldInfo.nth;
      serialized[serSz + 1] = fieldInfo.type;
      serSz += 2;
    } else if (fieldInfo.type < 16 && fieldInfo.nth >= 16) {
      serialized[serSz] = (fieldInfo.type << 4);
      serialized[serSz + 1] = fieldInfo.nth;
      serSz += 2;
    } else if (fieldInfo.type >= 16 && fieldInfo.nth >= 16) {
      serialized[serSz] = 0;
      serialized[serSz + 1] = fieldInfo.type;
      serialized[serSz + 2] = fieldInfo.nth;
      serSz += 3;
    }
    // write fieldId end

    if (fieldInfo.isVLEncoded) {
      // See Serializer::addEncoded(int)
      // https://github.com/ripple/rippled/blob/381a1b948b06d9526cc73f14cfc69635fabf8605/src/ripple/protocol/impl/Serializer.cpp#L303
      int vs = tf[i].vlSize;
      if (fieldInfo.type == RippleType_AccountID) {
        vs = 20;
      }
      if (vs < 192) {
        serialized[serSz] = (uint8_t)(vs & 0x000000FF);
        serSz += 1;
      } else if (vs <= 12480) {
        vs -= 193;
        serialized[serSz] = 193 + ((uint8_t)(vs >> 8));
        serialized[serSz + 1] = (uint8_t)(vs & 0xff);
        serSz += 2;
      } else if (vs <= 918744) {
        vs -= 12481;
        serialized[serSz] = 241 + ((uint8_t)(vs >> 16));
        serialized[serSz + 1] = (uint8_t)((vs >> 8) & 0xff);
        serialized[serSz + 2] = (uint8_t)(vs && 0xff);
        serSz += 3;
      } else {
        return -2;
      }
      COPY_BUF((fieldInfo.type == RippleType_AccountID) ? 20 : tf[i].vlSize);
    } else {
      switch (fieldInfo.type) {
        case RippleType_UInt8:
          COPY_BUF(1);
          break;
        case RippleType_UInt16:
          COPY_BUF(2);
          break;
        case RippleType_UInt32:
          COPY_BUF(4);
          break;
        case RippleType_UInt64:
          COPY_BUF(8);
          break;
        case RippleType_Hash128:
          COPY_BUF(16);
          break;
        case RippleType_Hash256:
          COPY_BUF(32);
          break;
        case RippleType_Amount:
          if ((tf[i].buf[0] & 0b10000000) == 0) {
            COPY_BUF(8);
          } else {
            COPY_BUF(48);
          }
          break;
        default:
          return -3;
          // fields that typecode is greater than 10 is not implemented yet.
      }
    }
    if (serSz > maxSerializedSize) {
      return -4;
    }
  }

  return serSz;
}

static void drops_to_xrp_formatted(uint64_t value, char *formated_value) {
  bn_format_uint64(value, NULL, " XRP", 6, 0, false, formated_value,
                   MAX_XRP_VALUE_SIZE);
}

void layoutRipplePayment(const char *recipient_addr, const uint64_t drops,
                         const uint32_t tag) {
  char formatted_amount[MAX_XRP_VALUE_SIZE];
  char formatted_recipient[MAX_XRP_RECIPIENT_SIZE] = {0};
  snprintf(formatted_recipient, MAX_XRP_RECIPIENT_SIZE, "%s(Tag:%lu)",
           recipient_addr, (unsigned long)tag);
  const char **str = split_message((const uint8_t *)formatted_recipient,
                                   strlen(formatted_recipient), 16);
  drops_to_xrp_formatted(drops, formatted_amount);
  layoutDialogSwipe(&bmp_icon_question, _("Cancel"), _("Confirm"), NULL,
                    _("Confirm sending XRP to:"), str[0], str[1], str[2], NULL,
                    NULL);
}

void layoutRippleSignerListSet() {
  layoutDialogSwipe(&bmp_icon_question, _("Cancel"), _("Confirm"), NULL,
                    _("Confirm setting signers?"), NULL, NULL, NULL, NULL,
                    NULL);
}
void layoutConfirmRippleFee(const uint64_t fee) {
  char formatted_fee[MAX_XRP_VALUE_SIZE];
  drops_to_xrp_formatted(fee, formatted_fee);
  layoutDialogSwipe(&bmp_icon_question, _("Cancel"), _("Confirm"), NULL,
                    _("Confirm transaction"), _("fee:"), formatted_fee, NULL,
                    NULL, NULL);
}
