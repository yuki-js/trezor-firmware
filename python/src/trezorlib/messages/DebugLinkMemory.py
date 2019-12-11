# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class DebugLinkMemory(p.MessageType):
    MESSAGE_WIRE_TYPE = 111

    def __init__(
        self,
        memory: bytes = None,
    ) -> None:
        self.memory = memory

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('memory', p.BytesType, 0),
        }
