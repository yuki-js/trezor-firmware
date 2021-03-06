# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RipplePaymentChannelClaim(p.MessageType):

    def __init__(
        self,
        channel: str = None,
        balance: int = None,
        amount: int = None,
        signature: str = None,
        public_key: str = None,
    ) -> None:
        self.channel = channel
        self.balance = balance
        self.amount = amount
        self.signature = signature
        self.public_key = public_key

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('channel', p.UnicodeType, 0),
            2: ('balance', p.UVarintType, 0),
            4: ('amount', p.UVarintType, 0),
            5: ('signature', p.UnicodeType, 0),
            6: ('public_key', p.UnicodeType, 0),
        }
