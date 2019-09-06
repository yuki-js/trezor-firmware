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

// unsinged integer to buffer
#define ULL2B(NUM) (uint8_t[]){ (NUM & 0xFF00000000000000)>>56, (NUM & 0x00FF000000000000)>>48, (NUM & 0x0000FF0000000000)>>40, (NUM & 0x000000FF00000000)>>32, (NUM & 0x00000000FF000000)>>24, (NUM & 0x0000000000FF0000)>>16, (NUM & 0x000000000000FF00)>>8, (NUM & 0x00000000000000FF)>>0 }
#define UL2B(NUM) (uint8_t[]){ (NUM & 0xFF000000)>>24, (NUM & 0x00FF0000)>>16, (NUM & 0x0000FF00)>>8, (NUM & 0x000000FF) }
#define US2B(NUM) (uint8_t[]){ (NUM & 0xFF00)>>8, (NUM & 0x00FF) }
#define UC2B(NUM) (uint8_t[]){ (NUM & 0xFF) }

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

enum TransactionTypes {
                       TransactionType_Invalid = -1,
                       TransactionType_Payment = 0,
                       TransactionType_EscrowCreate = 1,
                       TransactionType_EscrowFinish = 2,
                       TransactionType_AccountSet = 3,
                       TransactionType_EscrowCancel = 4,
                       TransactionType_SetRegularKey = 5,
                       TransactionType_NickNameSet = 6,
                       TransactionType_OfferCreate = 7,
                       TransactionType_OfferCancel = 8,
                       TransactionType_Contract = 9,
                       TransactionType_TicketCreate = 10,
                       TransactionType_TicketCancel = 11,
                       TransactionType_SignerListSet = 12,
                       TransactionType_PaymentChannelCreate = 13,
                       TransactionType_PaymentChannelFund = 14,
                       TransactionType_PaymentChannelClaim = 15,
                       TransactionType_CheckCreate = 16,
                       TransactionType_CheckCash = 17,
                       TransactionType_CheckCancel = 18,
                       TransactionType_DepositPreauth = 19,
                       TransactionType_TrustSet = 20,
                       TransactionType_EnableAmendment = 100,
                       TransactionType_SetFee = 101
};

enum TransactionFields {
                        TransactionField_Generic = 0,
                        TransactionField_Invalid = 1,
                        TransactionField_LedgerEntryType = 2,
                        TransactionField_TransactionType = 3,
                        TransactionField_SignerWeight = 4,
                        TransactionField_Flags = 5,
                        TransactionField_SourceTag = 6,
                        TransactionField_Sequence = 7,
                        TransactionField_PreviousTxnLgrSeq = 8,
                        TransactionField_LedgerSequence = 9,
                        TransactionField_CloseTime = 10,
                        TransactionField_ParentCloseTime = 11,
                        TransactionField_SigningTime = 12,
                        TransactionField_Expiration = 13,
                        TransactionField_TransferRate = 14,
                        TransactionField_WalletSize = 15,
                        TransactionField_OwnerCount = 16,
                        TransactionField_DestinationTag = 17,
                        TransactionField_HighQualityIn = 18,
                        TransactionField_HighQualityOut = 19,
                        TransactionField_LowQualityIn = 20,
                        TransactionField_LowQualityOut = 21,
                        TransactionField_QualityIn = 22,
                        TransactionField_QualityOut = 23,
                        TransactionField_StampEscrow = 24,
                        TransactionField_BondAmount = 25,
                        TransactionField_LoadFee = 26,
                        TransactionField_OfferSequence = 27,
                        TransactionField_FirstLedgerSequence = 28,
                        TransactionField_LastLedgerSequence = 29,
                        TransactionField_TransactionIndex = 30,
                        TransactionField_OperationLimit = 31,
                        TransactionField_ReferenceFeeUnits = 32,
                        TransactionField_ReserveBase = 33,
                        TransactionField_ReserveIncrement = 34,
                        TransactionField_SetFlag = 35,
                        TransactionField_ClearFlag = 36,
                        TransactionField_SignerQuorum = 37,
                        TransactionField_CancelAfter = 38,
                        TransactionField_FinishAfter = 39,
                        TransactionField_IndexNext = 40,
                        TransactionField_IndexPrevious = 41,
                        TransactionField_BookNode = 42,
                        TransactionField_OwnerNode = 43,
                        TransactionField_BaseFee = 44,
                        TransactionField_ExchangeRate = 45,
                        TransactionField_LowNode = 46,
                        TransactionField_HighNode = 47,
                        TransactionField_EmailHash = 48,
                        TransactionField_LedgerHash = 49,
                        TransactionField_ParentHash = 50,
                        TransactionField_TransactionHash = 51,
                        TransactionField_AccountHash = 52,
                        TransactionField_PreviousTxnID = 53,
                        TransactionField_LedgerIndex = 54,
                        TransactionField_WalletLocator = 55,
                        TransactionField_RootIndex = 56,
                        TransactionField_AccountTxnID = 57,
                        TransactionField_BookDirectory = 58,
                        TransactionField_InvoiceID = 59,
                        TransactionField_Nickname = 60,
                        TransactionField_Amendment = 61,
                        TransactionField_TicketID = 62,
                        TransactionField_Digest = 63,
                        TransactionField_hash = 64,
                        TransactionField_index = 65,
                        TransactionField_Amount = 66,
                        TransactionField_Balance = 67,
                        TransactionField_LimitAmount = 68,
                        TransactionField_TakerPays = 69,
                        TransactionField_TakerGets = 70,
                        TransactionField_LowLimit = 71,
                        TransactionField_HighLimit = 72,
                        TransactionField_Fee = 73,
                        TransactionField_SendMax = 74,
                        TransactionField_DeliverMin = 75,
                        TransactionField_MinimumOffer = 76,
                        TransactionField_RippleEscrow = 77,
                        TransactionField_DeliveredAmount = 78,
                        TransactionField_taker_gets_funded = 79,
                        TransactionField_taker_pays_funded = 80,
                        TransactionField_PublicKey = 81,
                        TransactionField_MessageKey = 82,
                        TransactionField_SigningPubKey = 83,
                        TransactionField_TxnSignature = 84,
                        TransactionField_Generator = 85,
                        TransactionField_Signature = 86,
                        TransactionField_Domain = 87,
                        TransactionField_FundCode = 88,
                        TransactionField_RemoveCode = 89,
                        TransactionField_ExpireCode = 90,
                        TransactionField_CreateCode = 91,
                        TransactionField_MemoType = 92,
                        TransactionField_MemoData = 93,
                        TransactionField_MemoFormat = 94,
                        TransactionField_Fulfillment = 95,
                        TransactionField_Condition = 96,
                        TransactionField_MasterSignature = 97,
                        TransactionField_Account = 98,
                        TransactionField_Owner = 99,
                        TransactionField_Destination = 100,
                        TransactionField_Issuer = 101,
                        TransactionField_Authorize = 102,
                        TransactionField_Unauthorize = 103,
                        TransactionField_Target = 104,
                        TransactionField_RegularKey = 105,
                        TransactionField_ObjectEndMarker = 106,
                        TransactionField_TransactionMetaData = 107,
                        TransactionField_CreatedNode = 108,
                        TransactionField_DeletedNode = 109,
                        TransactionField_ModifiedNode = 110,
                        TransactionField_PreviousFields = 111,
                        TransactionField_FinalFields = 112,
                        TransactionField_NewFields = 113,
                        TransactionField_TemplateEntry = 114,
                        TransactionField_Memo = 115,
                        TransactionField_SignerEntry = 116,
                        TransactionField_Signer = 117,
                        TransactionField_Majority = 118,
                        TransactionField_ArrayEndMarker = 119,
                        TransactionField_Signers = 120,
                        TransactionField_SignerEntries = 121,
                        TransactionField_Template = 122,
                        TransactionField_Necessary = 123,
                        TransactionField_Sufficient = 124,
                        TransactionField_AffectedNodes = 125,
                        TransactionField_Memos = 126,
                        TransactionField_Majorities = 127,
                        TransactionField_CloseResolution = 128,
                        TransactionField_Method = 129,
                        TransactionField_TransactionResult = 130,
                        TransactionField_TakerPaysCurrency = 131,
                        TransactionField_TakerPaysIssuer = 132,
                        TransactionField_TakerGetsCurrency = 133,
                        TransactionField_TakerGetsIssuer = 134,
                        TransactionField_Paths = 135,
                        TransactionField_Indexes = 136,
                        TransactionField_Hashes = 137,
                        TransactionField_Amendments = 138,
                        TransactionField_Transaction = 139,
                        TransactionField_LedgerEntry = 140,
                        TransactionField_Validation = 141,
                        TransactionField_SignerListID = 142,
                        TransactionField_SettleDelay = 143,
                        TransactionField_Channel = 144,
                        TransactionField_ConsensusHash = 145,
                        TransactionField_CheckID = 146,
                        TransactionField_TickSize = 147,
                        TransactionField_DestinationNode = 148
};
struct RippleField {
  char fieldName[20];
  char nth;
  bool isVLEncoded;
  bool isSerialized;
  bool isSigningField;
  enum RippleType type;
};

typedef struct TransactionField{
  enum TransactionFields field;
  uint8_t *buf; // if isVLEncoded is false, buf is raw data. VL will be prepended later
  uint32_t vlSize; // ignored if isVLEncoded is false
} TransactionField_t;

bool confirmRipplePayment(const HDNode *node, const RippleSignTx *msg, RippleSignedTx *resp);
int serializeRippleTx(TransactionField_t *tf, uint8_t nField, bool signing, uint8_t *serialized, uint32_t maxSerializedSize);
void layoutRipplePayment(const char *recipient_addr, const uint64_t drops, const uint32_t tag);
void layoutConfirmRippleFee(const uint64_t fee);

#endif /* __RIPPLE_H__ */
