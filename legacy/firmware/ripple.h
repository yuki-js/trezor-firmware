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

/* b = [["account_set","AccountSet"],["check_cancel","CheckCancel"],["check_cash","CheckCash"],["check_create","CheckCreate"],["deposit_preauth","DepositPreauth"],["escrow_cancel","EscrowCancel"],["escrow_create","EscrowCreate"],["escrow_finish","EscrowFinish"],["offer_cancel","OfferCancel"],["offer_create","OfferCreate"],["payment","Payment"],["payment_channel_claim","PaymentChannelClaim"],["payment_channel_create","PaymentChannelCreate"],["payment_channel_fund","PaymentChannelFund"],["set_regular_key","SetRegularKey"],["signer_list_set","SignerListSet"],["trust_set","TrustSet"]];

   b.map(c=>`( msg->has_${c[0]} && !ripple_Confirm${c[1]}(node, &msg->${c[0]}, resp) )`).join(" ||\n")

   b.map(c=>`bool ripple_Confirm${c[1]}(const HDNode *node, const Ripple${c[1]} *msg, RippleSignedTx *resp){}\n`).join("\n")

   b.map(c=>`bool ripple_Confirm${c[1]}(const HDNode *node, const Ripple${c[1]} *msg, RippleSignedTx *resp);`).join("\n")
*/

#ifndef __RIPPLE_H__
#define __RIPPLE_H__

#include <stdbool.h>
#include "messages-ripple.pb.h"
#include "bip32.h"


#define MAX_XRP_VALUE_SIZE 20
#define MAX_XRP_RECIPIENT_SIZE 40
#define MAX_RIPPLE_TX_SIZE 1024

enum RippleType {
                 RippleType_Validation = 10003,
                 RippleType_Done = -1,
                 RippleType_Hash128 = 4,
                 RippleType_Blob = 7,
                 RippleType_AccountID = 8,
                 RippleType_Amount = 6,
                 RippleType_Hash256 = 5,
                 RippleType_UInt8 = 16,
                 RippleType_Vector256 = 19,
                 RippleType_STObject = 14,
                 RippleType_Unknown = -2,
                 RippleType_Transaction = 10001,
                 RippleType_Hash160 = 17,
                 RippleType_PathSet = 18,
                 RippleType_LedgerEntry = 10002,
                 RippleType_UInt16 = 1,
                 RippleType_NotPresent = 0,
                 RippleType_UInt64 = 3,
                 RippleType_UInt32 = 2,
                 RippleType_STArray = 15
};

struct {
  char fieldName[20];
  short nth;
  bool isVLEncoded;
  bool isSerialized;
  bool isSigningField;
  enum RippleType type;
} rippleFields[] = {
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
  
bool confirmRipplePayment(const HDNode *node, const RippleSignTx *msg, RippleSignedTx *resp);
size_t serializeRippleTx(const HDNode *node, const RippleSignTx *msg);

void layoutRipplePayment(const char *recipient_addr, const uint64_t drops, const uint32_t tag);
void layoutConfirmRippleFee(const uint64_t fee);

#endif /* __RIPPLE_H__ */

