# ChromaGlyph Format Specification – v1 (cg1)

## Overview

A **ChromaGlyph** is a compact, portable representation of a colour palette plus
optional metadata and per-colour annotations. The format is designed to be:

- **Human-inspectable** – the decoded payload is plain JSON.
- **URL-safe** – the token uses base64url encoding with no padding characters.
- **Versioned** – the `v` field and the `CG1:` prefix allow future format evolution.
- **Compact** – field names in the wire payload are abbreviated to minimise token length.

---

## Token Structure

```
CG1:<base64url(JSON payload)>
```

| Component      | Description                                                  |
|----------------|--------------------------------------------------------------|
| `CG1:`         | Literal prefix; identifies the format family and version.    |
| `<base64url>`  | RFC 4648 §5 base64url encoding of the JSON payload (UTF-8).  |

Tokens MUST start with the prefix `CG1:`. Any other prefix is an error.

---

## JSON Payload (Wire Format)

Field names are abbreviated to keep tokens short.

```json
{
  "v":  "cg1",
  "id": "<string>",
  "ts": "<ISO-8601 datetime>",
  "au": "<optional string>",
  "t":  ["<optional tag>", "..."],
  "p": [
    { "h": "#RRGGBB", "l": "<optional label>", "a": "<optional annotation>" },
    "..."
  ]
}
```

### Fields

| Field | Full name   | Type             | Required | Description                                          |
|-------|-------------|------------------|----------|------------------------------------------------------|
| `v`   | version     | `string`         | ✅        | Format version. Always `"cg1"` for this spec.        |
| `id`  | identifier  | `string`         | ✅        | Unique glyph ID (UUID v4 recommended).               |
| `ts`  | timestamp   | `string`         | ✅        | ISO-8601 UTC creation datetime.                      |
| `au`  | author      | `string`         | ❌        | Author name or identifier.                           |
| `t`   | tags        | `string[]`       | ❌        | Free-form tags for search / categorisation.          |
| `p`   | palette     | `PaletteEntry[]` | ✅        | Ordered colour entries (1–16).                       |

### Palette Entry Fields

| Field | Full name   | Type     | Required | Description                                    |
|-------|-------------|----------|----------|------------------------------------------------|
| `h`   | hex         | `string` | ✅        | CSS hex colour: `#RGB` or `#RRGGBB`.           |
| `l`   | label       | `string` | ❌        | Human-readable colour name.                    |
| `a`   | annotation  | `string` | ❌        | Freeform usage note or mood tag.               |

---

## Constraints

| Rule                                   | Detail                                                     |
|----------------------------------------|------------------------------------------------------------|
| Palette size                           | Minimum 1, maximum 16 entries.                             |
| Hex format                             | Must match `/^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/`.      |
| `id` uniqueness                        | Callers are responsible for uniqueness (UUIDs recommended).|
| `ts` format                            | Must be a valid ISO-8601 datetime string.                  |
| Optional fields                        | MUST be omitted (not null) when not set to keep tokens compact. |

---

## Encoding Algorithm

1. Build a `WirePayload` object with abbreviated keys.
2. Omit optional fields (`au`, `t`, `l`, `a`) when they are `undefined`.
3. Serialise to JSON (no extra whitespace).
4. Encode the UTF-8 bytes as base64url (RFC 4648 §5, no padding).
5. Prepend `CG1:`.

## Decoding Algorithm

1. Assert the token starts with `CG1:`.
2. Strip the prefix; decode the base64url segment as UTF-8 bytes.
3. Parse as JSON.
4. Assert `v === "cg1"`.
5. Assert required fields (`id`, `ts`, `p`) are present and non-empty.
6. Return the fully-resolved `Glyph` object with expanded field names.

---

## Future Versions

A future breaking change (e.g. new required field, changed encoding) MUST:

1. Introduce a new format version string (e.g. `cg2`).
2. Change the token prefix accordingly (e.g. `CG2:`).
3. Bump the package `MAJOR` version.
4. Maintain backward-compatible decode support for `cg1` tokens.
