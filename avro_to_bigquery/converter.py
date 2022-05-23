from google.cloud import bigquery  # type: ignore

AVRO_TO_BIGQUERY_TYPES = {
    "record": "RECORD",
    "string": "STRING",
    "int": "INTEGER",
    "boolean": "BOOL",
    "double": "FLOAT",
    "float": "FLOAT",
    "long": "INT64",
    "bytes": "BYTES",
    "enum": "STRING",
    # logical types
    "decimal": "FLOAT",
    "uuid": "STRING",
    "date": "DATE",
    "time-millis": "TIME",
    "time-micros": "TIME",
    "timestamp-millis": "TIMESTAMP",
    "timestamp-micros": "TIMESTAMP",
}


def _convert_type(avro_type):
    """
    Convert an Avro type to a BigQuery type
    :param avro_type: The Avro type
    :return: The BigQuery type
    """
    mode = "NULLABLE"
    fields = ()

    if isinstance(avro_type, list):
        # list types are unions, one of them should be null; get the real type
        if len(avro_type) == 2:
            if avro_type[0] == "null":
                avro_type = avro_type[1]
            elif avro_type[1] == "null":
                avro_type = avro_type[0]
            else:
                raise ReferenceError(
                    "One of the union fields should have type `null`"
                )
        else:
            raise ReferenceError(
                "A Union type can only consist of two types, "
                "one of them should be `null`"
            )

    if isinstance(avro_type, dict):
        field_type, fields, mode = _convert_complex_type(avro_type)

    else:
        field_type = AVRO_TO_BIGQUERY_TYPES[avro_type]

    return field_type, mode, fields


def _convert_complex_type(avro_type):
    """
    Convert a Avro complex type to a BigQuery type
    :param avro_type: The Avro type
    :return: The BigQuery type
    """
    fields = ()
    mode = "NULLABLE"

    if avro_type["type"] == "record":
        field_type = "RECORD"
        fields = tuple(map(lambda f: _convert_field(f), avro_type["fields"]))
    elif avro_type["type"] == "array":
        mode = "REPEATED"
        if "logicalType" in avro_type["items"]:
            field_type = AVRO_TO_BIGQUERY_TYPES[
                avro_type["items"]["logicalType"]
            ]
        elif isinstance(avro_type["items"], dict):
            # complex array
            if avro_type["items"]["type"] == "enum":
                field_type = AVRO_TO_BIGQUERY_TYPES[avro_type["items"]["type"]]
            else:
                field_type = "RECORD"
                fields = tuple(
                    map(
                        lambda f: _convert_field(f),
                        avro_type["items"]["fields"],
                    )
                )
        else:
            # simple array
            field_type = AVRO_TO_BIGQUERY_TYPES[avro_type["items"]]
    elif avro_type["type"] == "enum":
        field_type = AVRO_TO_BIGQUERY_TYPES[avro_type["type"]]
    elif avro_type["type"] == "map":
        field_type = "RECORD"
        mode = "REPEATED"
        # Create artificial fields to represent map in BQ
        key_field = {
            "name": "key",
            "type": "string",
            "doc": "Key for map avro field"
        }
        value_field = {
            "name": "value",
            "type": avro_type["values"],
            "doc": "Value for map avro field"
        }
        fields = tuple(map(lambda f: _convert_field(f),
                       [key_field, value_field]))
    elif "logicalType" in avro_type:
        field_type = AVRO_TO_BIGQUERY_TYPES[avro_type["logicalType"]]
    else:
        raise ReferenceError(f"Unknown complex type {avro_type['type']}")
    return field_type, fields, mode


def _convert_field(avro_field):
    """
    Convert an Avro field to a BigQuery field
    :param avro_field: The Avro field
    :return: The BigQuery field
    """

    if "logicalType" in avro_field:
        field_type, mode, fields = _convert_type(avro_field["logicalType"])
    else:
        field_type, mode, fields = _convert_type(avro_field["type"])

    return bigquery.SchemaField(
        avro_field.get("name"),
        field_type,
        mode=mode,
        description=avro_field.get("doc"),
        fields=fields,
    )


def convert_schema(avro_schema: dict):
    """
    Convert an Avro schema to a BigQuery schema
    :param avro_schema: The Avro schema
    :return: The BigQuery schema
    """

    return tuple(map(lambda f: _convert_field(f), avro_schema["fields"]))
