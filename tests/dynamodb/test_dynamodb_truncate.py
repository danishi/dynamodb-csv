from app.dynamodb import truncate
from typing import Any


def test_dynamodb_truncate(table: Any):
    """Unit test DynamoDB table truncate

    Args:
        table (Any): boto3 DynamoDB table mock object
    """

    result = truncate(table)
    print(result)

    assert result == "{name} truncated".format(name=table.name)