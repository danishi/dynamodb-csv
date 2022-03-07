from app.dynamodb import truncate


def test_dynamodb_truncate(table):
    result = truncate(table)
    print(result)

    assert result == "{name} truncated".format(name=table.name)
