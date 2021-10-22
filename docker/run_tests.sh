#!/usr/bin/env bash

set -eo pipefail

BLACK_ACTION="--check"
ISORT_ACTION="--check-only"

function usage
{
    echo "usage: run_tests.sh [--format-code]"
    echo ""
    echo " --format-code : Format the code instead of checking formatting."
    exit 1
}

while [[ $# -gt 0 ]]; do
    arg="$1"
    case $arg in
        --format-code)
        BLACK_ACTION="--quiet"
        ISORT_ACTION=""
        ;;
        -h|--help)
        usage
        ;;
        "")
        # ignore
        ;;
        *)
        echo "Unexpected argument: ${arg}"
        usage
        ;;
    esac
    shift
done

# only generate html locally
pytest tests/unit --cov-report html

echo "Running MyPy..."
mypy avro_to_bigquery tests

echo "Running black..."
black ${BLACK_ACTION} avro_to_bigquery tests

echo "Running iSort..."
isort ${ISORT_ACTION} avro_to_bigquery tests

echo "Running flake8..."
flake8 avro_to_bigquery tests

echo "Running bandit..."
bandit --ini .bandit --quiet -r avro_to_bigquery
