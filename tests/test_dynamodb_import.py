from app.dynamodb_import import csv_import


def test_csv_import():
    result = csv_import("foo_table", "foo_file")
    assert result == "CSV file can't read"
