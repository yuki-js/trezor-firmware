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
#include "../../crypto/ripple.h"
#include "layout2.h"
#include "fsm.h"
#include "messages.pb.h"
#include "messages-ripple.pb.h"
#include "gettext.h"
#include "bitmaps.h"
#include "bip32.h"
#include "util.h"
#include "protect.h"



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
  layoutProgressSwipe(_("Signing transaction"), 0);
  
  serializeRippleTx(node,msg);
  if(resp){
    
  }
  return true;
}

size_t serializeRippleTx(const HDNode *node, const RippleSignTx *msg){
  uint8_t serialized[MAX_RIPPLE_TX_SIZE];
  
  //type

  
  ripple_get_address_raw(node->public_key, serialized);
  if(msg){
    
  }
  return (size_t)4;
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
