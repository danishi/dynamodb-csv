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
        csv_spec.optionxform = str
        csv_spec.read(f"{file}.spec")
    except Exception as e:
        return (f"CSV specification file can't read:{e}", 1)

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
                        return (f"query option error:{e}", 1)

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
            except Exception as e:
                return (f"table not found:{e}", 1)

            is_write_csv_header_labels = False
            for item in tqdm(export_items):

                if not is_write_csv_header_labels:
                    # write csv header labels
                    csv_header_labels = list(csv_spec["CSV_SPEC"])
                    writer = csv.DictWriter(f, fieldnames=csv_header_labels, lineterminator="\n")
                    writer.writeheader()
                    is_write_csv_header_labels = True

                # updated dict to match specifications
                for key in list(item.keys()):
                    try:
                        spec = csv_spec.get("CSV_SPEC", key)
                    except Exception:
                        # Removed attributes that do not match the specifications
                        del item[key]
                        continue

                    item[key] = convert_item(spec, item, key)

                writer.writerow(item)

        return ("{name} csv exported {count} items".format(
            name=table.name, count=len(export_items)), 0)

    except IOError as e:
        print(f"I/O error:{e}")

    except Exception as e:
        return (str(e), 1)


def convert_item(spec: str, item: Dict, key: str) -> Any:
    """convert item

    Args:
        spec (str): type of item
        row (Dict): row data
        key (str): key

    Returns:
        Any: converted item value
    """
    if spec == "S":  # String
        return str(item[key])
    elif spec == "I":  # Integer
        return int(item[key])
    elif spec == "D":  # Decimal
        return float(item[key])
    elif spec == "B":  # Boolean
        if not item[key]:
            return ""
    elif spec == "J":  # Json
        return json.dumps(item[key], default=decimal_encode)
    elif spec == "SL" or spec == "SS":  # StringList or StringSet
        return " ".join(item[key])
    elif spec == "DL" or spec == "DS":  # DecimalList or DecimalSetDecimalList
        return " ".join(list(map(str, item[key])))
    else:
        return item[key]


def decimal_encode(obj: Any) -> float:
    """encode decimal

    Args:
        obj (Any): object

    Raises:
        TypeError: Not decimal object

    Returns:
        float: decimal object
    """
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
