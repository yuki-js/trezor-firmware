import pytest

from trezorlib import messages

from .conftest import setup_client


def test_same_features(client):
    f0 = client.features
    f1 = client.call(messages.Initialize())
    assert f0 == f1


def test_features_output(client):
    features = client.call(messages.Initialize())
    assert features.vendor == "trezor.io"
    assert features.pin_protection is False
    assert features.passphrase_protection is False
    assert features.initialized is False


def test_features_capabilities(client):
    features = client.call(messages.Initialize())
    for capability in (
        messages.Feature.Bitcoin,
        messages.Feature.Crypto,
        messages.Feature.Shamir,
        messages.Feature.ShamirGroups,
    ):
        assert capability in features.features


@pytest.mark.altcoin  # do not run this test for Bitcoin-only fw
def test_features_all_capabilities(client):
    features = client.call(messages.Initialize())
    assert features.features == [
        messages.Feature.Bitcoin,
        messages.Feature.Bitcoin_like,
        messages.Feature.Binance,
        messages.Feature.Cardano,
        messages.Feature.Crypto,
        messages.Feature.EOS,
        messages.Feature.Ethereum,
        messages.Feature.Lisk,
        messages.Feature.Monero,
        messages.Feature.NEM,
        messages.Feature.Ripple,
        messages.Feature.Stellar,
        messages.Feature.Tezos,
        messages.Feature.U2F,
        messages.Feature.Shamir,
        messages.Feature.ShamirGroups,
    ]


@setup_client(mnemonic=" ".join(["all"] * 12), pin="123", passphrase=True)
def test_pin_passphrase(client):
    features = client.call(messages.Initialize())
    assert features.passphrase_protection is True
    assert features.pin_protection is True
