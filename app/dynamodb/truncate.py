from botocore.exceptions import ClientError
from tqdm import tqdm
import logging

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

log_file = logging.FileHandler("app/logs/dynamodb_truncate.log")
format = "%(asctime)s %(levelname)s %(name)s :%(message)s"
log_file.setFormatter(logging.Formatter(format))

logger.addHandler(log_file)


def truncate(table):
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
        logger.error(e)
        return "aws client error"
    except Exception as e:
        logger.error(e)
        return "table not found"

    logger.debug(delete_items)
    print("{name} scan {count} items".format(
        name=table.name, count=len(delete_items)))

    # get key attribute name and item delete keys
    key_names = [x["AttributeName"] for x in table.key_schema]
    delete_keys = [{k: v for k, v in x.items() if k in key_names}
                   for x in delete_items]

    logger.debug(key_names)
    logger.debug(delete_keys)

    # delete all items
    with table.batch_writer() as batch:
        print("please wait {name} truncating".format(name=table.name))

        for key in tqdm(delete_keys):
            batch.delete_item(Key=key)

    return "{name} truncated".format(name=table.name)
