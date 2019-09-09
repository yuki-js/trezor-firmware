/**
 * Copyright (c) 2013-2016 Tomas Dzetkulic
 * Copyright (c) 2013-2016 Pavol Rusnak
 * Copyright (c) 2015-2016 Jochen Hoenicke
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
 * OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */
#include "ripple.h"

#include <string.h>
#include <stdbool.h>
#include "sha2.h"
#include "ripemd160.h"
#include "hasher.h"
#include "base58_ripple.h"

void ripple_get_address_raw(const uint8_t *public_key, uint8_t *accountId){
  uint8_t hash[SHA256_DIGEST_LENGTH];
  
  SHA256_CTX ctx;
  sha256_Init(&ctx);
  sha256_Update(&ctx, public_key, 33); // compressed
  sha256_Final(&ctx, hash);
  
  ripemd160(hash, SHA256_DIGEST_LENGTH, accountId);
  
}
bool ripple_get_address(const uint8_t *public_key, char *address, int addrsize){
  uint8_t raw[1+20];

  ripple_get_address_raw(public_key,raw+1);
  address[0]=0x00; // "r"
  return base58r_encode_check(raw, 20+1, HASHER_SHA2D, address, addrsize);
}
