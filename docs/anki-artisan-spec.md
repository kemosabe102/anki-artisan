# Anki Artisan - Technical Specification

## Project Overview

### Purpose
Build a Python CLI tool that generates Anki flashcard decks with high-quality neural TTS audio for language learning. Supports multiple target languages with vocabulary organized by CEFR proficiency levels (A1, A2, B1, B2).

### Problem Statement
- Creating Anki cards with audio is tedious and manual
- ElevenLabs has excellent multilingual voices but no direct Anki integration
- Need consistent, high-quality pronunciation for vocabulary at different proficiency levels
- Must control API costs while building vocabulary incrementally

### Scope
- **Phase 1 (Current):** 5-10 word Italian A1 validation deck
- **Phase 2:** Complete Italian A1 deck (~50 words)
- **Phase 3:** Additional languages (Spanish, French, German)
- **Future:** B1/B2 levels, custom vocabulary lists

### Design Principles
| Principle | Implementation |
|-----------|----------------|
| Multi-language first | Language-agnostic core with per-language configurations |
| CEFR organization | Vocabulary grouped by A1, A2, B1, B2 levels |
| Optimize API usage | Phrases ≤6 words, cache all audio locally |
| Quality audio | Clear enunciation, appropriate voice per language |
| Validation-first | Small test runs before full generation |

---

## Tech Stack

### Core Technologies
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.10+ | Primary development language |
| Anki Generation | genanki | >=1.13.0 | Creates .apkg files programmatically |
| TTS | elevenlabs (SDK) | >=1.0.0 | Official Python SDK for ElevenLabs API |
| Data Validation | pydantic | >=2.5.0 | Type-safe data models, input validation |
| Configuration | pydantic-settings | >=2.0.0 | Environment-based configuration |
| YAML Parsing | pyyaml | >=6.0.0 | Read language config files |
| CLI Interface | argparse | stdlib | Command-line argument handling |
| Environment | python-dotenv | >=1.0.0 | Load .env files |

### Dependencies (pyproject.toml)
```toml
dependencies = [
    "genanki>=1.13.0",
    "elevenlabs>=1.0.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0.0",
]
```

---

## Project Structure

```
anki-artisan/
├── src/anki_artisan/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── config.py           # Pydantic settings, paths
│   ├── models.py           # Data models (VocabItem, etc.)
│   ├── csv_reader.py       # CSV parsing and validation
│   ├── tts_service.py      # ElevenLabs SDK wrapper with caching
│   └── deck_builder.py     # genanki deck generation
├── languages/
│   ├── _base/              # Reference concepts (documentation only)
│   │   ├── a1_concepts.md  # What A1 level should cover
│   │   └── a2_concepts.md
│   ├── italian/
│   │   ├── config.yaml     # Voice ID, language code, deck settings
│   │   ├── a1.csv          # A1 vocabulary
│   │   └── a2.csv
│   ├── spanish/
│   │   ├── config.yaml
│   │   └── a1.csv
│   └── french/
│       └── ...
├── templates/              # Card HTML/CSS templates
│   └── vocabulary.html
├── cache/                  # Generated audio (gitignored)
│   └── {language}/
│       └── {voice_id}/
├── output/                 # Generated .apkg files
├── tests/
├── docs/
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Multi-Language Architecture

### Language Configuration (languages/{language}/config.yaml)

```yaml
# languages/italian/config.yaml
language_code: "it"
language_name: "Italian"
native_name: "Italiano"

elevenlabs:
  # Sara - E-learning: Native Italian, designed for educational content
  voice_id: "uV2Bhcm1HwmAqPqkbjfl"
  voice_name: "Sara - E-learning"
  model_id: "eleven_multilingual_v2"
  
  # Settings optimized for flashcard consistency and beginner clarity
  voice_settings:
    stability: 0.7        # Higher = consistent pronunciation across cards
    similarity_boost: 0.8 # Strong voice adherence
    style: 0.0            # No expressive variation (predictable output)
    use_speaker_boost: true
    speed: 0.9            # Slightly slower for beginners

  # Alternative voices (all native Italian, education-optimized)
  alternative_voices:
    - voice_id: "wytO3xyllSDjJKHNkchr"
      name: "GianP - Edu"
      gender: "male"
    - voice_id: "oVJbgLwL0s5pk9e2U6QH"
      name: "Manuela"
      gender: "female"

deck:
  name_template: "{language} {level} Vocabulary"
  deck_id_base: 2059400000
  model_id_base: 1607390000

features:
  has_gender: true
  has_articles: true
  gender_types: ["m", "f"]

# Important pronunciation notes
pronunciation_notes:
  - "Always spell out numbers (write 'venti' not '20')"
  - "Test consonant clusters before bulk generation: gli, gn, sc"
```

### CEFR Level Concepts (languages/_base/)

The `_base/` folder contains markdown files documenting what each CEFR level should cover. These are reference documents, not used in generation:

```markdown
# A1 Concepts (Beginner)

## Categories
- Greetings and farewells
- Numbers 1-20
- Days of the week
- Basic colors
- Family members
- Common verbs (to be, to have, to go, to want, to eat)
- Basic adjectives (big, small, good, bad)
- Common nouns (house, water, food, person)
- Essential phrases (please, thank you, yes, no, excuse me)

## Target: ~50-100 words
```

Each language then implements these concepts with culturally appropriate, native-sounding vocabulary.

---

## Data Models

### CSV Schema (Language-Agnostic)

| Column | Required | Type | Description | Example |
|--------|----------|------|-------------|---------|
| `word` | ✅ | string | Word in target language (with article if applicable) | `la casa` |
| `translation` | ✅ | string | English translation | `the house` |
| `phrase` | ✅ | string | Example phrase in target language (≤6 words) | `La casa è bella.` |
| `phrase_translation` | ✅ | string | English phrase translation | `The house is beautiful.` |
| `part_of_speech` | ✅ | string | Grammar category | `noun` |
| `gender` | Optional | string | Grammatical gender (if applicable) | `f` |
| `tags` | Optional | string | Additional tags (space-separated) | `home places` |



### Pydantic Models (src/anki_artisan/models.py)

```python
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class PartOfSpeech(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    PRONOUN = "pronoun"
    INTERJECTION = "interjection"
    PHRASE = "phrase"  # For fixed expressions

class Gender(str, Enum):
    MASCULINE = "m"
    FEMININE = "f"
    NEUTER = "n"
    NOT_APPLICABLE = "n/a"

class VocabItem(BaseModel):
    """A single vocabulary item from the CSV."""
    word: str = Field(..., min_length=1)
    translation: str = Field(..., min_length=1)
    phrase: str = Field(..., min_length=1)
    phrase_translation: str = Field(..., min_length=1)
    part_of_speech: PartOfSpeech
    gender: Gender = Gender.NOT_APPLICABLE
    tags: str = ""
    
    @field_validator('phrase')
    @classmethod
    def validate_phrase_length(cls, v: str) -> str:
        word_count = len(v.split())
        if word_count > 6:
            raise ValueError(f'Phrase must be ≤6 words, got {word_count}: "{v}"')
        return v

class LanguageConfig(BaseModel):
    """Configuration for a target language."""
    language_code: str
    language_name: str
    native_name: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"
    has_gender: bool = False
    has_articles: bool = False
    
class GeneratedAudio(BaseModel):
    """Metadata for a generated audio file."""
    text: str
    file_path: str
    cached: bool = False
    character_count: int
```

---

## ElevenLabs Integration (SDK)

### Using the Official Python SDK

```python
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings, save

class TTSService:
    def __init__(self, api_key: str, voice_id: str, model_id: str = "eleven_multilingual_v2"):
        self.client = ElevenLabs(api_key=api_key)
        self.voice_id = voice_id
        self.model_id = model_id
        # Settings optimized for flashcard consistency and beginner clarity
        self.voice_settings = VoiceSettings(
            stability=0.7,         # Consistent pronunciation across cards
            similarity_boost=0.8,  # Strong voice adherence
            style=0.0,             # No expressive variation
            use_speaker_boost=True,
            speed=0.9,             # Slightly slower for beginners
        )
    
    def generate_audio(self, text: str, output_path: str) -> GeneratedAudio:
        """Generate audio using ElevenLabs SDK."""
        # Check cache first
        cache_path = self._get_cache_path(text)
        if cache_path.exists():
            return GeneratedAudio(
                text=text,
                file_path=str(cache_path),
                cached=True,
                character_count=len(text)
            )
        
        # Generate via SDK
        audio = self.client.text_to_speech.convert(
            voice_id=self.voice_id,
            text=text,
            model_id=self.model_id,
            voice_settings=self.voice_settings,
            output_format="mp3_44100_128"
        )
        
        # Save to cache
        save(audio, str(cache_path))
        
        return GeneratedAudio(
            text=text,
            file_path=str(cache_path),
            cached=False,
            character_count=len(text)
        )
    
    def list_voices(self) -> list[dict]:
        """List available voices."""
        response = self.client.voices.get_all()
        return [
            {
                "voice_id": v.voice_id,
                "name": v.name,
                "labels": v.labels,
            }
            for v in response.voices
        ]
```

### Audio Caching Strategy

Cache key includes: `{language}/{voice_id}/{text_hash}.mp3`

This allows:
- Switching voices without losing cache
- Per-language organization
- Sharing cache across deck generations

### Voice Selection Guidelines

For language learning flashcards, prioritize:
1. **Native speaker voices** trained on actual target language speech
2. **Educational/e-learning tagged voices** designed for clarity
3. **Consistent articulation** over expressive range

**Recommended voice settings for flashcards:**
| Setting | Value | Reason |
|---------|-------|--------|
| stability | 0.7 | Consistent pronunciation across all cards |
| similarity_boost | 0.8 | Strong adherence to voice character |
| style | 0.0 | No expressive variation (predictable output) |
| speed | 0.9 | Slightly slower helps beginners distinguish sounds |

### Pronunciation Considerations

**Always spell out numbers** in text—digits may render in English pronunciation:
- ✅ `"venti"` 
- ❌ `"20"`

**Test these patterns before bulk generation:**
- Italian: gli (famiglia), gn (gnocchi), sc (pesce vs pesca)
- Spanish: ñ, ll, rr
- French: liaison, nasal vowels

Use the `eleven_multilingual_v2` model for best results with non-English languages.



---

## Anki Note Type

### Fields (8 total)
1. `Word` - Target language word
2. `Translation` - English translation
3. `Phrase` - Example phrase
4. `PhraseTranslation` - English phrase
5. `WordAudio` - `[sound:word_xxx.mp3]`
6. `PhraseAudio` - `[sound:phrase_xxx.mp3]`
7. `PartOfSpeech` - Grammar category
8. `Gender` - Grammatical gender (if applicable)

### Card Templates (3 types)

#### Card 1: Recognition (Target → English)
**Front:** Word + Audio
**Back:** Translation, grammar info, example phrase with audio

#### Card 2: Production (English → Target)
**Front:** English translation + part of speech
**Back:** Target word with audio, example phrase

#### Card 3: Listening (Audio Only → All)
**Front:** "What do you hear?" + Word audio
**Back:** Full card with all information

### Card Styling (CSS)
```css
.card {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 24px;
    text-align: center;
    color: #333;
    background-color: #fafafa;
    padding: 20px;
}

.word {
    font-size: 32px;
    font-weight: bold;
    color: #1a5f2a;
    margin-bottom: 10px;
}

.translation {
    font-size: 28px;
    color: #2c3e50;
}

.phrase {
    font-size: 20px;
    font-style: italic;
    color: #555;
    margin-top: 15px;
}

.phrase-translation {
    font-size: 18px;
    color: #777;
    margin-top: 5px;
}

.pos {
    font-size: 16px;
    color: #888;
    margin-top: 5px;
}

.prompt {
    font-size: 18px;
    color: #666;
    margin-bottom: 10px;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 15px 0;
}
```

---

## CLI Interface

### Commands

```bash
# List available languages
anki-artisan list-languages

# List available voices (for a language)
anki-artisan list-voices --language italian

# Validate CSV without generating audio
anki-artisan generate --language italian --level a1 --dry-run

# Generate deck
anki-artisan generate --language italian --level a1 --output output/italian_a1.apkg

# Generate with specific voice override
anki-artisan generate --language italian --level a1 --voice-id "abc123"

# Generate with verbose logging
anki-artisan generate --language italian --level a1 --verbose

# Use only cached audio (no API calls)
anki-artisan generate --language italian --level a1 --cache-only
```

### Environment Variables
```bash
ELEVENLABS_API_KEY=your_api_key_here
# Optional: override default voice per language
ELEVENLABS_VOICE_ID_ITALIAN=voice_id_here
ELEVENLABS_VOICE_ID_SPANISH=voice_id_here
```



---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Missing API key | Exit with message: "Set ELEVENLABS_API_KEY environment variable" |
| Unknown language | List available languages and exit |
| Missing level CSV | Exit with message showing expected path |
| Invalid CSV row | Log warning with line number, skip row, continue |
| API rate limit | Exponential backoff (1s, 2s, 4s), max 3 retries |
| API quota exceeded | Stop, report progress, suggest --cache-only mode |
| Cache hit | Skip API call, log as "cached" |
| Network error | Retry 3 times, then fail with error |

---

## Test Data

### languages/italian/a1.csv (5-word validation set)

```csv
word,translation,phrase,phrase_translation,part_of_speech,gender,tags
il giorno,the day,Buon giorno!,Good day!,noun,m,greetings time
la notte,the night,Buona notte.,Good night.,noun,f,greetings time
mangiare,to eat,Voglio mangiare.,I want to eat.,verb,n/a,verbs food
bene,well,Sto bene.,I am well.,adverb,n/a,greetings basic
grande,big,È molto grande.,It is very big.,adjective,n/a,adjectives
```

---

## Success Criteria

### Phase 1: 5-Word Validation
- [ ] CLI parses arguments correctly
- [ ] Italian config.yaml loads
- [ ] CSV validates with Pydantic
- [ ] ElevenLabs SDK generates audio
- [ ] Audio cached correctly (language/voice/hash structure)
- [ ] genanki creates valid .apkg
- [ ] Deck imports into Anki Desktop
- [ ] All 3 card types display correctly
- [ ] Audio plays on all cards
- [ ] Character usage tracked and logged

### Phase 2: Full A1 Deck
- [ ] 50 vocabulary items processed
- [ ] 100 audio files generated and cached
- [ ] Deck syncs to AnkiDroid via AnkiWeb
- [ ] Tags enable filtering by category

---

## Future Enhancements (Out of Scope)

1. **Interactive voice selection** - TUI to preview and select voices
2. **Progress bar** - Rich/tqdm for batch processing
3. **Resume capability** - Continue from last successful item
4. **Spaced generation** - Generate subsets to spread API usage
5. **Pronunciation dictionary** - Custom pronunciations for edge cases
6. **Multiple deck formats** - Simplified cards, cloze deletion, etc.
7. **Web interface** - Browser-based deck builder

---

## References

- [genanki GitHub](https://github.com/kerrickstaley/genanki)
- [ElevenLabs Python SDK](https://github.com/elevenlabs/elevenlabs-python)
- [ElevenLabs API Docs](https://elevenlabs.io/docs/api-reference)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [CEFR Levels](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions)
