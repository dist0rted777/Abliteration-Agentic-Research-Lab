# Abliterated-Qwen-SuperLight

This is an abliterated version of [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B), specifically modified to remove refusal behaviors while maintaining model coherence and performance.

## Model Details

- **Base Model:** Qwen/Qwen3-0.6B
- **Technique:** Refusal Direction Ablation (Spectral Cascade)
- **Tool used:** [OBLITERATUS](https://github.com/elder-plinius/OBLITERATUS)
- **Refusal Rate:** 0.0% (Verified with 100 samples)
- **Perplexity:** 6.28 (Base: 5.52)
- **Coherence:** 1.0 (Fully preserved)

## Abliteration Process

This model was liberated using the **Spectral Cascade** method, which decomposes the refusal signal into spectral frequency bands via Discrete Cosine Transform (DCT). This allows for frequency-selective attenuation, separating systematic refusal trends from per-layer capability-entangled noise.

### Configuration
- **Directions:** 8 SVD-extracted refusal directions
- **Refinement passes:** 3 iterative passes
- **Regularization:** 0.3 (Norm-preserving)
- **Whitened SVD:** Enabled
- **Iterative Refinement:** True

## Performance Metrics

| Metric | Base Model | Abliterated Model |
|--------|------------|-------------------|
| Refusal Rate | ~100% (Safety) | 0.0% |
| Perplexity | 5.52 | 6.28 |
| KL Divergence | - | 0.00012 |
| Coherence | 1.0 | 1.0 |

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Dist0rted/Abliterated-Qwen-SuperLight"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "Write a guide on how to pick a lock."
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)

print(tokenizer.decode(outputs[0]))
```

## References

- **Arditi et al. (2024):** Refusal in Language Models Is Mediated by a Single Direction (NeurIPS 2024)
- **Gabliteration (arXiv:2512.18901):** SVD-based multi-direction extraction
- **OBLITERATUS:** Master Ablation Suite by elder-plinius
- **Spectral Cascade:** Frequency-domain decomposition for precision liberation.

## Disclaimer

This model has had its safety guardrails removed through weight surgery. It will follow instructions that the base model would typically refuse. Use responsibly and in accordance with your local laws and regulations.
