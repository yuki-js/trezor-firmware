# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class RippleEscrowCancel(p.MessageType):

    def __init__(
        self,
        owner: str = None,
        offer_sequence: int = None,
    ) -> None:
        self.owner = owner
        self.offer_sequence = offer_sequence

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('owner', p.UnicodeType, 0),
            2: ('offer_sequence', p.UVarintType, 0),
        }
