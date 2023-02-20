from app.dynamodb import move
from typing import Any


def test_dynamodb_move(table: Any) -> None:
    """Unit test DynamoDB table move

    Args:
        table (Any): boto3 DynamoDB table mock object
    """

    tables = [table, table]
    result = move(tables)

    assert result[0] == "{name} moved {count} items".format(
        name=table.name, count=1297)
