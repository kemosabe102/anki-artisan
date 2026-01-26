# Deck Generation Guide

This guide covers how to generate Anki flashcard decks with TTS audio using Anki Artisan.

---

## Quick Start

```bash
# Generate a deck
uv run anki-artisan generate --language italian --level a1_01_saluti_presentazioni

# Dry run (validate only, no API calls)
uv run anki-artisan generate --language italian --level a1 --dry-run

# Cache audio only (skip deck building)
uv run anki-artisan generate --language italian --level a1 --cache-only
```

---

## CSV File Format

Vocabulary files are stored in `languages/{language}/` with the naming pattern `{level}.csv`.

### Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| `word` | Target language word | `ciao` |
| `translation` | English translation | `hello/goodbye (informal)` |
| `phrase` | Example phrase (≤6 words) | `Ciao! Come stai?` |
| `phrase_translation` | English phrase translation | `Hello! How are you?` |
| `part_of_speech` | Grammar category | `interjection` |
| `gender` | Grammatical gender | `m`, `f`, `n/a` |
| `tags` | Space-separated tags | `greetings informal` |

### Part of Speech Values

`noun`, `verb`, `adjective`, `adverb`, `preposition`, `conjunction`, `pronoun`, `interjection`, `phrase`

### Gender Values

| Value | Meaning |
|-------|---------|
| `m` | Masculine |
| `f` | Feminine |
| `n` | Neuter (German) |
| `mf` | Dual gender |
| `c` | Common gender (Swedish/Danish) |
| `n/a` | Not applicable |

---

## Adding a New Language


### 1. Create Language Directory

```bash
mkdir languages/{language}
```

### 2. Create config.yaml

Copy and adapt from an existing language config:

```yaml
language_code: "es"           # ISO code
language_name: "Spanish"      # English name
native_name: "Español"        # Native name

elevenlabs:
  voice_id: "voice_id_here"   # From ElevenLabs
  voice_name: "Voice Name"
  model_id: "eleven_multilingual_v2"
  
  voice_settings:
    stability: 0.7
    similarity_boost: 0.8
    style: 0.0
    use_speaker_boost: true
    speed: 0.9
    leading_pause_seconds: 0.3  # Prevents audio truncation

deck:
  name_template: "Spanish {level} Vocabulary"
  deck_id_base: 2059400200    # Unique per language
  model_id_base: 1607390200   # Unique per language

features:
  has_gender: true
  has_articles: true
  gender_types: ["m", "f"]
```

### 3. Find Voice IDs

```bash
uv run anki-artisan list-voices
```

Look for voices with:
- Native accent for your target language
- Clear pronunciation (education/e-learning tags)
- Consistent delivery style

### 4. Create Vocabulary CSVs

Place CSV files in `languages/{language}/` directory.

---

## CLI Reference


### Generate Command

```bash
uv run anki-artisan generate [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--language`, `-l` | Language to generate (required) | - |
| `--level` | CSV filename without extension | `a1` |
| `--output`, `-o` | Output path for .apkg file | `output/{language}_{level}.apkg` |
| `--voice-id` | Override default voice ID | Config default |
| `--dry-run` | Validate only, no API calls | `false` |
| `--cache-only` | Generate audio cache, skip deck | `false` |

### Other Commands

```bash
# List available languages
uv run anki-artisan list-languages

# List ElevenLabs voices
uv run anki-artisan list-voices
```

---

## Audio Caching

Audio files are cached in `cache/{language_code}/{voice_id}/{hash}.mp3`.

- Cache key is based on original text (not SSML)
- Cached audio is reused across deck generations
- To regenerate audio, delete the relevant cache directory

### Cache Location

```
cache/
├── it/                       # Italian
│   └── uV2Bhcm1HwmAqPqkbjfl/ # Voice ID
│       ├── a1b2c3d4e5f6.mp3
│       └── ...
└── es/                       # Spanish
    └── 15bJsujCI3tcDWeoZsQP/
        └── ...
```

---

## ElevenLabs Credits


Each character sent to ElevenLabs counts against your quota. The CLI reports characters used after generation.

**Typical usage per deck:**
- ~40-50 vocabulary items ≈ 1,000-1,500 characters
- Each item generates 2 audio files (word + phrase)

**Cost optimization:**
- Audio caching prevents duplicate API calls
- Use `--dry-run` to validate before generating
- Use `--cache-only` to pre-generate audio across sessions

---

## Language-Specific Notes

### Italian
- Uses `eleven_multilingual_v2` model
- Default voice: Sara (female, e-learning optimized)
- Test consonant clusters: `gli`, `gn`, `sc`

### Spanish
- **Latin American** (default): Uses seseo (c/z = "s" sound)
- **Castilian** (Spain): Uses distinción (c/z = "th" sound)
- Default voice: Santiago (Mexican accent)
- For Castilian, switch to Gabriel Reyes or Jacobo Montoro
- Regional pronoun differences:
  - Latin America: `ustedes` for plural "you"
  - Spain: `vosotros` for informal plural "you"

---

## Troubleshooting

### Audio Truncation at Start
The `leading_pause_seconds` setting adds an SSML break tag before each phrase. Default is `0.3` seconds.

### Voice Not Found
Run `uv run anki-artisan list-voices` to get current voice IDs.

### CSV Validation Errors
- Ensure all required columns exist
- Check `part_of_speech` values match enum
- Phrases must be ≤6 words
