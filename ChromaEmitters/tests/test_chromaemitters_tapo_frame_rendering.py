from Dev.ChromaEmitters.src.chromaemitters.tapo.tapo_emitter import TapoEmitter


class _FakeDevice:
    def __init__(self):
        self.calls = []

    def set_rgb(self, rgb, transition_ms):
        self.calls.append((rgb, transition_ms))
        return {"ok": True}


def test_tapo_emitter_renders_frame_with_rgb():
    config = {
        "emitters": {
            "tapo_led": {
                "enabled": True,
                "device_ip": "192.168.1.12",
                "transition_ms": 40,
            }
        }
    }
    device = _FakeDevice()
    emitter = TapoEmitter(config=config, device=device)

    result = emitter.render({"rgb": [100, 120, 140]})
    assert result["emitted"] is True
    assert device.calls == [([100, 120, 140], 40)]
