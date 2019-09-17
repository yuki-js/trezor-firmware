from trezor import ui

if False:
    from typing import Any, Optional


def pin_to_int(pin: str) -> int:
    return int("1" + pin)


_previous_progress = None  # type: Optional[int]
_previous_seconds = None  # type: Optional[int]
keepalive_callback = None  # type: Any


def show_pin_timeout(seconds: int, progress: int, message: str) -> bool:
    global _previous_progress
    global _previous_seconds

    if callable(keepalive_callback):
        keepalive_callback()

    if progress == 0:
        if progress != _previous_progress:
            # avoid overdraw in case of repeated progress calls
            ui.display.clear()
            _previous_seconds = None
        ui.display.text_center(
            ui.WIDTH // 2, 37, message, ui.BOLD, ui.FG, ui.BG, ui.WIDTH
        )
    ui.display.loader(progress, False, 0, ui.FG, ui.BG)

    if seconds != _previous_seconds:
        if seconds == 0:
            remaining = "Done"
        elif seconds == 1:
            remaining = "1 second left"
        else:
            remaining = "%d seconds left" % seconds
        ui.display.text_center(
            ui.WIDTH // 2, ui.HEIGHT - 22, remaining, ui.BOLD, ui.FG, ui.BG, ui.WIDTH
        )
        _previous_seconds = seconds

    ui.display.refresh()
    _previous_progress = progress
    return False
