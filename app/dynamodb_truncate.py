import boto3
from botocore.exceptions import ClientError
import configparser
import argparse
from tqdm import tqdm
import logging

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

log_file = logging.FileHandler("app/logs/dynamodb_truncate.log")
format = "%(asctime)s %(levelname)s %(name)s :%(message)s"
log_file.setFormatter(logging.Formatter(format))

logger.addHandler(log_file)


def main():
    # arguments parse
    parser = argparse.ArgumentParser(description="DynamoDB truncate table")
    parser.add_argument("table", help="DynamoDB table name")
    args = parser.parse_args()

    # boto3 config setting
    config = configparser.ConfigParser()
    config.read("config.ini")

    logger.debug(config.items("AWS"))

    dynamodb = boto3.resource("dynamodb",
        region_name=config.get("AWS", "REGION"),
        aws_access_key_id=config.get("AWS", "AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=config.get("AWS", "AWS_SECRET_ACCESS_KEY"))

    table = dynamodb.Table(args.table)

    # truncate table
    return truncate(table)


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


if __name__ == "__main__":
    result = main()
    print(result)
