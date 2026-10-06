"""Day 6: check tool arguments against the JSON Schema
before calling the function.
"""


TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def validate_arguments(arguments, schema):
    """Return None when valid, or an error message when invalid."""

    # 1. Arguments must be a dictionary.
    if not isinstance(arguments, dict):
        return "Arguments must be a JSON object."

    properties = schema.get("properties", {})

    # 2. Check required arguments.
    for name in schema.get("required", []):
        if name not in arguments:
            return (
                f"Missing required argument '{name}'. "
                f"Expected: {', '.join(properties)}."
            )

    # 3. Check extra/invented arguments.
    if schema.get("additionalProperties") is False:
        extra = [
            key for key in arguments
            if key not in properties
        ]

        if extra:
            return (
                f"Unexpected argument(s): {', '.join(extra)}. "
                f"Allowed: {', '.join(properties)}."
            )

    # 4. Check data types and enum values.
    for name, value in arguments.items():

        rule = properties.get(name, {})

        expected = TYPES.get(rule.get("type"))

        if expected and not isinstance(value, expected):
            return (
                f"Argument '{name}' must be a "
                f"{rule['type']}, but got "
                f"{type(value).__name__}: {value!r}."
            )

        if "enum" in rule and value not in rule["enum"]:
            return (
                f"Argument '{name}' must be one of "
                f"{rule['enum']}, got {value!r}."
            )

    return None


if __name__ == "__main__":

    from tools_v2 import SCHEMAS

    schema = SCHEMAS["get_course_fee"]

    cases = [
        {"course_code": "CS101"},
        {"course_code": "CS101", "semester": "even"},
        {},
        {"course_code": 101},
        {"course_code": "CS101", "semester": "summer"},
        {"course_code": "CS101", "year": 2026},
    ]

    for case in cases:
        result = validate_arguments(case, schema)

        print(
            f"{str(case):<48} -> "
            f"{result or 'OK'}"
        )
        