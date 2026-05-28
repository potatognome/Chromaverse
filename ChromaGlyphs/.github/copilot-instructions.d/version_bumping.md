# Version Bumping – ChromaGlyphs

- Version lives in `package.json` → `"version"` and `config/CHROMAGLYPHS_CONFIG.json` → `INFO.VERSION`.
- Bump both fields together in the same commit.
- Follow Semantic Versioning: MAJOR for breaking API/format changes, MINOR for additive features, PATCH for fixes.
- Breaking token-format changes (e.g. `cg1` → `cg2`) are always a MAJOR bump.
- Add a changelog entry in `CHANGELOG.md` for every version bump.
