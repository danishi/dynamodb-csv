from botocore.exceptions import ClientError
from tqdm import tqdm
from typing import Tuple, List


def move(tables: List) -> Tuple:
    """DynamoDB table items move

    Args:
        tables (List): boto3 DynamoDB table objects

    Returns:
        Tuple: result message and exit code
    """

    from_table = tables[0]
    to_table = tables[1]

    # all scan move items
    move_items = []
    parameters = {}

    try:
        while True:
            response = from_table.scan(**parameters)
            move_items.extend(response["Items"])
            if ("LastEvaluatedKey" in response):
                parameters["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            else:
                break
    except ClientError as e:
        return (f"aws client error:{e}", 1)
    except Exception as e:
        return (f"table not found:{e}", 1)

    print("{name} scan {count} items".format(
        name=from_table.name, count=len(move_items)))

    # move all items
    try:
        with to_table.batch_writer() as batch:
            print("please wait {name} moving".format(name=to_table.name))

            for item in tqdm(move_items):
                batch.put_item(Item=item)

    except ClientError as e:
        return (f"aws client error:{e}", 1)
    except Exception as e:
        return (f"table not found:{e}", 1)

    return ("{name} moved {count} items".format(
        name=to_table.name, count=len(move_items)), 0)
