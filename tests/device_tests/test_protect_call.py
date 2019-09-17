# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import time

import pytest

from trezorlib import messages as proto
from trezorlib.exceptions import PinException

# FIXME TODO Add passphrase tests


@pytest.mark.skip_t2
class TestProtectCall:
    def _some_protected_call(self, client, button, pin, passphrase):
        # This method perform any call which have protection in the device
        res = client.ping(
            "random data",
            button_protection=button,
            pin_protection=pin,
            passphrase_protection=passphrase,
        )
        assert res == "random data"

    @pytest.mark.setup_client(pin="1234", passphrase=True)
    def test_expected_responses(self, client):
        # This is low-level test of set_expected_responses()
        # feature of debugging client

        with pytest.raises(AssertionError), client:
            # Scenario 1 - Received unexpected message
            client.set_expected_responses([])
            self._some_protected_call(client, True, True, True)

        with pytest.raises(AssertionError), client:
            # Scenario 2 - Received other than expected message
            client.set_expected_responses([proto.Success()])
            self._some_protected_call(client, True, True, True)

        with pytest.raises(AssertionError), client:
            # Scenario 3 - Not received expected message
            client.set_expected_responses(
                [proto.ButtonRequest(), proto.Success(), proto.Success()]
            )  # This is expected, but not received
            self._some_protected_call(client, True, False, False)

        with pytest.raises(AssertionError), client:
            # Scenario 4 - Received what expected
            client.set_expected_responses(
                [
                    proto.ButtonRequest(),
                    proto.PinMatrixRequest(),
                    proto.PassphraseRequest(),
                    proto.Success(message="random data"),
                ]
            )
            self._some_protected_call(client, True, True, True)

        with pytest.raises(AssertionError), client:
            # Scenario 5 - Failed message by field filter
            client.set_expected_responses(
                [proto.ButtonRequest(), proto.Success(message="wrong data")]
            )
            self._some_protected_call(client, True, True, True)

    def test_no_protection(self, client):
        with client:
            assert client.debug.read_pin()[0] is None
            client.set_expected_responses([proto.Success()])
            self._some_protected_call(client, False, True, True)

    @pytest.mark.setup_client(pin="1234", passphrase=True)
    def test_pin(self, client):
        with client:
            assert client.debug.read_pin()[0] == "1234"
            client.setup_debuglink(button=True, pin_correct=True)
            client.set_expected_responses(
                [proto.ButtonRequest(), proto.PinMatrixRequest(), proto.Success()]
            )
            self._some_protected_call(client, True, True, False)

    @pytest.mark.setup_client(pin="1234", passphrase=True)
    def test_incorrect_pin(self, client):
        client.setup_debuglink(button=True, pin_correct=False)
        with pytest.raises(PinException):
            self._some_protected_call(client, False, True, False)

    @pytest.mark.setup_client(pin="1234", passphrase=True)
    def test_cancelled_pin(self, client):
        client.setup_debuglink(button=True, pin_correct=False)  # PIN cancel
        with pytest.raises(PinException):
            self._some_protected_call(client, False, True, False)

    @pytest.mark.setup_client(pin="1234", passphrase=True)
    def test_exponential_backoff_with_reboot(self, client):
        client.setup_debuglink(button=True, pin_correct=False)

        def test_backoff(attempts, start):
            if attempts <= 1:
                expected = 0
            else:
                expected = (2 ** (attempts - 1)) - 1
            got = round(time.time() - start, 2)

            msg = "Pin delay expected to be at least %s seconds, got %s" % (
                expected,
                got,
            )
            print(msg)
            assert got >= expected

        for attempt in range(1, 4):
            start = time.time()
            with pytest.raises(PinException):
                self._some_protected_call(client, False, True, False)
            test_backoff(attempt, start)
