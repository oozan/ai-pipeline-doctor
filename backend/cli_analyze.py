import sys
import argparse
from core.analyzer import analyze_log

def main():
    parser = argparse.ArgumentParser(description="AI Pipeline Doctor CLI")
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path to CI/CD log file. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "--provider",
        "-p",
        type=str,
        default="auto",
        help="CI provider: github, gitlab, circleci, auto",
    )
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            log_text = f.read()
    else:
        log_text = sys.stdin.read()

    result = analyze_log(log_text, provider=args.provider)

    print("=== AI Pipeline Doctor ===")
    print(f"Provider:       {result.provider}")
    print(f"Category:       {result.error_category}")
    print(f"Primary error:  {result.primary_error}")
    if result.failed_command:
        print(f"Failed command: {result.failed_command}")
    print()
    print("Summary:")
    print(f"  {result.summary}")
    print()
    print("Suggested fixes:")
    for i, s in enumerate(result.suggested_fixes, start=1):
        print(f"  {i}. {s}")
    print()
    print(f"(Confidence: {result.confidence:.2f})")


if __name__ == "__main__":
    main()
