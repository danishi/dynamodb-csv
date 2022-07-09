import configparser
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from tqdm import tqdm
import csv
import json
from decimal import Decimal
from typing import Any, Tuple, Dict


def csv_export(table: Any, file: str, parameters: Dict = {}) -> Tuple:
    """Export DynamoDB table to csv

    Args:
        table (Table): boto3 DynamoDB table object
        file (str): csv file path

    Returns:
        Tuple: result message and exit code
    """

    # read csv spec
    try:
        csv_spec = configparser.ConfigParser()
        csv_spec.read(f"{file}.spec")
    except Exception:
        return ("CSV specification file can't read", 1)

    # write csv
    try:
        with open(file, mode="w", encoding="utf_8") as f:
            print("please wait {name} exporting {file}".format(
                name=table.name, file=file))

            export_items = []
            try:
                if "QUERY_OPTION" in csv_spec:
                    try:
                        # Partition key option
                        if "PKAttribute" in csv_spec["QUERY_OPTION"]:
                            pk_key = csv_spec.get("QUERY_OPTION", "PKAttribute")
                            pk_value = csv_spec.get("QUERY_OPTION", "PKAttributeValue")
                            pk_type = csv_spec.get("QUERY_OPTION", "PKAttributeType")
                            if pk_type == "I":
                                pk_value = int(pk_value)
                            parameters["KeyConditionExpression"] = Key(pk_key).eq(pk_value)

                        # Sort key option
                        if "SKAttribute" in csv_spec["QUERY_OPTION"]:
                            sk_key = csv_spec.get("QUERY_OPTION", "SKAttribute")
                            sk_values = csv_spec.get("QUERY_OPTION", "SKAttributeValues").split(",")
                            sk_type = csv_spec.get("QUERY_OPTION", "SKAttributeType")

                            if sk_type == "I":
                                sk_values = [int(v) for v in sk_values]

                            sk_values = sk_values[0] if len(sk_values) == 1 else sk_values

                            sk_expression = csv_spec.get("QUERY_OPTION", "SKAttributeExpression")
                            if sk_expression == "begins_with":
                                parameters["KeyConditionExpression"] &= Key(sk_key).begins_with(sk_values)
                            elif sk_expression == "between":
                                parameters["KeyConditionExpression"] &= Key(sk_key).between(sk_values[0], sk_values[1])
                            elif sk_expression == "eq":
                                parameters["KeyConditionExpression"] &= Key(sk_key).eq(sk_values)
                            elif sk_expression == "gt":
                                parameters["KeyConditionExpression"] &= Key(sk_key).gt(sk_values)
                            elif sk_expression == "gte":
                                parameters["KeyConditionExpression"] &= Key(sk_key).gte(sk_values)
                            elif sk_expression == "lt":
                                parameters["KeyConditionExpression"] &= Key(sk_key).lt(sk_values)
                            elif sk_expression == "lte":
                                parameters["KeyConditionExpression"] &= Key(sk_key).lte(sk_values)

                        # query table
                        while True:
                            response = table.query(**parameters)
                            export_items.extend(response["Items"])
                            if ("LastEvaluatedKey" in response):
                                parameters["ExclusiveStartKey"] = response["LastEvaluatedKey"]
                            else:
                                break
                    except Exception as e:
                        return ("query option error:" + str(e), 1)

                else:
                    # scan table
                    while True:
                        response = table.scan(**parameters)
                        export_items.extend(response["Items"])
                        if ("LastEvaluatedKey" in response):
                            parameters["ExclusiveStartKey"] = response["LastEvaluatedKey"]
                        else:
                            break
            except ClientError as e:
                return (f"aws client error:{e}", 1)
            except Exception:
                return ("table not found", 1)

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

        return ("{name} csv exported {count} items".format(
            name=table.name, count=len(export_items)), 0)

    except IOError:
        print("I/O error")

    except Exception as e:
        return (str(e), 1)


def decimal_encode(obj: Any) -> float:
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
