# FinBERT Lifecycle Reference

Complete specifications for FinBERT model management, device detection, and batch processing.

---

## Lazy Loading Strategy

- Load FinBERT only when first inference requested (not session start)
- Device detection: Check GPU availability (CUDA/MPS) -> fallback to CPU
- Model caching: Keep model in memory for session, reload only on version change
- Version tracking: Log model_version in all outputs for reproducibility

---

## Device Detection & Selection

```python
import torch

# Priority order: CUDA -> MPS -> CPU
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
```

### Device-Specific Parameters

| Parameter | GPU (CUDA) | GPU (MPS) | CPU | Description |
|-----------|------------|-----------|-----|-------------|
| batch_size | 32 | 16 | 8 | Headlines per inference batch |
| max_length | 128 | 128 | 128 | Max token length |
| timeout | 30s | 30s | 60s | Per-batch timeout |

---

## Batch Adaptation Strategy

```python
def get_batch_size(device: str, config_batch_size: int) -> int:
    """Adapt batch size to device capabilities."""
    if device == "cuda":
        return min(32, config_batch_size)
    elif device == "mps":
        return min(16, config_batch_size)
    else:  # cpu
        return min(8, config_batch_size)
```

### Processing Modes

| Device | Processing | Memory Bound | Notes |
|--------|------------|--------------|-------|
| CUDA | Parallel batches | ~4GB VRAM | Optimal for high throughput |
| MPS | Parallel batches | ~4GB | Apple Silicon GPU |
| CPU | Sequential | No limit | More forgiving on timeout |

---

## Memory Management

### Cache Management
- Monitor cache size, evict LRU entries if >500MB
- Cache key: headline text hash (MD5)
- Cache TTL: Session duration (no persistence)

### GPU Memory
- Pre-allocate batch tensors
- Clear cache between large batches: `torch.cuda.empty_cache()`
- Monitor VRAM usage before inference

### Timeout Handling
```python
# On timeout, reduce batch and retry
try:
    results = model.predict(batch, timeout=timeout)
except TimeoutError:
    new_batch_size = batch_size // 2
    # Retry with smaller batches
```

---

## Error Recovery

| Error | Recovery Strategy | Fallback |
|-------|-------------------|----------|
| Model loading failure | Retry with CPU device | Keyword-based sentiment |
| CUDA OOM | Reduce batch_size by 50% | Process sequentially |
| Inference timeout | Retry with smaller batch | Partial results + flag |
| Version mismatch | Clear cache, reload model | Continue with cached |

---

## Model Configuration

```python
MODEL_CONFIG = {
    'model_name': 'ProsusAI/finbert',
    'max_length': 128,
    'num_labels': 3,  # positive, negative, neutral
    'output_hidden_states': False,
    'output_attentions': False
}
```

---

## Initialization Checklist

- [ ] Device detected and logged
- [ ] Batch size adapted to device
- [ ] Model loaded successfully
- [ ] Cache initialized
- [ ] Timeout configured
