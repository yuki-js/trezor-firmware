# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class CosiCommit(p.MessageType):
    MESSAGE_WIRE_TYPE = 71

    def __init__(
        self,
        address_n: List[int] = None,
        data: bytes = None,
    ) -> None:
        self.address_n = address_n if address_n is not None else []
        self.data = data

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
            2: ('data', p.BytesType, 0),
        }