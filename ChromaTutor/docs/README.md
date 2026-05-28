# ChromaTutor

A Chroma-native instructional LMS and procedural interpreter for the Prismata ecosystem

**Version:** 0.1.0
**Author:** Daniel Austin <the.potato.gnome@gmail.com>

ChromaTutor is the instructional intelligence of Prismata. It reads procedural
step-by-step instructions, interprets them semantically, lint-checks them,
restructures them into teachable sequences, generates ChromaGlyph-ready symbolic
meaning, and uses the tUilKit canvas as a visual substrate for training-ready
instructional synthesis.


## Features

- Procedural instruction ingestion and interpretation
- Instruction linting and ambiguity detection
- Structured action sequencing for teachable workflows
- ChromaGlyph-oriented symbolic reconstruction
- tUilKit canvas-backed visual instruction synthesis
- CLI, API, and compositor-facing execution surface

## Classification

- Project type: tenant
- Role: instructional LMS
- Core function: procedural interpreter
- Neural analog: Premotor Cortex
- Interfaces: cli, api, compositor

## Ecosystem Placement

ChromaTutor bridges language into action. It sits between semantic retrieval,
symbolic encoding, sequencing, and visual composition in the Chroma family.

## Installation

### Development Installation

For development, install in editable mode:

```bash
cd ChromaTutor
pip install -e .
```

This allows you to:
- Run the project as a module: `python -m ChromaTutor`
- Use the console script: `chromatutor`
- Make changes to the code without reinstalling

### Standard Installation

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Using the root-level runner (no installation needed)

```bash
python ChromaTutor.py
```

### Option 2: As a module (after pip install -e .)

```bash
python -m ChromaTutor
```

### Option 3: Using console script (after pip install -e .)

```bash
chromatutor
```
