from app.dynamodb import csv_export
import boto3
from moto import mock_dynamodb2
import json
from decimal import Decimal


@mock_dynamodb2
def test_dynamodb_csv_export():
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

    # Test data put
    for i in range(100):
        table.put_item(Item={
            "StringPK": "foo",
            "NumberSK": i,
            "DecimalValue": Decimal(str(1.23)),
            "BooleanValue": True,
            "NullValue": None,
            "JsonValue": json.loads(
                '[{"string" : "value"},{"number" : 100}]', parse_float=Decimal),
            "StringListValues": ["foo", "bar", "baz"],
            "DecimalListValues": [10, Decimal(str(10.5)), 20],
        })

    output_file = "sample_exp.csv"

    result = csv_export(table, output_file)
    print(result)

    assert result == "{name} csv exported {count} items".format(
        name=table.name, count=100)
