from app.dynamodb import truncate


def test_dynamodb_truncate(table):
    """Unit test DynamoDB table truncate

    Args:
        table (Table): boto3 DynamoDB table mock object
    """

    result = truncate(table)
    print(result)

    assert result == "{name} truncated".format(name=table.name)
