# Avro to Bigquery

[![CI pipeline status](https://github.com/wayfair-incubator/avro-to-bigquery/workflows/CI/badge.svg?branch=main)](https://github.com/wayfair-incubator/avro-to-bigquery/actions/workflows/main.yml)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/wayfair-incubator/avro-to-bigquery/blob/main/CODE_OF_CONDUCT.md)

## About The Project

Avro to bigquery is a simple project to create a bigquery schema from an avro schema.

## Getting Started

### Installation`

   ```sh
   pip install avro-to-bigquery
   ```

## Usage

With avro_schema.avsc:

```json
{
    "type": "record",
    "name": "User",
    "namespace": "example.avro",
    "fields": [
        {"name": "favorite_number", "type": "int", "doc": "Favorite number"}
    ]
}
```

```python
>>> import json
>>> from pathlib import Path
>>> from avro_to_bigquery import convert_schema
>>> schema = json.loads(Path("avro_schema.avsc").read_text())
>>> print(convert_schema(schema))
(SchemaField('favorite_number', 'INTEGER', 'NULLABLE', 'Favorite number', (), ()),)
```

## Roadmap

See the [open issues](https://github.com/wayfair-incubator/avro-to-bigquery/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. For detailed contributing guidelines, please see [https://github.com/wayfair-incubator/avro-to-bigquery/blob/main/CONTRIBUTING.md](CONTRIBUTING.md)

## License

Distributed under the `MIT` License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/wayfair-incubator/avro-to-bigquery/](https://github.com/wayfair-incubator/avro-to-bigquery/)
