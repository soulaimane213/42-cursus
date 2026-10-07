"""Entry point for the function calling system."""
try:
    import argparse
    import sys
    from typing import List

    from llm_sdk import Small_LLM_Model

    from .engine import ConstrainedFunctionCallingEngine
    from .models import FunctionCallResult
    from .parser import (
        load_function_definitions,
        load_test_prompts,
        save_results,
    )
except BaseException as e:
    print(e)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Function calling with constrained decoding"
    )
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to function definitions JSON file",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to input prompts JSON file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path for output results JSON file",
    )
    return parser.parse_args()


def main() -> None:
    """Run the function calling pipeline using the real LLM."""
    try:
        args: argparse.Namespace = parse_args()

        try:
            functions = load_function_definitions(args.functions_definition)
        except Exception as e:
            print(f"Error loading function definitions: {e}", file=sys.stderr)
            return

        if not functions:
            print("Error: No valid functions found.", file=sys.stderr)
            return

        try:
            tests = load_test_prompts(args.input)
        except Exception as e:
            print(f"Error loading test prompts: {e}", file=sys.stderr)
            return

        if not tests:
            print("Error: No valid test prompts found.", file=sys.stderr)
            return

        try:
            model = Small_LLM_Model()
            engine = ConstrainedFunctionCallingEngine(model)
        except Exception as e:
            print(f"Error initializing LLM engine: {e}", file=sys.stderr)
            return

        results: List[FunctionCallResult] = []
        for test in tests:
            try:
                result: FunctionCallResult = engine.process_prompt(
                    test.prompt, functions
                )
                results.append(result)
            except Exception as e:
                print(
                    f"Error processing prompt '{test.prompt}': {e}",
                    file=sys.stderr,
                )

        try:
            if not save_results(results, args.output):
                print(
                    f"Error: Could not save results to {args.output}",
                    file=sys.stderr,
                )
        except Exception as e:
            print(f"Error saving results: {e}", file=sys.stderr)

    except KeyboardInterrupt:
        print("Program interrupted by user.", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error in execution pipeline: {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(e)
