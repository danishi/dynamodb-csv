from app.dynamodb import truncate
import boto3
from moto import mock_dynamodb2


@mock_dynamodb2
def test_dynamodb_truncate():
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
        })

    result = truncate(table)
    print(result)

    assert result == "{name} truncated".format(name=table.name)
