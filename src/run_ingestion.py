
import logging
import sys

from src.ingestion import run_ingestion


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main():
    try:
        output_path = run_ingestion()
        print(f"\nIngestion completed: {output_path}")

    except Exception:
        logging.exception("Ingestion failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
