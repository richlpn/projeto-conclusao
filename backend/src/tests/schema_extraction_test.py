import json
from typing import Final
from src.tools.extract_docs_schema_tool import extract_schema

TEST_ID = "SCHEMA"


def extract_and_save_schema():
    file_path: Final[str] = "static/data/docs/familias_atendidas_fomento_rural.txt"
    output_path: Final[str] = "static/data/schema_output.json"

    try:
        schema = extract_schema.invoke(file_path)
        with open(output_path, "w", encoding="utf8") as f:
            json.dump(schema.model_dump(), f, indent=4, ensure_ascii=False)
        print(f"Schema extracted and saved to {output_path}")
    except Exception as e:
        print(f"Error extracting schema: {str(e)}")


def main():
    extract_and_save_schema()
