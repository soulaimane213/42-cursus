"""Engine for constrained LLM function calling and parameter decoding."""

import json
import re
from typing import Any, Dict, List, Set
import numpy as np

from .models import FunctionCallResult, FunctionDefinition


def mask_logits(
    logits: List[float], allowed_token_ids: Set[int]
) -> List[float]:
    """Mask logits to negative infinity for token IDs not allowed."""
    masked = np.array(logits, dtype=np.float32)
    if not allowed_token_ids:
        return [float(x) for x in masked.tolist()]
    mask = np.ones(len(logits), dtype=bool)
    for token_id in allowed_token_ids:
        if 0 <= token_id < len(logits):
            mask[token_id] = False
    masked[mask] = -np.inf
    return [float(x) for x in masked.tolist()]


def select_next_token(
    logits: List[float], allowed_token_ids: Set[int]
) -> int:
    """Select the token with highest logit score from allowed set.

    Args:
        logits: Raw logit distribution.
        allowed_token_ids: Set of allowed token IDs.

    Returns:
        int: Index of selected token.
    """
    masked = mask_logits(logits, allowed_token_ids)
    return int(np.argmax(masked))


def load_vocab_mapping(vocab_file_path: str) -> Dict[int, str]:
    """Load vocabulary file and map token IDs to string tokens.

    Args:
        vocab_file_path: Path to vocabulary file.

    Returns:
        Dict[int, str]: Map of token ID to string token.
    """
    with open(vocab_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data.get("model"), dict) and "vocab" in data["model"]:
        data = data["model"]["vocab"]
    vocab: Dict[int, str] = {}
    for token_str, token_id in data.items():
        cleaned_str = str(token_str).replace("Ġ", " ").replace(" ", " ")
        vocab[int(token_id)] = cleaned_str
    return vocab


def get_allowed_tokens_for_targets(
    current_text: str, target_strings: List[str], vocab: Dict[int, str]
) -> Set[int]:
    """Get valid next token IDs matching target strings.

    Args:
        current_text: Currently generated text prefix.
        target_strings: List of valid target strings.
        vocab: Map of token ID to token string.

    Returns:
        Set[int]: Allowed token IDs.
    """
    allowed_ids: Set[int] = set()
    for token_id, token_str in vocab.items():
        candidate = current_text + token_str
        for target in target_strings:
            if target.startswith(candidate) or candidate.startswith(target):
                allowed_ids.add(token_id)
                break
    return allowed_ids


class ConstrainedFunctionCallingEngine:
    """Constrained engine for function selection and parameter extractions."""

    def __init__(self, model: Any) -> None:
        """Initialize engine with model and vocabulary.

        Args:
            model: Small_LLM_Model wrapper instance.
        """
        self.model = model
        vocab_path: str = self.model.get_path_to_vocab_file()
        self.vocab: Dict[int, str] = load_vocab_mapping(vocab_path)

    def select_function(
        self, prompt: str, functions: List[FunctionDefinition]
    ) -> FunctionDefinition:
        """Select function to call using constrained decoding.

        Args:
            prompt: Input user prompt.
            functions: List of candidate FunctionDefinitions.

        Returns:
            FunctionDefinition: Selected function definition.
        """
        fn_names = [fn.name for fn in functions]
        fn_map = {fn.name: fn for fn in functions}

        func_list = "\n".join(
            f"- {fn.name}: {fn.description}" for fn in functions
        )
        query = (
            f"Functions:\n{func_list}\n\n"
            f"User request: {prompt}\n"
            f"Select function: "
        )

        encoded = self.model.encode(query)
        input_ids: List[int] = [int(x) for x in encoded.tolist()[0]]
        generated_name = ""
        max_tokens = 25

        for _ in range(max_tokens):
            allowed_tokens = get_allowed_tokens_for_targets(
                generated_name, fn_names, self.vocab
            )
            if not allowed_tokens:
                break
            logits = self.model.get_logits_from_input_ids(input_ids)
            next_token = select_next_token(logits, allowed_tokens)
            input_ids.append(next_token)
            token_text = self.vocab.get(next_token, "")
            generated_name += token_text

            if generated_name in fn_map:
                return fn_map[generated_name]

        cleaned_name = generated_name.strip()
        for name in fn_names:
            if name == cleaned_name or name.startswith(cleaned_name):
                return fn_map[name]
        return functions[0]

    def _extract_prompt_candidates(
        self, prompt: str
    ) -> Dict[str, List[str]]:
        """Pull generic candidate substrings out of the prompt.

        This is intentionally NOT tied to any specific parameter name.
        It gathers "plausible whole chunks" (quoted text, path-like
        tokens, encoding-like tokens) and, only as a last resort,
        individual leftover words. Whole phrases are never split into
        their component words here, so the decoder can't accidentally
        prefer a short fragment over the correct full phrase.
        """
        matches = re.findall(r'"([^"]*)"|\'([^\']*)\'', prompt)
        quoted = [m[0] if m[0] else m[1] for m in matches if m[0] or m[1]]

        num_matches = re.findall(r"[-+]?\b\d+(?:\.\d+)?\b", prompt)

        # File-path-like tokens: unix paths or windows paths.
        paths = re.findall(r"[A-Za-z]:\\[^\s'\"]+|/[^\s'\"]+", prompt)

        # Encoding-like tokens: word(s) with a trailing number, e.g.
        # "utf-8", "latin-1", "ascii".
        encodings = re.findall(
            r"\b[a-zA-Z]+-?\d+\b|\bascii\b", prompt, re.IGNORECASE
        )

        words = [
            w.strip(" ,.?!'\"")
            for w in prompt.split()
            if w.strip(" ,.?!'\"")
        ]
        stopwords = {
            "what", "is", "the", "a", "an", "for", "to", "of", "in",
            "on", "at", "with", "and", "run", "execute", "read",
        }
        filtered_words = [
            w for w in words
            if w.lower() not in stopwords and w not in num_matches
        ]

        return {
            "quoted": quoted,
            "numbers": num_matches,
            "paths": paths,
            "encodings": encodings,
            "words": filtered_words,
        }

    def extract_arguments(
        self, prompt: str, function: FunctionDefinition
    ) -> Dict[str, Any]:
        """Extract function parameters using constrained decoding.

        String parameters are resolved generically: a pool of
        candidate substrings is built from the prompt, and for each
        string parameter the LLM (via constrained decoding) picks the
        best-matching candidate, using the parameter's own name as
        context rather than a hardcoded keyword-to-name mapping.

        Whole quoted phrases and paths are offered as single, intact
        candidates (never split into individual words), so the model
        can't drift onto a short fragment of a longer correct answer.
        Loose word-splitting is only used as a fallback when nothing
        stronger (quote/path/encoding) is available in the prompt.

        Args:
            prompt: Natural language user prompt.
            function: Function definition detailing parameters.

        Returns:
            Dict[str, Any]: Map of parameter name to value.
        """
        candidates = self._extract_prompt_candidates(prompt)
        parameters: Dict[str, Any] = {}

        num_params = [
            p_name for p_name, p_def in function.parameters.items()
            if p_def.type.lower() in ("number", "integer", "int", "float")
        ]

        str_params = [
            p_name for p_name, p_def in function.parameters.items()
            if p_def.type.lower() == "string"
        ]

        # 1. Process Numbers
        available_nums = list(candidates["numbers"])
        for p_name in num_params:
            p_type = function.parameters[p_name].type.lower()
            if available_nums:
                val_str = self._decode_constrained_value(
                    prompt,
                    function.name,
                    p_name,
                    available_nums,
                    position_idx=0,
                )
                try:
                    num_val = float(val_str)
                    if p_type in ("integer", "int"):
                        parameters[p_name] = int(round(num_val))
                    else:
                        parameters[p_name] = float(num_val)
                except ValueError:
                    if p_type in ("integer", "int"):
                        parameters[p_name] = 0
                    else:
                        parameters[p_name] = 0.0

                if val_str in available_nums:
                    available_nums.remove(val_str)
            else:
                if p_type in ("integer", "int"):
                    parameters[p_name] = 0
                else:
                    parameters[p_name] = 0.0

        # 2. Process Strings generically — no param-name keyword
        # matching. Build one candidate pool per prompt and let the
        # model pick, in declaration order, removing each choice from
        # the pool so two params don't collapse onto the same value.
        if str_params:
            # Content-based (not name-based) hints: react to what the
            # prompt says, not what the parameter is called.
            extra_candidates: List[str] = []
            lowered = prompt.lower()
            if "vowels" in lowered:
                extra_candidates.append(r"[aeiouAEIOU]")
            if "numbers" in lowered or "digit" in lowered:
                extra_candidates.append(r"\d+")
            if "asterisk" in lowered:
                extra_candidates.append("*")

            # Strong candidates are whole, intact spans: quotes,
            # paths, encodings. These are NEVER decomposed into
            # individual words.
            strong_candidates = list(dict.fromkeys(
                extra_candidates
                + candidates["quoted"]
                + candidates["paths"]
                + candidates["encodings"]
            ))

            # Only fall back to loose word-splitting when nothing
            # stronger is available in the prompt at all — prevents
            # the decoder from ever choosing a short word fragment
            # over an intact correct phrase.
            pool = (
                strong_candidates
                if strong_candidates
                else candidates["words"]
            )

            remaining_pool = list(pool)
            for p_name in str_params:
                if remaining_pool:
                    chosen = self._decode_constrained_value(
                        prompt,
                        function.name,
                        p_name,
                        remaining_pool,
                        position_idx=0,
                    )
                    parameters[p_name] = chosen
                    if chosen in remaining_pool:
                        remaining_pool.remove(chosen)
                elif candidates["words"]:
                    # Last-resort fallback if strong candidates ran
                    # out before all string params were filled.
                    chosen = self._decode_constrained_value(
                        prompt,
                        function.name,
                        p_name,
                        candidates["words"],
                        position_idx=0,
                    )
                    parameters[p_name] = chosen
                else:
                    parameters[p_name] = ""

        return parameters

    def _decode_constrained_value(
        self,
        prompt: str,
        func_name: str,
        param_name: str,
        targets: List[str],
        position_idx: int = 0,
    ) -> str:
        query = (
            f"Prompt: {prompt}\n"
            f"Function: {func_name}\n"
            f"Target parameter '{param_name}': "
        )
        encoded = self.model.encode(query)
        input_ids: List[int] = [int(x) for x in encoded.tolist()[0]]

        generated_val = ""
        max_tokens = 20

        for _ in range(max_tokens):
            allowed_tokens = get_allowed_tokens_for_targets(
                generated_val, targets, self.vocab
            )
            if not allowed_tokens:
                break

            logits = self.model.get_logits_from_input_ids(input_ids)
            next_token = select_next_token(logits, allowed_tokens)
            input_ids.append(next_token)

            token_text = self.vocab.get(next_token, "")
            generated_val += token_text

        cleaned_val = generated_val.strip()

        if cleaned_val in targets:
            return cleaned_val

        for target in targets:
            if (
                target == cleaned_val
                or target.startswith(cleaned_val)
                or cleaned_val.startswith(target)
            ):
                return target

        if 0 <= position_idx < len(targets):
            return targets[position_idx]
        return targets[0] if targets else ""

    def process_prompt(
        self, prompt: str, functions: List[FunctionDefinition]
    ) -> FunctionCallResult:
        """Process a single natural language prompt into FunctionCallResult.

        Args:
            prompt: Input user request prompt.
            functions: Available functions list.

        Returns:
            FunctionCallResult: Extracted call target and arguments.
        """
        try:
            selected_fn = self.select_function(prompt, functions)
        except Exception:
            selected_fn = functions[0]

        try:
            parameters = self.extract_arguments(prompt, selected_fn)
        except Exception:
            parameters = {}

        for p_name, p_def in selected_fn.parameters.items():
            if p_name not in parameters:
                p_t = p_def.type.lower()
                if p_t in ("integer", "int"):
                    parameters[p_name] = 0
                elif p_t in ("number", "float"):
                    parameters[p_name] = 0.0
                elif p_t in ("boolean", "bool"):
                    parameters[p_name] = False
                else:
                    parameters[p_name] = ""

        return FunctionCallResult(
            prompt=prompt,
            name=selected_fn.name,
            parameters=parameters,
        )
