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
                    try:
                        if spec == "S":  # String
                            row[key] = str(row[key])
                        elif spec == "I":  # Integer
                            row[key] = int(row[key])
                        elif spec == "D":  # Decimal
                            row[key] = Decimal(row[key])
                        elif spec == "B":  # Boolean
                            row[key] = bool(row[key])
                        elif spec == "J":  # Json
                            row[key] = json.loads(row[key], parse_float=Decimal)
                        elif spec == "SL":  # StringList
                            row[key] = row[key].split()
                        elif spec == "DL":  # DecimalList
                            row[key] = list(map(Decimal, row[key].split()))
                        else:
                            pass
                    except Exception:
                        del row[key]

                batch.append(row)

            if(len(batch)) > 0:
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
