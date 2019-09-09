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

void fsm_msgRippleGetAddress(const RippleGetAddress *msg){
  CHECK_INITIALIZED;
  CHECK_PIN;

  RESP_INIT(RippleAddress);
  
  HDNode *node = fsm_getDerivedNode(SECP256K1_NAME, msg->address_n,
                                    msg->address_n_count, NULL);
  if (!node) return;
  hdnode_fill_public_key(node);

  char address[40];
  if(! hdnode_get_ripple_address(node, address) ) return;
  if (msg->has_show_display && msg->show_display) {
    if (!fsm_layoutAddress(address, "Ripple:", true, 0, msg->address_n,
                           msg->address_n_count, false)) {
      return;
    }
  }
  resp->has_address=true;
  strlcpy(resp->address, address, 40);
  msg_write(MessageType_MessageType_RippleAddress, resp);
  layoutHome();
}
void fsm_msgRippleSignTx(const RippleSignTx *msg){
  CHECK_INITIALIZED;
  CHECK_PIN;

  RESP_INIT(RippleSignedTx);
  
  HDNode *node = fsm_getDerivedNode(SECP256K1_NAME, msg->address_n,
                                    msg->address_n_count, NULL);
  if (!node) return;
  
  
  if(
     ( msg->has_payment && !confirmRipplePayment(node, msg, resp) )
     )
    {
      layoutHome();
      return;
    }
  msg_write(MessageType_MessageType_RippleSignedTx, resp);
  layoutHome();
}
