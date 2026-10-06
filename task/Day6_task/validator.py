# validator.py

"""
Simple JSON-schema-style validator for the Day 6 task.

The validator uses the same SCHEMAS dictionary that is sent
to the model.
"""

from tools import SCHEMAS


def validate_arguments(tool_name, arguments):
    """
    Validate tool arguments against the schema.

    Returns:
        None -> arguments are valid
        str  -> error message
    """

    # -----------------------------------------------------
    # Check whether the tool exists
    # -----------------------------------------------------

    if tool_name not in SCHEMAS:
        return (
            f"Validation error: unknown tool '{tool_name}'. "
            f"Expected one of: {list(SCHEMAS.keys())}."
        )

    schema = SCHEMAS[tool_name]

    # -----------------------------------------------------
    # Arguments must be a dictionary
    # -----------------------------------------------------

    if not isinstance(arguments, dict):
        return (
            "Validation error: arguments must be a JSON object "
            "containing named fields."
        )

    properties = schema.get("properties", {})
    required = schema.get("required", [])
    allow_extra = schema.get("additionalProperties", True)

    # -----------------------------------------------------
    # Check missing required arguments
    # -----------------------------------------------------

    for field in required:

        if field not in arguments:

            return (
                f"Validation error: missing required argument "
                f"'{field}'. Expected fields: {required}."
            )

    # -----------------------------------------------------
    # Check invented / extra arguments
    # -----------------------------------------------------

    if allow_extra is False:

        for field in arguments:

            if field not in properties:

                return (
                    f"Validation error: unexpected argument "
                    f"'{field}'. Expected only: "
                    f"{list(properties.keys())}."
                )

    # -----------------------------------------------------
    # Check every supplied field
    # -----------------------------------------------------

    for field, value in arguments.items():

        if field not in properties:
            continue

        field_schema = properties[field]

        expected_type = field_schema.get("type")

        # -------------------------------------------------
        # Type checking
        # -------------------------------------------------

        if expected_type == "string":

            if not isinstance(value, str):

                return (
                    f"Validation error: '{field}' must be a string. "
                    f"Received {type(value).__name__}."
                )

        elif expected_type == "number":

            # bool is technically a subclass of int in Python,
            # so explicitly reject it.
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
            ):

                return (
                    f"Validation error: '{field}' must be a number. "
                    f"Received {type(value).__name__}."
                )

        elif expected_type == "integer":

            if (
                not isinstance(value, int)
                or isinstance(value, bool)
            ):

                return (
                    f"Validation error: '{field}' must be an integer. "
                    f"Received {type(value).__name__}."
                )

        # -------------------------------------------------
        # Enum checking
        # -------------------------------------------------

        allowed_values = field_schema.get("enum")

        if allowed_values is not None:

            if value not in allowed_values:

                return (
                    f"Validation error: '{field}' has invalid value "
                    f"'{value}'. Expected one of: "
                    f"{allowed_values}."
                )

    # -----------------------------------------------------
    # Everything passed
    # -----------------------------------------------------

    return None


# ---------------------------------------------------------
# SMALL TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("VALID:")
    print(
        validate_arguments(
            "get_weather",
            {
                "city": "Chennai",
                "unit": "C"
            }
        )
    )

    print("\nMISSING ARGUMENT:")
    print(
        validate_arguments(
            "get_weather",
            {
                "city": "Chennai"
            }
        )
    )

    print("\nEXTRA ARGUMENT:")
    print(
        validate_arguments(
            "get_weather",
            {
                "city": "Chennai",
                "unit": "C",
                "temperature": 30
            }
        )
    )

    print("\nWRONG TYPE:")
    print(
        validate_arguments(
            "get_weather",
            {
                "city": 123,
                "unit": "C"
            }
        )
    )

    print("\nINVALID ENUM:")
    print(
        validate_arguments(
            "get_weather",
            {
                "city": "Chennai",
                "unit": "K"
            }
        )
    )
    