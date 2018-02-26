# Automatically generated by pb2py
import protobuf as p


class EthereumGetAddress(p.MessageType):
    FIELDS = {
        1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
        2: ('show_display', p.BoolType, 0),
    }
    MESSAGE_WIRE_TYPE = 56

    def __init__(
        self,
        address_n: list = [],
        show_display: bool = None,
        **kwargs,
    ):
        self.address_n = address_n
        self.show_display = show_display
        p.MessageType.__init__(self, **kwargs)