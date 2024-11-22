import argparse
import src.tests as tests


def run_test(test_name):
    try:
        if hasattr(tests, test_name):
            test_module = getattr(tests, test_name)
            test_module.main()
        else:
            print(f"Test {test_name} does not have a main function.")
    except ImportError:
        print(f"Test {test_name} not found.")


def main():
    parser = argparse.ArgumentParser(description="Run tests")
    parser.add_argument(
        "test_name", type=str, nargs="?", default="all", help="Name of the test to run"
    )
    args = parser.parse_args()

    tests = [
        "review_script_test",
        "schema_extraction_test",
        "script_generation_test",
        "task_creation_test",
    ]

    if args.test_name == "all":
        for test in tests:
            print(f"Running test {test}...")
            run_test(test)
    elif args.test_name in tests:
        print(f"Running test {args.test_name}...")
        run_test(args.test_name)
    else:
        print(f"Test {args.test_name} not found.")


if __name__ == "__main__":
    main()
