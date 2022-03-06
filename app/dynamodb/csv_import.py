import configparser
from tqdm import tqdm
import csv
import json
from decimal import Decimal

count = 0


def csv_import(table, file):
    # read csv spec
    try:
        csv_spec = configparser.ConfigParser()
        csv_spec.read(f"{file}.spec")
    except Exception:
        return "CSV specification file can't read"

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
                for key in row.keys():
                    spec = csv_spec.get("CSV_SPEC", key)
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

                batch.append(row)

            if(len(batch)) > 0:
                write_to_dynamo(table, batch)

        return "{name} csv imported {count} items".format(
            name=table.name, count=count)

    except Exception:
        return "CSV file can't read"


def write_to_dynamo(table, rows):
    global count

    try:
        # overwrite duplicate key item
        key_names = [x["AttributeName"] for x in table.key_schema]
        with table.batch_writer(overwrite_by_pkeys=key_names) as batch:
            for i in tqdm(range(len(rows))):
                batch.put_item(
                    Item=rows[i]
                )
                count = count + 1

    except Exception:
        print("Error executing batch_writer")
