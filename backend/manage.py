import argparse

import uvicorn
from src.config.database import create_tables


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for managing the application"
    )
    subparsers = parser.add_subparsers(dest="command")

    migrate_parser = subparsers.add_parser(
        "migrate", help="Execute database migrations"
    )
    migrate_parser.set_defaults(func=create_tables)

    run_parser = subparsers.add_parser(
        "run", help="Create and start the FastAPI application"
    )
    run_parser.set_defaults(
        func=lambda: uvicorn.run(
            "src.config.app:app", host="0.0.0.0", port=8000, reload=True
        )
    )

    args = parser.parse_args()
    if args.command:
        args.func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
