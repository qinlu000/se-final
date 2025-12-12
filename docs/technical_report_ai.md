# AI System Technical Report: LLM Integration

## 1. Intelligence Architecture

### 1.1 The "Model-Agnostic" Proxy
The system uses the **Proxy Pattern** via OpenRouter.
- **Interface**: OpenAI-compatible JSON API.
- **Routing**: The backend sends requests to `https://openrouter.ai/api/v1`, which routes to `DeepSeek V3`.
- **Why?**: Allows hot-swapping models (e.g., to `meta-llama/llama-3-70b`) without code changes if DeepSeek experiences downtime.

## 2. Prompt Engineering Specification

### 2.1 System Prompt (Source of Truth)
The prompting strategy relies on **Role Definition**, **Constraint Setting**, and **Output Schematization**.

```text
ROLE: You are a concise social-media assistant.
CONSTRAINT: Return ONLY valid JSON. No reasoning preamble.
MODES:
- summary: limit to 120 chars.
- vibe: return {score, label, emoji, color}.
- polish: rewrite for fluency.
...
FORMAT: {"summary": "...", "vibe": {...}}
```
**Technique**: "JSON Mode" (enforced via API parameter) guarantees the output can be parsed by `json.loads()`.

## 3. Performance & Cost Modeling

### 3.1 Token Usage Analysis
- **Avg User Post**: 50 Chinese characters (~80 tokens).
- **System Prompt Overhead**: ~150 tokens.
- **Output (Summary/Vibe)**: ~100 tokens.
- **Total per Request**: ~330 tokens.

### 3.2 Cost Calculation (DeepSeek V3 Pricing)
- **Input**: $0.14 / 1M tokens.
- **Output**: $0.28 / 1M tokens.
- **Cost per Analysis**:
    - Input: $0.000032
    - Output: $0.000028
    - **Total**: ~$0.00006 per click (Negligible).
- **At Scale**: 10,000 requests = $0.60.

### 3.3 Semantic Caching Strategy
To reduce cost/latency further, we implemented a hash-based cache.
- **Key Function**: `H = SHA256(Content_UTF8 + Mode_Str + Tone_Str)`
- **Hit Rate Estimate**:
    - Viral content (Viewing): High Hit Rate (>90%).
    - Creation content (Magic Compose): Low Hit Rate (<5%).
- **Benefit**: Reduces P99 latency from 2.5s (LLM Gen) to <5ms (Redis Read).

## 4. Safety & Robustness

### 4.1 Sensitive Word Defense
We employ a **"Sandwich Defense"** structure.
1.  **Pre-Check**: User Input -> `check_sensitive(Input)` -> **Reject** if bad.
2.  **Processing**: LLM Generation.
3.  **Post-Check**: LLM Output -> `check_sensitive(Output)` -> **Mask** if bad.
    - *Why Post-Check?* Jailbroken LLMs might generate offensive content even from safe inputs.

### 4.2 Failure Mode Handling (Finite State Machine)
- **State: Normal**: API Calls succeed.
- **State: Timeout**: If LLM takes >10s, abort and return "AI Busy".
- **State: API Error**: If 5xx from OpenRouter, switch to `HeuristicFallback`.
    - `HeuristicFallback`: Returns first 100 chars as summary; Regex matches keywords ("food", "tech") as tags.

## 5. Future AI Roadmap
- **RAG (Retrieval Augmented Generation)**: Retrieve user's previous 10 posts to mimic their specific tone in "Magic Compose".
- **Vision**: Use `gpt-4o-mini` to analyze uploaded images for alt-text generation.
