from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import format_amount
from trezor.ui.scroll import Paginated

from . import helpers

from apps.common.confirm import require_confirm, require_hold_to_confirm
from apps.common.layout import split_address


async def require_confirm_fee(ctx, fee):
    text = Text("Confirm fee", ui.ICON_SEND, ui.GREEN)
    text.normal("Transaction fee:")
    text.bold(format_amount(fee, helpers.DIVISIBILITY) + " XRP")
    await require_confirm(ctx, text, ButtonRequestType.ConfirmOutput)


async def require_confirm_destination_tag(ctx, tag):
    text = Text("Confirm tag", ui.ICON_SEND, ui.GREEN)
    text.normal("Destination tag:")
    text.bold(str(tag))
    await require_confirm(ctx, text, ButtonRequestType.ConfirmOutput)


async def require_confirm_tx(ctx, to, value):

    text = Text("Confirm sending", ui.ICON_SEND, ui.GREEN)
    text.bold(format_amount(value, helpers.DIVISIBILITY) + " XRP")
    text.normal("to")
    text.mono(*split_address(to))
    return await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_multisig(ctx, account):

    text = Text("Confirm signing", ui.ICON_SEND, ui.GREEN)
    text.normal("for multisig account:")
    text.mono(*split_address(account))
    await require_confirm(ctx, text, ButtonRequestType.ConfirmOutput)


async def require_confirm_signer_list_set(ctx, quorum, signerEntries):
    pages = []
    for i, entry in enumerate(signerEntries):
        text = Text("Confirm signers #%d" % i, ui.ICON_SEND, ui.GREEN)
        text.normal("Quorum: %d" % quorum)
        text.mono(*split_address(entry.account))
        text.normal("Weight: %d" % entry.signer_weight)
        pages.append(text)
    paginated = Paginated(pages)
    await require_hold_to_confirm(ctx, paginated,
                                  ButtonRequestType.ConfirmOutput)
