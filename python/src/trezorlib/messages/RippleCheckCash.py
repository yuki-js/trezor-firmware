# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .RippleIssuedAmount import RippleIssuedAmount

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleCheckCash(p.MessageType):

    def __init__(
        self,
        check_id: str = None,
        amount: int = None,
        issued_amount: RippleIssuedAmount = None,
        deliver_min: int = None,
        issued_deliver_min: RippleIssuedAmount = None,
    ) -> None:
        self.check_id = check_id
        self.amount = amount
        self.issued_amount = issued_amount
        self.deliver_min = deliver_min
        self.issued_deliver_min = issued_deliver_min

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('check_id', p.UnicodeType, 0),
            2: ('amount', p.UVarintType, 0),
            3: ('issued_amount', RippleIssuedAmount, 0),
            4: ('deliver_min', p.UVarintType, 0),
            5: ('issued_deliver_min', RippleIssuedAmount, 0),
        }
