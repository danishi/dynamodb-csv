from app.dynamodb import csv_import
import boto3
from moto import mock_dynamodb2


@mock_dynamodb2
def test_dynamodb_csv_import():
    # Create mock DynamoDB table
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    dynamodb.create_table(
        TableName="my_table",
        KeySchema=[
            {
                "AttributeName": "StringPK",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "NumberSK",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "StringPK",
                "AttributeType": "S"
            },
            {
                "AttributeName": "NumberSK",
                "AttributeType": "N"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
    table = dynamodb.Table('my_table')

    csv_file = "sample.csv"

    result = csv_import(table, csv_file)
    print(result)

    assert result == "{name} csv imported {count} items".format(
        name=table.name, count=300)
