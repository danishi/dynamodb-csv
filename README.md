# DynamoDB import CSV utilities

[![ci](https://github.com/danishi/DynamoDBCSV/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/danishi/DynamoDBImportCSV/actions/workflows/ci.yaml)
![MIT](https://img.shields.io/github/license/danishi/DynamoDBCSV)
![Python](https://img.shields.io/badge/Python-3-1384C5.svg)
[![PyPI](https://badge.fury.io/py/dynamodb-csv.svg)](https://badge.fury.io/py/dynamodb-csv)
[![Downloads](https://pepy.tech/badge/dynamodb-csv)](https://pepy.tech/project/dynamodb-csv)
[![Downloads](https://pepy.tech/badge/dynamodb-csv/month)](https://pepy.tech/project/dynamodb-csv)
[![Downloads](https://pepy.tech/badge/dynamodb-csv/week)](https://pepy.tech/project/dynamodb-csv)

Python command to import CSV into DynamoDB

## Introduction

I wrote this script because there was no tool to satisfy my modest desire to make it easy to import CSV files into DynamoDB.  
Written in a simple Python script, it should be easy to parse and modify.  
  
it works for me.

## Getting started

### Install

```
$ python -m venv venv
$ . venv/bin/activate
$ pip install dynamodb-csv
$ dynamodb-csv -h
usage: dynamodb-csv [-h] [-i] [--truncate] -t TABLE [-f FILE]

Import CSV file into DynamoDB table utilities

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version
  -i, --imp             mode import
  --truncate            mode truncate
  -t TABLE, --table TABLE
                        DynamoDB table name
  -f FILE, --file FILE  UTF-8 CSV file path required import mode
```

### Install for developer 

```
$ python -m venv venv
$ . venv/bin/activate
$ python setup.py install
$ dynamodb-csv -h
```

or

```
$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements-dev.txt
$ python app/main.py -h
```

### Create your config.ini file

```
[AWS]
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
REGION=your_dynamodb_table_region
```

### Create your CSV and CSV spec file.ini

Prepare a UTF-8 CSV file of the format you want to import into your DynamoDB table and a file that defines that format.  

#### For example

Please refer to this writing method.

[sample.csv](sample.csv)
```
StringPK,NumberSK,DecimalValue,BooleanValue,NullValue,JsonValue,StringListValues,DecimalListValues
foo,1,1.23,TRUE,,"[{""string"" : ""value""},{""number"" : 100}]",foo bar baz,10 10.1 20
foo,2,0.001,,,"[{""boolean"" : true}]",リンゴ バナナ スイカ,10 10.1 20
foo,3,1,,,"[{""boolean"" : false}]",,
```

[sample.csv.spec](sample.csv.spec)
```
# sample.csv data format specification

# String : S
# Integer : I
# Decimal : D
# Boolean : B
# Json : J
# StringList : SL
# DecimalList : DL

[CSV_SPEC]
StringPK=S
NumberSK=I
DecimalValue=D
BooleanValue=B
NullValue=S
JsonValue=J
StringListValues=SL
DecimalListValues=DL
```

### Create DynamoDB table

You need to have created a DynamoDB table that meets your specifications.

```
$ aws dynamodb describe-table --table-name my_table
{
    "Table": {
        "AttributeDefinitions": [
            {
                "AttributeName": "NumberSK",
                "AttributeType": "N"
            },
            {
                "AttributeName": "StringPK",
                "AttributeType": "S"
            }
        ],
        "TableName": "my_table",
        "KeySchema": [
            {
                "AttributeName": "StringPK",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "NumberSK",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": "2022-02-23T15:31:55.141000+09:00",
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": "2022-02-23T16:37:29.382000+09:00",
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:ap-northeast-1:XXXXXXXXXX:table/my_table",
        "TableId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }
}
```

### CSV import

This command requires a CSV spec file in the same directory.  

```
$ dynamodb-csv -i -t my_table -f sample.csv
please wait my_table importing sample.csv
300it [00:00, 19983.03it/s]
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:07<00:00, 40.97it/s]
my_table csv imported 300 items
```

### Table truncate

Also, since you may want to erase unnecessary data during the import experiment, we have prepared a command to discard it.

```
$ dynamodb-csv --truncate -t my_table
my_table scan 300 items
please wait my_table truncating
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:07<00:00, 40.95it/s]
my_table truncated
```

## License

See [LICENSE](LICENSE)
