from app.dynamodb import csv_export
from typing import Any


def test_dynamodb_csv_export(table: Any) -> None:
    """Unit test export DynamoDB table to csv

    Args:
        table (Any): boto3 DynamoDB table mock object
    """

    size = 1000
    output_file = "sample_exp.csv"

    result = csv_export(table, output_file)
    print(result)

    assert result[0] == "{name} csv exported {count} items".format(
        name=table.name, count=size)


def test_dynamodb_csv_export_with_gsi(table: Any) -> None:
    """Unit test export DynamoDB table to csv with gsi

    Args:
        table (Any): boto3 DynamoDB table mock object
    """

    size = 1000
    output_file = "sample_exp.csv"
    parameters = {"IndexName": "NumberSK-index"}

    result = csv_export(table, output_file, parameters)
    print(result)

    assert result[0] == "{name} csv exported {count} items".format(
        name=table.name, count=size)
