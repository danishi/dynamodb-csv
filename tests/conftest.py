import boto3
from moto import mock_dynamodb
import json
from decimal import Decimal
import pytest
from typing import Any

size = 1000


@pytest.fixture
def table() -> Any:
    """Create DynamoDB table mock

    Yields:
        Table: boto3 DynamoDB table mock object
    """

    print("Create mock DynamoDB table")
    with mock_dynamodb():
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
        for i in range(size):
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

        yield table
