import boto3


def create_table():
    dynamodb = boto3.resource("dynamodb",
        region_name="ap-northeast-1",
        aws_access_key_id="XXXXXXXXXXXXXXXXXX",
        aws_secret_access_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        endpoint_url="http://dynamodb-local:8000")

    table = dynamodb.create_table(
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
            },

        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
    return table


if __name__ == "__main__":
    my_table = create_table()
    print("Table status:", my_table.table_status)
