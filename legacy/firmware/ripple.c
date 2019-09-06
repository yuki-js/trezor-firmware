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

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include "ripple.h"
#include "layout2.h"
#include "fsm.h"
#include "messages.pb.h"
#include "messages-ripple.pb.h"
#include "gettext.h"
#include "bitmaps.h"
#include "bip32.h"
#include "util.h"
#include "protect.h"

struct RippleField rippleFields[] = {
                                     { "Generic", 0, false, false, false, RippleType_Unknown },
                                     { "Invalid", -1, false, false, false, RippleType_Unknown },
                                     { "LedgerEntryType", 1, false, true, true, RippleType_UInt16 },
                                     { "TransactionType", 2, false, true, true, RippleType_UInt16 },
                                     { "SignerWeight", 3, false, true, true, RippleType_UInt16 },
                                     { "Flags", 2, false, true, true, RippleType_UInt32 },
                                     { "SourceTag", 3, false, true, true, RippleType_UInt32 },
                                     { "Sequence", 4, false, true, true, RippleType_UInt32 },
                                     { "PreviousTxnLgrSeq", 5, false, true, true, RippleType_UInt32 },
                                     { "LedgerSequence", 6, false, true, true, RippleType_UInt32 },
                                     { "CloseTime", 7, false, true, true, RippleType_UInt32 },
                                     { "ParentCloseTime", 8, false, true, true, RippleType_UInt32 },
                                     { "SigningTime", 9, false, true, true, RippleType_UInt32 },
                                     { "Expiration", 10, false, true, true, RippleType_UInt32 },
                                     { "TransferRate", 11, false, true, true, RippleType_UInt32 },
                                     { "WalletSize", 12, false, true, true, RippleType_UInt32 },
                                     { "OwnerCount", 13, false, true, true, RippleType_UInt32 },
                                     { "DestinationTag", 14, false, true, true, RippleType_UInt32 },
                                     { "HighQualityIn", 16, false, true, true, RippleType_UInt32 },
                                     { "HighQualityOut", 17, false, true, true, RippleType_UInt32 },
                                     { "LowQualityIn", 18, false, true, true, RippleType_UInt32 },
                                     { "LowQualityOut", 19, false, true, true, RippleType_UInt32 },
                                     { "QualityIn", 20, false, true, true, RippleType_UInt32 },
                                     { "QualityOut", 21, false, true, true, RippleType_UInt32 },
                                     { "StampEscrow", 22, false, true, true, RippleType_UInt32 },
                                     { "BondAmount", 23, false, true, true, RippleType_UInt32 },
                                     { "LoadFee", 24, false, true, true, RippleType_UInt32 },
                                     { "OfferSequence", 25, false, true, true, RippleType_UInt32 },
                                     { "FirstLedgerSequence", 26, false, true, true, RippleType_UInt32 },
                                     { "LastLedgerSequence", 27, false, true, true, RippleType_UInt32 },
                                     { "TransactionIndex", 28, false, true, true, RippleType_UInt32 },
                                     { "OperationLimit", 29, false, true, true, RippleType_UInt32 },
                                     { "ReferenceFeeUnits", 30, false, true, true, RippleType_UInt32 },
                                     { "ReserveBase", 31, false, true, true, RippleType_UInt32 },
                                     { "ReserveIncrement", 32, false, true, true, RippleType_UInt32 },
                                     { "SetFlag", 33, false, true, true, RippleType_UInt32 },
                                     { "ClearFlag", 34, false, true, true, RippleType_UInt32 },
                                     { "SignerQuorum", 35, false, true, true, RippleType_UInt32 },
                                     { "CancelAfter", 36, false, true, true, RippleType_UInt32 },
                                     { "FinishAfter", 37, false, true, true, RippleType_UInt32 },
                                     { "IndexNext", 1, false, true, true, RippleType_UInt64 },
                                     { "IndexPrevious", 2, false, true, true, RippleType_UInt64 },
                                     { "BookNode", 3, false, true, true, RippleType_UInt64 },
                                     { "OwnerNode", 4, false, true, true, RippleType_UInt64 },
                                     { "BaseFee", 5, false, true, true, RippleType_UInt64 },
                                     { "ExchangeRate", 6, false, true, true, RippleType_UInt64 },
                                     { "LowNode", 7, false, true, true, RippleType_UInt64 },
                                     { "HighNode", 8, false, true, true, RippleType_UInt64 },
                                     { "EmailHash", 1, false, true, true, RippleType_Hash128 },
                                     { "LedgerHash", 1, false, true, true, RippleType_Hash256 },
                                     { "ParentHash", 2, false, true, true, RippleType_Hash256 },
                                     { "TransactionHash", 3, false, true, true, RippleType_Hash256 },
                                     { "AccountHash", 4, false, true, true, RippleType_Hash256 },
                                     { "PreviousTxnID", 5, false, true, true, RippleType_Hash256 },
                                     { "LedgerIndex", 6, false, true, true, RippleType_Hash256 },
                                     { "WalletLocator", 7, false, true, true, RippleType_Hash256 },
                                     { "RootIndex", 8, false, true, true, RippleType_Hash256 },
                                     { "AccountTxnID", 9, false, true, true, RippleType_Hash256 },
                                     { "BookDirectory", 16, false, true, true, RippleType_Hash256 },
                                     { "InvoiceID", 17, false, true, true, RippleType_Hash256 },
                                     { "Nickname", 18, false, true, true, RippleType_Hash256 },
                                     { "Amendment", 19, false, true, true, RippleType_Hash256 },
                                     { "TicketID", 20, false, true, true, RippleType_Hash256 },
                                     { "Digest", 21, false, true, true, RippleType_Hash256 },
                                     { "hash", 257, false, false, false, RippleType_Hash256 },
                                     { "index", 258, false, false, false, RippleType_Hash256 },
                                     { "Amount", 1, false, true, true, RippleType_Amount },
                                     { "Balance", 2, false, true, true, RippleType_Amount },
                                     { "LimitAmount", 3, false, true, true, RippleType_Amount },
                                     { "TakerPays", 4, false, true, true, RippleType_Amount },
                                     { "TakerGets", 5, false, true, true, RippleType_Amount },
                                     { "LowLimit", 6, false, true, true, RippleType_Amount },
                                     { "HighLimit", 7, false, true, true, RippleType_Amount },
                                     { "Fee", 8, false, true, true, RippleType_Amount },
                                     { "SendMax", 9, false, true, true, RippleType_Amount },
                                     { "DeliverMin", 10, false, true, true, RippleType_Amount },
                                     { "MinimumOffer", 16, false, true, true, RippleType_Amount },
                                     { "RippleEscrow", 17, false, true, true, RippleType_Amount },
                                     { "DeliveredAmount", 18, false, true, true, RippleType_Amount },
                                     { "taker_gets_funded", 258, false, false, false, RippleType_Amount },
                                     { "taker_pays_funded", 259, false, false, false, RippleType_Amount },
                                     { "PublicKey", 1, true, true, true, RippleType_Blob },
                                     { "MessageKey", 2, true, true, true, RippleType_Blob },
                                     { "SigningPubKey", 3, true, true, true, RippleType_Blob },
                                     { "TxnSignature", 4, true, true, false, RippleType_Blob },
                                     { "Generator", 5, true, true, true, RippleType_Blob },
                                     { "Signature", 6, true, true, false, RippleType_Blob },
                                     { "Domain", 7, true, true, true, RippleType_Blob },
                                     { "FundCode", 8, true, true, true, RippleType_Blob },
                                     { "RemoveCode", 9, true, true, true, RippleType_Blob },
                                     { "ExpireCode", 10, true, true, true, RippleType_Blob },
                                     { "CreateCode", 11, true, true, true, RippleType_Blob },
                                     { "MemoType", 12, true, true, true, RippleType_Blob },
                                     { "MemoData", 13, true, true, true, RippleType_Blob },
                                     { "MemoFormat", 14, true, true, true, RippleType_Blob },
                                     { "Fulfillment", 16, true, true, true, RippleType_Blob },
                                     { "Condition", 17, true, true, true, RippleType_Blob },
                                     { "MasterSignature", 18, true, true, false, RippleType_Blob },
                                     { "Account", 1, true, true, true, RippleType_AccountID },
                                     { "Owner", 2, true, true, true, RippleType_AccountID },
                                     { "Destination", 3, true, true, true, RippleType_AccountID },
                                     { "Issuer", 4, true, true, true, RippleType_AccountID },
                                     { "Authorize", 5, true, true, true, RippleType_AccountID },
                                     { "Unauthorize", 6, true, true, true, RippleType_AccountID },
                                     { "Target", 7, true, true, true, RippleType_AccountID },
                                     { "RegularKey", 8, true, true, true, RippleType_AccountID },
                                     { "ObjectEndMarker", 1, false, true, true, RippleType_STObject },
                                     { "TransactionMetaData", 2, false, true, true, RippleType_STObject },
                                     { "CreatedNode", 3, false, true, true, RippleType_STObject },
                                     { "DeletedNode", 4, false, true, true, RippleType_STObject },
                                     { "ModifiedNode", 5, false, true, true, RippleType_STObject },
                                     { "PreviousFields", 6, false, true, true, RippleType_STObject },
                                     { "FinalFields", 7, false, true, true, RippleType_STObject },
                                     { "NewFields", 8, false, true, true, RippleType_STObject },
                                     { "TemplateEntry", 9, false, true, true, RippleType_STObject },
                                     { "Memo", 10, false, true, true, RippleType_STObject },
                                     { "SignerEntry", 11, false, true, true, RippleType_STObject },
                                     { "Signer", 16, false, true, true, RippleType_STObject },
                                     { "Majority", 18, false, true, true, RippleType_STObject },
                                     { "ArrayEndMarker", 1, false, true, true, RippleType_STArray },
                                     { "Signers", 3, false, true, false, RippleType_STArray },
                                     { "SignerEntries", 4, false, true, true, RippleType_STArray },
                                     { "Template", 5, false, true, true, RippleType_STArray },
                                     { "Necessary", 6, false, true, true, RippleType_STArray },
                                     { "Sufficient", 7, false, true, true, RippleType_STArray },
                                     { "AffectedNodes", 8, false, true, true, RippleType_STArray },
                                     { "Memos", 9, false, true, true, RippleType_STArray },
                                     { "Majorities", 16, false, true, true, RippleType_STArray },
                                     { "CloseResolution", 1, false, true, true, RippleType_UInt8 },
                                     { "Method", 2, false, true, true, RippleType_UInt8 },
                                     { "TransactionResult", 3, false, true, true, RippleType_UInt8 },
                                     { "TakerPaysCurrency", 1, false, true, true, RippleType_Hash160 },
                                     { "TakerPaysIssuer", 2, false, true, true, RippleType_Hash160 },
                                     { "TakerGetsCurrency", 3, false, true, true, RippleType_Hash160 },
                                     { "TakerGetsIssuer", 4, false, true, true, RippleType_Hash160 },
                                     { "Paths", 1, false, true, true, RippleType_PathSet },
                                     { "Indexes", 1, true, true, true, RippleType_Vector256 },
                                     { "Hashes", 2, true, true, true, RippleType_Vector256 },
                                     { "Amendments", 3, true, true, true, RippleType_Vector256 },
                                     { "Transaction", 1, false, false, false, RippleType_Transaction },
                                     { "LedgerEntry", 1, false, false, false, RippleType_LedgerEntry },
                                     { "Validation", 1, false, false, false, RippleType_Validation },
                                     { "SignerListID", 38, false, true, true, RippleType_UInt32 },
                                     { "SettleDelay", 39, false, true, true, RippleType_UInt32 },
                                     { "Channel", 22, false, true, true, RippleType_Hash256 },
                                     { "ConsensusHash", 23, false, true, true, RippleType_Hash256 },
                                     { "CheckID", 24, false, true, true, RippleType_Hash256 },
                                     { "TickSize", 16, false, true, true, RippleType_UInt8 },
                                     { "DestinationNode", 9, false, true, true, RippleType_UInt64 }
};

static char* toByte(uint64_t num, uint8_t bytes){:
  char byteArray[bytes] = {};
  while(bytes){
    byteArray[bytes-1]=num & 0x00000000000000ff;
    num=num>>2;
    bytes--;
  }
  return byteArray;
}

bool confirmRipplePayment(const HDNode *node, const RippleSignTx *msg, RippleSignedTx *resp){
  layoutRipplePayment(msg->payment.destination,msg->payment.amount,msg->payment.destination_tag);
  if (!protectButton(ButtonRequestType_ButtonRequest_SignTx,false)) {
    fsm_sendFailure(FailureType_Failure_ActionCancelled, "Signing cancelled");
    return false;
  }
  layoutConfirmRippleFee(msg->fee);
  if (!protectButton(ButtonRequestType_ButtonRequest_SignTx,false)) {
    fsm_sendFailure(FailureType_Failure_ActionCancelled, "Signing cancelled");
    return false;
  }
  layoutProgressSwipe(_("Gathering information"), 0);
  struct TransactionField tf[20]={
                                  {TransactionField_TransactionType, toByte(TransactionType_Payment, 2), 2},
                                  {TransactionField_Flags, {0,0,0,0}, 4}
  };
  if(!serializeRippleTx(tf,20,NULL,NULL)){
    fsm_sendFailure(FailureType_Failure_ActionCancelled, "Signing cancelled");
    return false;
  }
  if(resp){
    
  }
  return true;
}

bool serializeRippleTx(struct *TransactionField tf, uint8_t elems, uint8_t *result, uint32_t *serializedSize){
  if(tf||elems||result||serializedSize){return false;}
}


static void drops_to_xrp_formatted(uint64_t value, char *formated_value) {
  bn_format_uint64(value, NULL, " XRP", 6, 0, false, formated_value,
                   MAX_XRP_VALUE_SIZE);
}

void layoutRipplePayment(const char *recipient_addr, const uint64_t drops, const uint32_t tag){
  char formatted_amount[MAX_XRP_VALUE_SIZE];
  char formatted_recipient[MAX_XRP_RECIPIENT_SIZE] ={0};
  snprintf(formatted_recipient,MAX_XRP_RECIPIENT_SIZE,"%s(Tag:%lu)",recipient_addr,(unsigned long)tag);
  const char **str =
    split_message((const uint8_t *)formatted_recipient, strlen(formatted_recipient), 16);
  drops_to_xrp_formatted(drops, formatted_amount);
  layoutDialogSwipe(&bmp_icon_question, _("Cancel"), _("Confirm"), NULL,
                    _("Confirm sending XRP to:"), str[0],
                    str[1], str[2],NULL,NULL);

}
void layoutConfirmRippleFee(const uint64_t fee){
  char formatted_fee[MAX_XRP_VALUE_SIZE];
  drops_to_xrp_formatted(fee, formatted_fee);
  layoutDialogSwipe(&bmp_icon_question, _("Cancel"), _("Confirm"), NULL,
                    _("Confirm transaction"), _("fee:"),
                    formatted_fee, NULL, NULL, NULL);
}
