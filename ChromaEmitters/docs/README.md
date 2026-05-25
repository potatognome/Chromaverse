# ChromaEmitters

ChromaEmitters is the device output layer for Chromaspace.

Initial emitter:
- Tapo LED output via a registry-discoverable emitter class.

It loads `config/ChromaEmitters_CONFIG.json`, merges deterministic
overrides from `config/emitters.d/`, and registers emitters through
the Chromacore registry.
