# LLMAid – Public API Reference

*Version 0.0.0‑wishful – authoritative spec for the first implementation*

> This reference defines every **public surface** of the upcoming `llmaid` module so maintainers can generate unit‑test scaffolding and implement the library in strict TDD. If code and spec ever diverge, update one until tests pass.

---

## Table of contents

1. [Configuration & instantiation](#1-configuration--instantiation)
2. [Prompt‑builder helpers](#2-prompt-builder-helpers)
3. [Core completion methods](#3-core-completion-methods)
4. [Streaming](#4-streaming)
5. [Callable clone operator](#5-callable-clone-operator)
6. [Error hierarchy](#6-error-hierarchy)
7. [Environment‑variable precedence](#7-environment-variable-precedence)

---

## 1. Configuration & instantiation

### Factory function `llmaid(**config) -> LLMAid`

> Primary constructor; users normally call `llmaid()` rather than importing `LLMAid` directly (which still exists for typing).

| Param                                   | Type                       | Default                  | Purpose                                                                                                   |
| --------------------------------------- | -------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------- |
| **Connection**                          |                            |                          |                                                                                                           |
| `base_url`                              | `str`                      | `http://127.0.0.1:17434` | URL of an OpenAI‑compatible backend.                                                                      |
| `secret`                                | `str \| None`              | `None`                   | Sent as `Authorization: Bearer <secret>` if not `None`.                                                   |
| `model`                                 | `str`                      | `mistral-large-v0.1`     | Model identifier.                                                                                         |
| **Prompting**                           |                            |                          |                                                                                                           |
| `prompt_template_dir`                   | `str \| Path \| None`      | `None`                   | Base folder searched by `prompt_template()` / `system_prompt()`.                                          |
| `strict_template`                       | `bool`                     | `True`                   | Raise if placeholders are missing or extra.                                                             |
| `strict_context_length`                       | `bool`                     | `True`                   | Raise if max context length is exceeded if yes.                                                             |
| **Resilience**                          |                            |                          |                                                                                                           |
| `max_retries`                           | `int`                      | `3`                      | Maximum attempts on retryable errors.                                                                     |
| `backoff_factor`                        | `float`                    | `1.0`                    | Base seconds for exponential back‑off (`sleep = backoff_factor * 2**(attempt‑1)`).                        |
| `max_timeout`                        | `int`                    | `60`                    | seconds until LLM call is considered stalled and closed gracefully.                        |
| **Common generation knobs (ctor‑only)** |                            |                          |                                                                                                           |
|   `context_length`                         | `int\| None`            |  `8192`                  | both Max and target content length for provider. LLMAID either raise error or silently trims  value                                                                                     |

|   `temperature`                         | `float \| None`            |  `None`                  | Sampling temperature.                                                                                     |
|   `max_tokens`                          | `int \| None`              | `None`                   | Hard limit on response tokens.                                                                            |
|   `top_p`                               | `float \| None`            | `None`                   | Nucleus sampling fraction.                                                                                |
|   `frequency_penalty`                   | `float \| None`            | `None`                   | Penalise new token frequency.                                                                             |
|   `presence_penalty`                    | `float \| None`            | `None`                   | Penalise token presence.                                                                                  |
|   `stop`                                | `str \| list[str] \| None` | `None`                   | Stop sequence(s).                                                                                         |
|   `logit_bias`                          | `dict[int,int] \| None`    | `None`                   | OpenAI logit bias map.                                                                                    |
|   `user`                                | `str \| None`              | `None`                   | User identifier forwarded to backend.                                                                     |
| `model_parameter`                       | `dict[str, Any] \| None`   | `None`                   | **Free‑form** dict merged into request JSON *after* built‑ins—use this to pass obscure provider switches. |

>

#### Acceptance criteria

* **Given** `LLMAID_TEMPERATURE=0.8` **When** `llmaid()` **Then** `instance.temperature == 0.8`.
* **Given** a ctor kwarg overrides an env var **Then** kwarg wins.
* **Given** `temperature=` passed to `completion` **Then it is used as a prompt template variable**

---
## 2. Prompt‑builder helpers

Helpers return **new, immutable `LLMAid` instances** that inherit all configuration from the parent except for the updated prompt.

`LLMAid.prompt_template(*templates: str | Path, strict_template: bool | None = None) -> LLMAid`

Configure – or re‑configure – the **prompt template stack** for the instance.

**Signature**
```python
prompt_template(*templates: str | Path, strict_template: bool | None = None) -> LLMAid
```

#### How it works
1. **Accepts any number of arguments.**  Each `*template` may be:
    - **Inline `str`** – treated verbatim.
    - **`Path` / path‑like string** – the file is read as UTF‑8.  Resolution order:
        1. Absolute path ⇒ used directly.
        2. Relative path ⇒ looked up inside `prompt_template_dir` (if set).
        3. Fallback ⇒ relative to current working directory.
2. **Concatenation** – parts are joined **in the given order**, separated by exactly two newlines
3. **Placeholder syntax** – Uses *Jinja‑flavoured* double‑brace tokens, e.g. `{{ role }}`.
4. **`strict\_template`override** – If provided, overrides the instance’s setting *for this derived clone only*; otherwise the parent’s flag is inherited.
5. **Return value** – A **new LLMAid object** whose prompt template string equals the concatenation result. The parent is not mutated.

#### Example

```python
from pathlib import Path
ai = llmaid(prompt_template_dir=Path("./prompts"))
scientist = ai.prompt_template("roles/scientist.txt", "task_summary.txt")
# Effective prompt == contents("roles/scientist.txt") + "/n/n" + contents("task_summary.txt")
```

### `LLMAid.system_prompt(*templates, **kwargs)`  – *exact alias of* `prompt_template`

Provided for ergonomic parity with the OpenAI SDK; no behavioural differences.

#### Acceptance criteria

- Given three templates (`"A"`, `"B"`, `"C"`) **When** used **Then** the resulting prompt is the three joined with two newlines: `"A\n\nB\n\nC"`.
- Given `strict_template=True` and a placeholder mismatch **Then** `TemplateMismatchError` is raised *before* any backend call.
- Given an unknown keyword argument to the derived instance **Then** `TemplateMismatchError` is raised.

---

## 3. Core completion methods

| Method                                          | Sync/Async | Returns              | Notes                     |
| ----------------------------------------------- | ---------- | -------------------- | ------------------------- |
| `completion(*user_parts: str, **placeholders)`  | sync       | `str`                | Entire assistant message. |
| `acompletion(*user_parts: str, **placeholders)` | async      | `str`                | Awaitable equivalent.     |
| `stream(*user_parts: str, **placeholders)`      | async      | `AsyncIterator[str]` | Token stream.             |


| Behaviour aspect  | Spec                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------- |
| Positional args   | Appended to the final prompt, each preceded by a single newline.                                  |
| Keyword args      | Injected into `{{ placeholder }}` tokens; must satisfy `strict_template`.                         |
| **Rejected args** | Any key matching the generation‑knob list **or** `model_parameter`.  Raises `ConfigurationError`. |
| Retry policy      | Automatic `max_retries` with exponential back‑off.                                                |

## 4. Streaming specifics

* Must honour back‑pressure (`await` network reads).
* Cancelling the async iterator closes the HTTP connection within one event‑loop tick.

---

## 5. Callable clone operator `__call__(**overrides) -> LLMAid`

Acts like `copy(update=overrides)`:

* All **constructor parameters**—including generation knobs and `model_parameter`—may be provided.
* The original instance is **never** mutated.
* Overrides follow the same validation rules (e.g. type checks) as the ctor.

```python
base = llmaid(model="gpt-3.5", temperature=0.2)
creative = base(temperature=0.9)
compact  = creative(max_tokens=32)
```

---

## 6. Error hierarchy

```text
LLMAidError (base)
├── ConfigurationError              # invalid configuration  
├── TemplateMismatchError           # placeholder trouble
├── ContextLengthExceededError      # prompt exceeds context limit
├── ProviderError                   # downstream issues
│   ├── ProviderHTTPError           # 4XX/5XX non‑retryable
│   ├── ProviderRateLimitError      # 429, retryable
│   └── ProviderTimeoutError        # network/H timeout, retryable
└── RetryExhaustedError             # max_retries exceeded

```

All exceptions expose `.attempt`, `.max_attempts`, and `.last_response` (when applicable) for rich assertions.

---

## 7. Environment‑variable precedence

1. **Explicit kwargs** in constructor.
2. **Call‑time overrides** via the clone operator.
3. **Process env** (`LLMAID_*`).
4. Hard‑coded defaults.

### Supported env variables

| Env var                    | Maps to ctor param                                |
| -------------------------- | ------------------------------------------------- |
| `LLMAID_BASE_URL`          | `base_url`                                        |
| `LLMAID_SECRET`            | `secret`                                          |
| `LLMAID_MODEL`             | `model`                                           |
| `LLMAID_PROMPT_DIR`        | `prompt_template_dir`                             |
| `LLMAID_STRICT_TEMPLATE`   | `strict_template`                                 |
| `LLMAID_TEMPERATURE`       | `temperature`                                     |
| `LLMAID_MAX_TOKENS`        | `max_tokens`                                      |
| `LLMAID_TOP_P`             | `top_p`                                           |
| `LLMAID_FREQUENCY_PENALTY` | `frequency_penalty`                               |
| `LLMAID_PRESENCE_PENALTY`  | `presence_penalty`                                |
| `LLMAID_STOP`              | `stop`                                            |
| (all others)               | Must be supplied via `model_parameter` or ignored |

---
