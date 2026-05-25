from Dev.ChromaEmitters.src.chromaemitters.tapo.tapo_device import TapoLedDevice


def test_tapo_device_uses_injected_transport():
    calls = []

    def transport(endpoint, payload):
        calls.append((endpoint, payload))
        return {"ok": True}

    device = TapoLedDevice("192.168.1.10", auth_token="abc", transport=transport)
    result = device.set_rgb([1, 2, 3], transition_ms=15)

    assert result["sent"] is True
    assert calls[0][0].startswith("http://192.168.1.10/")
    assert calls[0][1]["rgb"] == [1, 2, 3]
