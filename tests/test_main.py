from app import main
from typing import Any
import pytest


def test_parse_args_version(mocker: Any):
    """Unit test argparse

    Args:
        mocker (Any): mock object
    """

    mocker.patch("sys.argv", ["dynamodb-csv", "-v"])
    with pytest.raises(SystemExit) as e:
        main.main()

    assert e.value.code == 0


def test_parse_args_import(mocker: Any):
    """Unit test argparse mode import

    Args:
        mocker (Any): mock object
    """

    mocker.patch("sys.argv", [
        "dynamodb-csv", "-i", "-t", "test_table"
    ])
    result = main.main()

    assert result == "Import mode requires a input file option."


def test_parse_args_export(mocker: Any):
    """Unit test argparse mode export

    Args:
        mocker (Any): mock object
    """

    mocker.patch("sys.argv", [
        "dynamodb-csv", "-e", "-t", "test_table"
    ])
    result = main.main()

    assert result == "Export mode requires a output file option."


def test_config_file_not_exists(mocker: Any):
    """Unit test config file not exists

    Args:
        mocker (Any): mock object
    """

    mocker.patch("sys.argv", [
        "dynamodb-csv", "-i", "-t", "test_table", "-f", "sample.csv"
    ])
    mocker.patch("os.path.isfile", return_value=False)
    result = main.main()

    assert result == "Please make your config.ini file"
