import configparser
from tqdm import tqdm
import csv
import json
from decimal import Decimal
from typing import Any, Dict, Tuple

count = 0
error_count = 0


def csv_import(table: Any, file: str, ignore: bool = False) -> Tuple:
    """csv import into DynamoDB table

    Args:
        table (Any): boto3 DynamoDB table object
        file (str): csv file path
        ignore (bool): ignore put item error

    Returns:
        Tuple: result message and exit code
    """

    # read csv spec
    try:
        csv_spec = configparser.ConfigParser()
        csv_spec.optionxform = str
        csv_spec.read(f"{file}.spec")
    except Exception as e:
        return (f"CSV specification file can't read:{e}", 1)

    # read csv
    try:
        with open(file, mode="r", encoding="utf_8") as f:
            reader = csv.DictReader(f)

            # batch_size = 100
            batch = []

            print("please wait {name} importing {file}".format(
                name=table.name, file=file))
            for row in tqdm(reader):
                # No use buffer
                # if len(batch) >= batch_size:
                #     write_to_dynamo(table, batch)
                #     batch.clear()

                # updated dict to match specifications
                for key in list(row.keys()):
                    spec = csv_spec.get("CSV_SPEC", key)

                    # Convert blank value
                    if "IMPORT_OPTION" in csv_spec:
                        if "ConvertBlankToNullAttrs" in csv_spec["IMPORT_OPTION"] and not row[key]:
                            to_null_attrs = csv_spec.get("IMPORT_OPTION", "ConvertBlankToNullAttrs").split(",")
                            if key in to_null_attrs:
                                row[key] = None
                                continue

                        if "ConvertBlankToDropAttrs" in csv_spec["IMPORT_OPTION"] and not row[key]:
                            to_drop_attrs = csv_spec.get("IMPORT_OPTION", "ConvertBlankToDropAttrs").split(",")
                            if key in to_drop_attrs:
                                del row[key]
                                continue

                    try:
                        row[key] = convert_column(spec, row, key)
                    except Exception:
                        del row[key]

                batch.append(row)

            if (len(batch)) > 0:
                write_to_dynamo(table, batch, ignore)

        if ignore:
            message = "{name} csv imported {count} items and {error_count} error items".format(
                name=table.name, count=count, error_count=error_count)
        else:
            message = "{name} csv imported {count} items".format(
                name=table.name, count=count)
        return (message, 0)

    except Exception as e:
        return (f"CSV file can't read:{e}", 1)


def convert_column(spec: str, row: Dict, key: str) -> Any:
    """convert column

    Args:
        spec (str): type of column
        row (Dict): row data
        key (str): key

    Returns:
        Any: converted column value
    """
    if spec == "S":  # String
        return str(row[key])
    elif spec == "I":  # Integer
        return int(row[key])
    elif spec == "D":  # Decimal
        return Decimal(row[key])
    elif spec == "B":  # Boolean
        return bool(row[key])
    elif spec == "J":  # Json
        return json.loads(row[key], parse_float=Decimal)
    elif spec == "SL":  # StringList
        return row[key].split()
    elif spec == "SS":  # StringSet
        return set(row[key].split())
    elif spec == "DL":  # DecimalList
        return list(map(Decimal, row[key].split()))
    elif spec == "DS":  # DecimalSet
        return set(list(map(Decimal, row[key].split())))
    else:
        return row[key]


def write_to_dynamo(table: Any, rows: Dict, ignore: bool = False) -> None:
    """csv rows into DynamoDB

    Args:
        table (Any): boto3 DynamoDB table object
        rows (Dict): csv rows
        ignore (bool): ignore put item error
    """
    global count
    global error_count

    # Ignore error item
    if ignore:
        for i in tqdm(range(len(rows))):
            try:
                table.put_item(
                    Item=rows[i]
                )
                count = count + 1
            except Exception:
                error_count = error_count + 1

    # Batch write
    else:
        try:
            # overwrite duplicate key item
            key_names = [x["AttributeName"] for x in table.key_schema]
            with table.batch_writer(overwrite_by_pkeys=key_names) as batch:
                for i in tqdm(range(len(rows))):
                    batch.put_item(
                        Item=rows[i]
                    )
                    count = count + 1

        except Exception as e:
            print(f"Error executing batch_writer:{e}")
