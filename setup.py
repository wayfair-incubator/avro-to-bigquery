#!/usr/bin/env python

# We still need a setup.py shim so we can still pip install -e .
# https://snarky.ca/what-the-heck-is-pyproject-toml/#how-to-use-pyproject-toml-with-setuptools

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="avro-to-bigquery",
        version="0.5.0",
        packages=["avro_to_bigquery"],
        author="isaac",
        license="",
        author_email="fellipe.wurthmann@isaac.com.br",
        description="Avro to BigQuery library",
        python_requires="==3.12"
    )
