import pytest

from avro_to_bigquery import convert_schema


def test_convert_avro_schema_to_bigquery_schema():
    # arrange
    avs = {
        "type": "record",
        "name": "Test_Schema",
        "namespace": "example.avro",
        "fields": [
            {"name": "full_name", "type": "string", "doc": "The name"},
            {"name": "age", "type": "int", "doc": "The age"},
            {
                "name": "check",
                "type": "boolean",
                "doc": "Just a boolean tester",
            },
            {"name": "length", "type": "float", "doc": "The length"},
            {"name": "shoe_size", "type": "long", "doc": "The shoe size"},
            {"name": "image", "type": "bytes"},
            {"name": "complex", "type": ["double", "null"]},
            {"name": "size", "type": "double"},
            {
                "name": "sub",
                "type": {
                    "type": "record",
                    "name": "sub",
                    "fields": [
                        {"name": "sub1", "type": "long"},
                        {"name": "sub2", "type": "int"},
                        {
                            "name": "sub_sub",
                            "type": {
                                "type": "record",
                                "name": "sub_sub",
                                "fields": [
                                    {"name": "sub_sub1", "type": "boolean"},
                                    {"name": "sub_sub2", "type": "float"},
                                ],
                            },
                        },
                    ],
                },
            },
            {
                "name": "dimensions",
                "type": {
                    "type": "array",
                    "default": [],
                    "items": {
                        "type": "record",
                        "name": "dimensions",
                        "fields": [
                            {"name": "width", "type": "double"},
                            {"name": "length", "type": "double"},
                            {
                                "name": "timestamp",
                                "type": {
                                    "type": "long",
                                    "logicalType": "timestamp-millis",
                                },
                            },
                        ],
                    },
                },
            },
            {
                "name": "birthdate",
                "type": {"type": "int", "logicalType": "date"},
            },
            {
                "name": "timestamp",
                "type": {"type": "long", "logicalType": "time-micros"},
            },
            {
                "name": "nullable array",
                "doc": "A test array",
                "type": ["null", {"type": "array", "items": "int"}],
            },
            {
                "name": "logical type array",
                "type": [
                    "null",
                    {
                        "type": "array",
                        "items": {"type": "int", "logicalType": "date"},
                    },
                ],
            },
            {
                "name": "enumeration",
                "type": [
                    "null",
                    {
                        "type": "enum",
                        "name": "enum-test-field",
                        "symbols": ["Test1", "Test2", "Test3"],
                    },
                ],
            },
            {"name": "map_field", "type": {"type": "map", "values": "int"}},
            {
                "name": "complex_map",
                "type": {
                    "type": "map",
                    "values": {"type": "array", "items": "int"},
                },
            },
        ],
    }

    # act
    s = convert_schema(avs)

    # assert
    assert len(s) == 17
    assert s[0].name == "full_name"
    assert s[1].field_type == "INTEGER"
    assert s[2].description == "Just a boolean tester"
    assert s[3].mode == "NULLABLE"
    assert s[4].name == "shoe_size"
    assert s[5].description is None
    assert s[6].field_type == "FLOAT"
    assert s[7].field_type == "FLOAT"
    assert s[8].field_type == "RECORD"
    assert s[8].fields[0].name == "sub1"
    assert s[8].fields[2].fields[1].name == "sub_sub2"
    assert s[9].field_type == "RECORD"
    assert s[9].mode == "REPEATED"
    assert s[9].fields[0].field_type == "FLOAT"
    assert s[9].fields[2].field_type == "TIMESTAMP"
    assert s[10].field_type == "DATE"
    assert s[11].field_type == "TIME"
    assert s[12].name == "nullable array"
    assert s[12].field_type == "INTEGER"
    assert s[12].mode == "REPEATED"
    assert s[13].name == "logical type array"
    assert s[13].field_type == "DATE"
    assert s[13].mode == "REPEATED"
    assert s[14].field_type == "STRING"
    assert s[15].name == "map_field"
    assert s[15].field_type == "RECORD"
    assert s[15].mode == "REPEATED"
    assert s[15].fields[0].field_type == "STRING"
    assert s[15].fields[1].field_type == "INTEGER"
    assert s[15].fields[0].name == "key"
    assert s[15].fields[1].name == "value"
    assert s[16].fields[0].field_type == "STRING"
    assert s[16].fields[1].field_type == "INTEGER"
    assert s[16].fields[1].mode == "REPEATED"


def test_incorrect_nullable_field():
    # arrange
    avs = {
        "type": "record",
        "name": "Test_Schema",
        "namespace": "example.avro",
        "fields": [
            {
                "name": "test1",
                "type": ["double", "null"],
                "doc": "Correct nullable field",
            },
            {
                "name": "test2",
                "type": ["double", "string"],
                "doc": "Incorrect nullable field",
            },
        ],
    }

    # act
    with pytest.raises(ReferenceError) as re:
        convert_schema(avs)

        # assert
        assert "One of the union fields should have type `null`" in re.value


def test_incorrect_field_type():
    # arrange
    avs = {
        "type": "record",
        "name": "Test_Schema",
        "namespace": "example.avro",
        "fields": [
            {"name": "test1", "type": "string", "doc": "Correct field type"},
            {
                "name": "test2",
                "type": "something_useless",
                "doc": "Incorrect field type",
            },
        ],
    }

    # act
    with pytest.raises(KeyError):

        # assert
        convert_schema(avs)
