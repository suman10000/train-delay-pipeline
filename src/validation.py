
def validate_payload(payload):
    """
    Check the basic structure of the MBTA JSON response.
    Raise ValueError if the response is malformed.
    """

    if not isinstance(payload, dict):
        raise ValueError("Payload must be a JSON object.")

    if "data" not in payload:
        raise ValueError("Payload is missing the 'data' field.")

    records = payload["data"]

    if not isinstance(records, list):
        raise ValueError("'data' must contain a list.")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(
                f"Record {index} must be a JSON object."
            )

        if "id" not in record:
            raise ValueError(
                f"Record {index} is missing its ID."
            )

        if "attributes" not in record:
            raise ValueError(
                f"Record {index} is missing attributes."
            )

        if not isinstance(record["attributes"], dict):
            raise ValueError(
                f"Record {index} attributes must be an object."
            )

    return records
