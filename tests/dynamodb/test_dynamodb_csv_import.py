from app.dynamodb import csv_import
from typing import Any


def test_dynamodb_csv_import(table: Any) -> None:
    """Unit test csv import into DynamoDB table

    Args:
        table (Any): boto3 DynamoDB table mock object
    """

    csv_file = "sample.csv"
    result = csv_import(table, csv_file)
    print(result)

    assert result[0] == "{name} csv imported {count} items".format(
        name=table.name, count=300)
