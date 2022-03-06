import configparser
from botocore.exceptions import ClientError
from tqdm import tqdm
import csv
import json
from decimal import Decimal


def csv_export(table, file):
    # read csv spec
    try:
        csv_spec = configparser.ConfigParser()
        csv_spec.read(f"{file}.spec")
    except Exception:
        return "CSV specification file can't read"

    # write csv
    try:
        with open(file, mode="w", encoding="utf_8") as f:
            print("please wait {name} exporting {file}".format(
                name=table.name, file=file))

            # scan table
            export_items = []
            parameters = {}
            try:
                while True:
                    response = table.scan(**parameters)
                    export_items.extend(response["Items"])
                    if ("LastEvaluatedKey" in response):
                        parameters["ExclusiveStartKey"] = response["LastEvaluatedKey"]
                    else:
                        break

            except ClientError:
                return "aws client error"
            except Exception:
                return "table not found"

            is_write_csv_header_labels = False
            for item in tqdm(export_items):

                if not is_write_csv_header_labels:
                    # write csv header labels
                    csv_header_labels = item.keys()
                    writer = csv.DictWriter(f, fieldnames=csv_header_labels, lineterminator="\n")
                    writer.writeheader()
                    is_write_csv_header_labels = True

                # updated dict to match specifications
                for key in item.keys():
                    spec = csv_spec.get("CSV_SPEC", key)
                    if spec == "S":  # String
                        item[key] = str(item[key])
                    elif spec == "I":  # Integer
                        item[key] = int(item[key])
                    elif spec == "D":  # Decimal
                        item[key] = float(item[key])
                    elif spec == "B":  # Boolean
                        if not item[key]:
                            item[key] = ""
                    elif spec == "J":  # Json
                        item[key] = json.dumps(item[key], default=decimal_encode)
                    elif spec == "SL":  # StringList
                        item[key] = " ".join(item[key])
                    elif spec == "DL":  # DecimalList
                        item[key] = " ".join(list(map(str, item[key])))
                    else:
                        pass

                writer.writerow(item)

        return "{name} csv exported {count} items".format(
            name=table.name, count=len(export_items))

    except IOError:
        print("I/O error")

    except Exception as e:
        return str(e)


def decimal_encode(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
