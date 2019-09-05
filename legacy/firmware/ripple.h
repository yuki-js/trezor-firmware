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

struct RippleField {
  char fieldName[20];
  short nth;
  bool isVLEncoded;
  bool isSerialized;
  bool isSigningField;
  enum RippleType type;
};
  
bool confirmRipplePayment(const HDNode *node, const RippleSignTx *msg, RippleSignedTx *resp);
size_t serializeRippleTx(const HDNode *node, const RippleSignTx *msg);

void layoutRipplePayment(const char *recipient_addr, const uint64_t drops, const uint32_t tag);
void layoutConfirmRippleFee(const uint64_t fee);

#endif /* __RIPPLE_H__ */
