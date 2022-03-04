from app.dynamodb_truncate import truncate


def test_csv_import():
    result = truncate("foo_table")
    assert result == "table not found"
