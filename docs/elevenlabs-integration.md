# ElevenLabs Integration Guide

## Overview

Anki Artisan uses the ElevenLabs API for neural text-to-speech audio generation. This document covers API configuration, voice selection, caching strategy, and cost optimization.

---

## Configuration

### Environment Variables

```bash
# Required - your ElevenLabs API key
ELEVENLABS_API_KEY=your_api_key_here

# Optional - specific voice ID (set after listing available voices)
ELEVENLABS_VOICE_ID=voice_id_here
```

### API Settings

```python
ELEVENLABS_CONFIG = {
    "api_base_url": "https://api.elevenlabs.io/v1",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.75,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": True
    },
    "output_format": "mp3_44100_128"
}
```

---

## Voice Selection

### Criteria for Language Learning

- Native speaker voice for target language
- Clear enunciation (prefer educational/professional voices)
- Moderate-to-slow natural pace
- Consistent quality across short phrases

### List Available Voices

```bash
anki-artisan --list-voices
```

Or via API:
```
GET https://api.elevenlabs.io/v1/voices
Headers: xi-api-key: {API_KEY}
```

### Recommended Voices by Language

| Language | Voice | Voice ID | Notes |
|----------|-------|----------|-------|
| Italian | TBD | TBD | Select after testing |
| Spanish | TBD | TBD | Select after testing |
| French | TBD | TBD | Select after testing |

---

## API Endpoints

### Text-to-Speech

```
POST /v1/text-to-speech/{voice_id}
Headers: 
  xi-api-key: {API_KEY}
  Content-Type: application/json
Body: {
  "text": "La casa è bella.",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.75,
    "similarity_boost": 0.75
  }
}
Response: audio/mpeg binary
```

---

## Audio Caching Strategy

### Why Cache?

- Prevents redundant API calls for repeated words
- Reduces costs significantly for large decks
- Enables offline regeneration of decks
- Faster iteration during development

### Cache Implementation

```
cache/
└── audio/
    └── {hash}.mp3
```

**Hash key formula**: `sha256(text + language + voice_id)`

### Cache Behavior

| Scenario | Action |
|----------|--------|
| Audio in cache | Return cached file, skip API call |
| Audio not cached | Call API, save to cache, return |
| `--cache-only` flag | Only use cached audio, skip missing |
| `--no-cache` flag | Always call API, overwrite cache |

---

## Rate Limits & Error Handling

### Rate Limit Strategy

ElevenLabs enforces character quotas per month.

| Retry | Delay |
|-------|-------|
| 1 | 1 second |
| 2 | 2 seconds |
| 3 | 4 seconds |
| Fail | Log error, save progress |

### Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Invalid API key | Check ELEVENLABS_API_KEY |
| 429 | Rate limited | Retry with backoff |
| 400 | Invalid voice ID | List voices and select valid one |

---

## Character Budget

### Estimation

| Item | Avg Characters |
|------|----------------|
| Word (with article) | ~8 |
| Example phrase (≤6 words) | ~25 |
| **Per vocabulary item** | **~33** |

### Monthly Quota (Free Tier)

- ~10,000 characters/month
- 30-word deck ≈ 990 characters (~10% of quota)
- 100-word deck ≈ 3,300 characters (~33% of quota)

---

## Best Practices

1. **Always test with small batches first** (5 words)
2. **Enable caching** to avoid duplicate API calls
3. **Monitor character usage** via `get_usage_stats()`
4. **Use dry-run mode** to validate CSV before generating audio
5. **Keep phrases short** (≤6 words) to optimize character usage
