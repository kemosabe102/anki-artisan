# CLAUDE.md

**Project**: Anki Artisan | **Version**: 1.0.0 | **Python**: 3.13+

---

## Quick Links

| Resource | Path |
|----------|------|
| Project Spec | `docs/italian-anki-generator-spec.md` |
| ElevenLabs Integration | `docs/elevenlabs-integration.md` |
| Development Guide | `docs/development.md` |
| README | `README.md` |

---

## Project Overview

**Anki Artisan** is a Python CLI tool that generates Anki flashcard decks with neural TTS audio.

**Pipeline**: CSV vocabulary → ElevenLabs TTS → Anki deck (.apkg)

**Key Features**:
- Multi-language support (Italian, Spanish, French)
- Neural TTS via ElevenLabs API
- Smart audio caching to reduce API costs
- Type-safe with Pydantic validation

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13+ |
| Anki Generation | genanki |
| TTS | ElevenLabs API |
| Validation | Pydantic v2 |
| HTTP | requests |
| Testing | pytest |
| Package Manager | uv |

---

## Project Structure

```
anki-artisan/
├── src/anki_artisan/     # Core implementation
│   ├── cli.py            # CLI entry point
│   ├── models.py         # Pydantic data models
│   ├── csv_reader.py     # CSV parsing/validation
│   ├── tts_service.py    # ElevenLabs integration
│   └── deck_builder.py   # genanki deck generation
├── languages/            # Language configurations
│   └── italian/          # Italian vocab & config
├── templates/            # Card HTML templates
├── cache/                # Audio cache (gitignored)
├── tests/                # Unit tests
└── docs/                 # Documentation
```

---

## Code Style

| Element | Convention |
|---------|------------|
| Classes | `PascalCase` |
| Functions/Variables | `snake_case` |
| Constants | `UPPER_SNAKE_CASE` |
| Private | `_leading_underscore` |

**Requirements**: Type hints on all functions | Docstrings on public methods

---

## Commands

```bash
# Run tests
pytest

# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Generate deck
anki-artisan generate --language italian --output deck.apkg
```

---

## Environment Setup

```bash
# Required
ELEVENLABS_API_KEY=your_api_key_here

# Optional (set after listing voices)
ELEVENLABS_VOICE_ID=voice_id_here
```

---

## Git Safety

**NEVER run destructive commands**:
```bash
git checkout <file>     # Discards changes
git restore <file>      # Discards changes  
git reset --hard        # Wipes working directory
git clean -fd           # Deletes untracked files
```

**Safe alternatives**:
```bash
git reset HEAD          # Unstages (preserves working directory)
git reset --soft        # Moves HEAD (preserves staging + working)
```

---

## Tool Preferences

**ALWAYS prefer built-in tools over bash**:
- ✅ `Glob("**/*.py")` | ❌ `find . -name "*.py"`
- ✅ `Grep(pattern)` | ❌ `grep -r pattern`
- ✅ `Read("file.py")` | ❌ `cat file.py`

---

## API Key Handling

- Store in `.env` file (gitignored)
- Never commit credentials
- Use `.env.example` as template

---

## Development Checklist

**Before implementing**:
- [ ] Check `docs/italian-anki-generator-spec.md` for requirements
- [ ] Review existing code patterns
- [ ] Consider edge cases

**Before committing**:
- [ ] Tests pass (`pytest`)
- [ ] Code formatted (`black`, `ruff`)
- [ ] No hardcoded credentials
- [ ] Docs updated if needed
