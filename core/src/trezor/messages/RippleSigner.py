# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleSigner(p.MessageType):

    def __init__(
        self,
        account: str = None,
        txn_signature: str = None,
        signing_pub_key: str = None,
    ) -> None:
        self.account = account
        self.txn_signature = txn_signature
        self.signing_pub_key = signing_pub_key

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('account', p.UnicodeType, 0),
            2: ('txn_signature', p.UnicodeType, 0),
            3: ('signing_pub_key', p.UnicodeType, 0),
        }
