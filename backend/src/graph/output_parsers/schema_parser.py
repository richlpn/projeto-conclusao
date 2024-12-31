from abc import ABC
from typing import Generic, TypeVar
from langchain_core.output_parsers import JsonOutputParser

T = TypeVar("T")


class SchemaParser(JsonOutputParser, Generic[T], ABC):

    def filter_properties(self, properties: dict) -> dict:
        """
        Filters out properties containing 'id' or with a 'uuid' format.

        This method takes a dictionary of properties and returns a new dictionary
        with properties whose keys contain 'id' (case-insensitive) or have a 'uuid'
        format removed.

        Args:
            properties (dict): The input dictionary of properties to be filtered.

        Returns:
            dict: The filtered dictionary of properties.

        Raises:
            None
        """
        # Remove keys containing "id" or with the format "uuid"
        return {
            key: value
            for key, value in properties.items()
            if "id" not in key.lower() and value.get("format") != "uuid"
        }

    def process_object(self, obj: dict) -> dict:
        """
        Processes a JSON schema object by filtering its properties and nested definitions.

        This method recursively traverses the input object, filtering out properties
        containing 'id' and removing 'id' attributes from the 'required' list. It also
        processes any nested definitions in the '$defs' section.

        Args:
            obj (dict): The input JSON schema object to be processed.

        Returns:
            dict: The processed JSON schema object.

        Raises:
            None
        """
        # Remove ID's attributes from the object
        if "properties" in obj:
            obj["properties"] = self.filter_properties(obj["properties"])

        if "required" in obj:
            obj["required"] = [
                attr for attr in obj["required"] if "id" not in attr.lower()
            ]

        # If there are nested definitions, process them recursively
        if "$defs" in obj:
            obj["$defs"] = {
                key: self.process_object(value) for key, value in obj["$defs"].items()
            }
        return obj

    def remove_id_properties(self, schema: dict) -> dict:
        return self.process_object(schema.copy())
