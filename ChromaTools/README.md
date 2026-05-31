# ChromaTools

ChromaTools is the Chromaverse utility hub: a standalone Python subproject with a
menu-driven CLI for inspecting shared configuration, browsing the Chroma app
catalogue, and launching supported tools from one place.

## Features

- Menu-based CLI scaffold with a tUilKit-compatible logging/config pattern
- Central app catalogue for Chromaspace, Chromagrams, ChromaGlyphs, ChromaTutor,
  ChromaEmitters, and ChromaSchemes
- Config-driven access metadata for entry points, project paths, and app configs
- Safe launch flow that only runs commands explicitly configured for an app

## Installation

```bash
pip install -e .
```

## Usage

```bash
chromatools
```

## Development

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

