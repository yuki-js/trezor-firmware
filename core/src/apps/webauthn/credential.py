import ustruct
from micropython import const

from trezor import log, utils
from trezor.crypto import bip32, chacha20poly1305, hashlib, hmac, random

from apps.common import HARDENED, cbor, storage

if False:
    from typing import Optional

# Credential ID values
_CRED_ID_VERSION = b"\xf1\xd0\x02\x00"
_CRED_ID_MIN_LENGTH = const(33)
_KEY_HANDLE_LENGTH = const(64)

# Credential ID keys
_CRED_ID_RP_ID = const(0x01)
_CRED_ID_RP_NAME = const(0x02)
_CRED_ID_USER_ID = const(0x03)
_CRED_ID_USER_NAME = const(0x04)
_CRED_ID_USER_DISPLAY_NAME = const(0x05)
_CRED_ID_CREATION_TIME = const(0x06)
_CRED_ID_HMAC_SECRET = const(0x07)

# Key paths
_FIDO_KEY_PATH = [HARDENED | 10022, HARDENED | 0xF1D00200]
_FIDO_CRED_ID_KEY_PATH = [b"SLIP-0022", b"FIDO2", b"Encryption key"]
_FIDO_HMAC_SECRET_KEY_PATH = [b"SLIP-0022", b"FIDO2", b"hmac-secret"]
_U2F_KEY_PATH = const(0x80553246)


class Credential:
    def __init__(self) -> None:
        self.id = b""  # type: bytes
        self.rp_id = ""  # type: str
        self.rp_id_hash = b""  # type: bytes
        self.user_id = None  # type: Optional[bytes]

    def app_name(self) -> str:
        return ""

    def account_name(self) -> Optional[str]:
        return None

    def private_key(self) -> bytes:
        return b""

    def hmac_secret_key(self) -> Optional[bytes]:
        return None

    @staticmethod
    def from_bytes(data: bytes, rp_id_hash: bytes) -> Optional["Credential"]:
        cred = Fido2Credential.from_cred_id(
            data, rp_id_hash
        )  # type: Optional[Credential]
        if cred is None:
            cred = U2fCredential.from_key_handle(data, rp_id_hash)
        return cred


class Fido2Credential(Credential):
    def __init__(self) -> None:
        super().__init__()
        self.rp_name = None  # type: Optional[str]
        self.user_name = None  # type: Optional[str]
        self.user_display_name = None  # type: Optional[str]
        self._creation_time = 0  # type: int
        self.hmac_secret = False  # type: bool

    def __lt__(self, other: Credential) -> bool:
        # Sort FIDO2 credentials newest first amongst each other.
        if isinstance(other, Fido2Credential):
            return self._creation_time > other._creation_time

        # Sort FIDO2 credentials before U2F credentials.
        return True

    def generate_id(self) -> None:
        from apps.common import seed

        self._creation_time = storage.device.next_u2f_counter() or 0

        data = cbor.encode(
            {
                key: value
                for key, value in (
                    (_CRED_ID_RP_ID, self.rp_id),
                    (_CRED_ID_RP_NAME, self.rp_name),
                    (_CRED_ID_USER_ID, self.user_id),
                    (_CRED_ID_USER_NAME, self.user_name),
                    (_CRED_ID_USER_DISPLAY_NAME, self.user_display_name),
                    (_CRED_ID_CREATION_TIME, self._creation_time),
                    (_CRED_ID_HMAC_SECRET, self.hmac_secret),
                )
                if value
            }
        )
        key = seed.derive_slip21_node_without_passphrase(_FIDO_CRED_ID_KEY_PATH).key()
        iv = random.bytes(12)
        ctx = chacha20poly1305(key, iv)
        ctx.auth(hashlib.sha256(self.rp_id.encode()).digest())
        ciphertext = ctx.encrypt(data)
        tag = ctx.finish()
        self.id = _CRED_ID_VERSION + iv + ciphertext + tag

    @staticmethod
    def from_cred_id(cred_id: bytes, rp_id_hash: bytes) -> Optional["Fido2Credential"]:
        from apps.common import seed

        if len(cred_id) < _CRED_ID_MIN_LENGTH or cred_id[0:4] != _CRED_ID_VERSION:
            return None

        key = seed.derive_slip21_node_without_passphrase(_FIDO_CRED_ID_KEY_PATH).key()
        iv = cred_id[4:16]
        ciphertext = cred_id[16:-16]
        tag = cred_id[-16:]
        ctx = chacha20poly1305(key, iv)
        ctx.auth(rp_id_hash)
        data = ctx.decrypt(ciphertext)
        if not utils.consteq(ctx.finish(), tag):
            return None

        try:
            data = cbor.decode(data)
        except Exception:
            return None

        if not isinstance(data, dict):
            return None

        cred = Fido2Credential()
        cred.rp_id = data.get(_CRED_ID_RP_ID, None)
        cred.rp_id_hash = rp_id_hash
        cred.rp_name = data.get(_CRED_ID_RP_NAME, None)
        cred.user_id = data.get(_CRED_ID_USER_ID, None)
        cred.user_name = data.get(_CRED_ID_USER_NAME, None)
        cred.user_display_name = data.get(_CRED_ID_USER_DISPLAY_NAME, None)
        cred._creation_time = data.get(_CRED_ID_CREATION_TIME, 0)
        cred.hmac_secret = data.get(_CRED_ID_HMAC_SECRET, False)
        cred.id = cred_id

        if (
            not cred.check_required_fields()
            or not cred.check_data_types()
            or hashlib.sha256(cred.rp_id).digest() != rp_id_hash
        ):
            return None

        return cred

    def check_required_fields(self) -> bool:
        return (
            self.rp_id is not None
            and self.user_id is not None
            and self._creation_time is not None
        )

    def check_data_types(self) -> bool:
        return (
            isinstance(self.rp_id, str)
            and isinstance(self.rp_name, (str, type(None)))
            and isinstance(self.user_id, (bytes, bytearray))
            and isinstance(self.user_name, (str, type(None)))
            and isinstance(self.user_display_name, (str, type(None)))
            and isinstance(self.hmac_secret, bool)
            and isinstance(self._creation_time, (int, type(None)))
            and isinstance(self.id, (bytes, bytearray))
        )

    def app_name(self) -> str:
        return self.rp_id

    def account_name(self) -> Optional[str]:
        from ubinascii import hexlify

        if self.user_name:
            return self.user_name
        elif self.user_display_name:
            return self.user_display_name
        elif self.user_id:
            return hexlify(self.user_id).decode()
        else:
            return None

    def private_key(self) -> bytes:
        from apps.common import seed

        path = _FIDO_KEY_PATH + [
            HARDENED | i for i in ustruct.unpack("<4L", self.id[-16:])
        ]
        node = seed.derive_node_without_passphrase(path, "nist256p1")
        return node.private_key()

    def hmac_secret_key(self) -> Optional[bytes]:
        # Returns the symmetric key for the hmac-secret extension also known as CredRandom.

        if not self.hmac_secret:
            return None

        from apps.common import seed

        node = seed.derive_slip21_node_without_passphrase(
            _FIDO_HMAC_SECRET_KEY_PATH + [self.id]
        )
        return node.key()


class U2fCredential(Credential):
    def __init__(self) -> None:
        super().__init__()
        self.node = None  # type: Optional[bip32.HDNode]

    def __lt__(self, other: "Credential") -> bool:
        # Sort U2F credentials after FIDO2 credentials.
        if isinstance(other, Fido2Credential):
            return False

        # Sort U2F credentials lexicographically amongst each other.
        return self.id > other.id

    def private_key(self) -> bytes:
        if self.node is None:
            return b""
        return self.node.private_key()

    def generate_key_handle(self) -> None:
        from apps.common import seed

        # derivation path is m/U2F'/r'/r'/r'/r'/r'/r'/r'/r'
        path = [HARDENED | random.uniform(0xF0000000) for _ in range(0, 8)]
        nodepath = [_U2F_KEY_PATH] + path

        # prepare signing key from random path, compute decompressed public key
        self.node = seed.derive_node_without_passphrase(nodepath, "nist256p1")

        # first half of keyhandle is keypath
        keypath = ustruct.pack("<8L", *path)

        # second half of keyhandle is a hmac of rp_id_hash and keypath
        mac = hmac.Hmac(self.node.private_key(), self.rp_id_hash, hashlib.sha256)
        mac.update(keypath)

        self.id = keypath + mac.digest()

    def app_name(self) -> str:
        from ubinascii import hexlify
        from apps.webauthn import knownapps

        app_name = knownapps.knownapps.get(self.rp_id_hash, None)
        if app_name is None:
            app_name = "%s...%s" % (
                hexlify(self.rp_id_hash[:4]).decode(),
                hexlify(self.rp_id_hash[-4:]).decode(),
            )
        return app_name

    @staticmethod
    def from_key_handle(
        key_handle: bytes, rp_id_hash: bytes
    ) -> Optional["U2fCredential"]:
        # check the keyHandle and generate the signing key
        node = U2fCredential._node_from_key_handle(rp_id_hash, key_handle, "<8L")
        if node is None:
            # prior to firmware version 2.0.8, keypath was serialized in a
            # big-endian manner, instead of little endian, like in trezor-mcu.
            # try to parse it as big-endian now and check the HMAC.
            node = U2fCredential._node_from_key_handle(rp_id_hash, key_handle, ">8L")
        if node is None:
            # specific error logged in msg_authenticate_genkey
            return None

        cred = U2fCredential()
        cred.id = key_handle
        cred.rp_id_hash = rp_id_hash
        cred.node = node
        return cred

    @staticmethod
    def _node_from_key_handle(
        rp_id_hash: bytes, keyhandle: bytes, pathformat: str
    ) -> Optional[bip32.HDNode]:
        from apps.common import seed

        # unpack the keypath from the first half of keyhandle
        keypath = keyhandle[:32]
        path = ustruct.unpack(pathformat, keypath)

        # check high bit for hardened keys
        for i in path:
            if not i & HARDENED:
                if __debug__:
                    log.warning(__name__, "invalid key path")
                return None

        # derive the signing key
        nodepath = [_U2F_KEY_PATH] + list(path)
        node = seed.derive_node_without_passphrase(nodepath, "nist256p1")

        # second half of keyhandle is a hmac of rp_id_hash and keypath
        mac = hmac.Hmac(node.private_key(), rp_id_hash, hashlib.sha256)
        mac.update(keypath)

        # verify the hmac
        if mac.digest() != keyhandle[32:]:
            if __debug__:
                log.warning(__name__, "invalid key handle")
            return None

        return node
