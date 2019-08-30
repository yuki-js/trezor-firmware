from trezor import config, ui, wire
from trezor.messages import ButtonRequestType
from trezor.messages.ButtonAck import ButtonAck
from trezor.messages.ButtonRequest import ButtonRequest
from trezor.messages.Success import Success
from trezor.pin import pin_to_int
from trezor.ui.popup import Popup
from trezor.ui.text import Text

from apps.common.confirm import require_confirm
from apps.common.request_pin import PinCancelled, request_pin
from apps.common.sd_salt import request_sd_salt
from apps.common.storage import device

if False:
    from typing import Any, Optional, Tuple
    from trezor.messages.ChangePin import ChangePin


async def change_pin(ctx: wire.Context, msg: ChangePin) -> Success:
    # confirm that user wants to change the pin
    await require_confirm_change_pin(ctx, msg)

    # get old pin
    curpin, salt = await request_pin_and_sd_salt(ctx, "Enter old PIN")

    # if changing pin, pre-check the entered pin before getting new pin
    if curpin and not msg.remove:
        if not config.check_pin(pin_to_int(curpin), salt):
            raise wire.PinInvalid("PIN invalid")

    # get new pin
    if not msg.remove:
        newpin = await request_pin_confirm(ctx)
    else:
        newpin = ""

    # write into storage
    if not config.change_pin(pin_to_int(curpin), pin_to_int(newpin), salt, salt):
        raise wire.PinInvalid("PIN invalid")

    if newpin:
        return Success(message="PIN changed")
    else:
        return Success(message="PIN removed")


def require_confirm_change_pin(ctx: wire.Context, msg: ChangePin) -> None:
    has_pin = config.has_pin()

    if msg.remove and has_pin:  # removing pin
        text = Text("Remove PIN", ui.ICON_CONFIG)
        text.normal("Do you really want to")
        text.bold("disable PIN protection?")
        return require_confirm(ctx, text)

    if not msg.remove and has_pin:  # changing pin
        text = Text("Change PIN", ui.ICON_CONFIG)
        text.normal("Do you really want to")
        text.bold("change the current PIN?")
        return require_confirm(ctx, text)

    if not msg.remove and not has_pin:  # setting new pin
        text = Text("Enable PIN", ui.ICON_CONFIG)
        text.normal("Do you really want to")
        text.bold("enable PIN protection?")
        return require_confirm(ctx, text)


async def request_pin_confirm(ctx: wire.Context, *args: Any, **kwargs: Any) -> str:
    while True:
        pin1 = await request_pin_ack(ctx, "Enter new PIN", *args, **kwargs)
        pin2 = await request_pin_ack(ctx, "Re-enter new PIN", *args, **kwargs)
        if pin1 == pin2:
            return pin1
        await pin_mismatch()


async def request_pin_and_sd_salt(
    ctx: wire.Context, prompt: str = "Enter your PIN", allow_cancel: bool = True
) -> Tuple[str, Optional[bytearray]]:
    salt_auth_key = device.get_sd_salt_auth_key()
    if salt_auth_key is not None:
        salt = await request_sd_salt(ctx, salt_auth_key)  # type: Optional[bytearray]
    else:
        salt = None

    if config.has_pin():
        pin = await request_pin_ack(ctx, prompt, config.get_pin_rem(), allow_cancel)
    else:
        pin = ""

    return pin, salt


async def request_pin_ack(ctx: wire.Context, *args: Any, **kwargs: Any) -> str:
    try:
        await ctx.call(ButtonRequest(code=ButtonRequestType.Other), ButtonAck)
        return await ctx.wait(request_pin(*args, **kwargs))
    except PinCancelled:
        raise wire.ActionCancelled("Cancelled")


async def pin_mismatch() -> None:
    text = Text("PIN mismatch", ui.ICON_WRONG, ui.RED)
    text.normal("The PINs you entered", "do not match.")
    text.normal("")
    text.normal("Please try again.")
    popup = Popup(text, 3000)  # show for 3 seconds
    await popup
