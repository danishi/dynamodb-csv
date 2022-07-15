from botocore.exceptions import ClientError
from tqdm import tqdm
from typing import Any, Tuple


def truncate(table: Any) -> Tuple:
    """DynamoDB table truncate

    Args:
        table (Any): boto3 DynamoDB table object

    Returns:
        Tuple: result message and exit code
    """

    # all scan delete items
    delete_items = []
    parameters = {}

    try:
        while True:
            response = table.scan(**parameters)
            delete_items.extend(response["Items"])
            if ("LastEvaluatedKey" in response):
                parameters["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            else:
                break
    except ClientError as e:
        return (f"aws client error:{e}", 1)
    except Exception as e:
        return (f"table not found:{e}", 1)

    print("{name} scan {count} items".format(
        name=table.name, count=len(delete_items)))

    # get key attribute name and item delete keys
    key_names = [x["AttributeName"] for x in table.key_schema]
    delete_keys = [{k: v for k, v in x.items() if k in key_names}
                for x in delete_items]

    # delete all items
    with table.batch_writer() as batch:
        print("please wait {name} truncating".format(name=table.name))

        for key in tqdm(delete_keys):
            batch.delete_item(Key=key)

    return ("{name} truncated".format(name=table.name), 0)
