"""JSON file parsing and writing with error handling."""

import json
from pathlib import Path
from typing import Any, List, Optional

from pydantic import TypeAdapter, ValidationError

from .models import FunctionCallResult, FunctionDefinition, TestPrompt


def _load_json_file(filepath: str) -> Optional[List[Any]]:
    """Safely load a JSON file containing a list of items."""
    path = Path(filepath)

    if not path.exists():
        print(f"Error: File not found: {filepath}")
        return None

    if not path.is_file():
        print(f"Error: Path is not a file: {filepath}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print(f"Error: File is empty: {filepath}")
            return None

        data = json.loads(content)

        if not isinstance(data, list):
            print(f"Error: Expected JSON array in {filepath}")
            return None

        return data

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON syntax in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Error: Could not read {filepath}: {e}")
        return None


def load_function_definitions(filepath: str) -> List[FunctionDefinition]:
    """Load and validate function definitions from a JSON file.

    Each raw item is validated through
    FunctionDefinition.model_validate, pydantic's canonical
    validation entry point, rather than plain keyword-unpacking.
    Invalid items are skipped individually so one malformed entry
    doesn't discard the whole file.
    """
    raw_list = _load_json_file(filepath)
    if raw_list is None:
        return []

    functions: List[FunctionDefinition] = []
    for item in raw_list:
        try:
            functions.append(FunctionDefinition.model_validate(item))
        except ValidationError as e:
            print(f"Warning: Skipping invalid function definition: {e}")
        except Exception as e:
            print(f"Warning: Skipping invalid function definition: {e}")

    return functions


def load_test_prompts(filepath: str) -> List[TestPrompt]:
    """Load and validate test prompts from a JSON file.

    Each raw item is validated through TestPrompt.model_validate.
    Invalid items are skipped individually so one malformed entry
    doesn't discard the whole file.
    """
    raw_list = _load_json_file(filepath)
    if raw_list is None:
        return []

    prompts: List[TestPrompt] = []
    for item in raw_list:
        try:
            prompts.append(TestPrompt.model_validate(item))
        except ValidationError as e:
            print(f"Warning: Skipping invalid test prompt: {e}")
        except Exception as e:
            print(f"Warning: Skipping invalid test prompt: {e}")

    return prompts


def save_results(results: List[FunctionCallResult], filepath: str) -> bool:
    """Save function call results to a JSON file.

    Uses a pydantic TypeAdapter over List[FunctionCallResult] to
    validate the full collection as a unit before serialization,
    then dumps to JSON via pydantic's own JSON-mode dumping so
    output types match each field's declared schema exactly.
    """
    try:
        adapter = TypeAdapter(List[FunctionCallResult])
        validated: List[FunctionCallResult] = adapter.validate_python(
            results
        )

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = [r.model_dump(mode="json") for r in validated]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except ValidationError as e:
        print(f"Error: Results failed validation before saving: {e}")
        return False
    except Exception as e:
        print(f"Error: Failed to save results to {filepath}: {e}")
        return False
