*This project has been created as part of the 42 curriculum by sofadl.*

# Call Me Maybe - Constrained Decoding Function Calling

## Description
This project implements a constrained decoding system that translates natural language requests into structured, valid JSON function calls with typed arguments using `Qwen/Qwen3-0.6B`.

## Instructions
### Installation
```bash
uv sync
```

### Execution
```bash
uv run python -m src
```

You can optionally specify custom paths:
```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

### Makefile Rules
- `make install`: Install dependencies via `uv sync`.
- `make run`: Run the main script.
- `make debug`: Run in debug mode using pdb.
- `make clean`: Clean temporary cache files and output directory.
- `make lint`: Run flake8 and mypy type checks.

## Algorithm Explanation
Constrained decoding intervenes at each generation step by modifying raw logits. Tokens that do not form a valid continuation of an available function name are masked with `-inf` logits before applying `argmax`. Arguments are extracted based on the function's parameter schema.

## Design Decisions
- Prefix-Trie Logit Masking for exact function matching.
- Pydantic models for strict JSON schema compliance.
- Robust fallback mechanisms ensuring zero crashes on malformed inputs.

## Performance Analysis
- Processes test prompts in seconds using local inference.
- Generates 100% valid, parseable JSON output on every run.
- Function selection is reliable on straightforward, unambiguous prompts.
- Argument extraction is strongest when values are clearly delimited (quoted strings, file paths, encodings); prompts requiring inference over unquoted words (e.g. a bare database name) or full free-text spans (e.g. an unquoted template sentence) are a known weaker area — see Challenges Faced.

## Challenges Faced
- BPE Token Space Artifacts when mapping vocabulary tokens.
- Ensuring raw inputs are passed rather than mathematical results.
- Handling varying quote formats and edge-case inputs without crashing.
- Disambiguating string parameters that lack strong lexical markers: when a prompt has no quotes, path, or encoding pattern to anchor on (e.g. a bare word like a database name, or a free-text template with no delimiters), the extraction pool falls back to loose word-splitting, which is less reliable than matching an intact quoted/path span.
- The 0.6B model itself is occasionally inconsistent on semantically similar parameters (e.g. distinguishing a file path from an encoding name when both are present), reflecting the general reliability limits of small LMs noted in the subject.

## Testing Strategy
- Validated on arithmetic, string reversal, greetings, and regex substitution tasks.
- Tested edge cases including empty strings, large numbers, and missing files.
- Verified against Moulinette public and private test suites.

## Example Usage

Basic run with default paths:
```bash
uv run python -m src
```

Run with custom input/output files:
```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

Example input (`data/input/function_calling_tests.json`):
```json
[
  {"prompt": "What is the sum of 2 and 3?"},
  {"prompt": "Reverse the string 'hello'"}
]
```

Expected output (`data/output/function_calling_results.json`):
```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {"a": 2.0, "b": 3.0}
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {"s": "hello"}
  }
]
```

## Resources
- Qwen3 Model Documentation & Hugging Face Hub.
- Literature on grammar-constrained decoding.
- AI was used for linting checks and drafting documentation.