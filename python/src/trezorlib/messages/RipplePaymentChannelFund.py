# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RipplePaymentChannelFund(p.MessageType):

    def __init__(
        self,
        channel: str = None,
        amount: int = None,
        expiration: int = None,
    ) -> None:
        self.channel = channel
        self.amount = amount
        self.expiration = expiration

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('channel', p.UnicodeType, 0),
            2: ('amount', p.UVarintType, 0),
            3: ('expiration', p.UVarintType, 0),
        }
