from app.dynamodb import truncate


def test_dynamodb_truncate():
    result = truncate("foo_table")
    assert result == "table not found"
