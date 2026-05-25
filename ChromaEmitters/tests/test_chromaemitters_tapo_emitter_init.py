from Dev.ChromaEmitters.src.chromaemitters.tapo.tapo_emitter import TapoEmitter


def test_tapo_emitter_initializes_from_config():
    config = {
        "emitters": {
            "tapo_led": {
                "enabled": True,
                "device_ip": "192.168.1.11",
                "transition_ms": 25,
            }
        }
    }
    emitter = TapoEmitter(config=config)
    assert emitter.enabled is True
    assert emitter.transition_ms == 25
