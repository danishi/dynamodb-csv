# DynamoDB CSV utility

[![ci](https://github.com/danishi/DynamoDBCSV/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/danishi/DynamoDBImportCSV/actions/workflows/ci.yaml)
![MIT](https://img.shields.io/github/license/danishi/DynamoDBCSV)
![Python](https://img.shields.io/badge/Python-3.6-1384C5.svg)
[![PyPI](https://badge.fury.io/py/dynamodb-csv.svg)](https://badge.fury.io/py/dynamodb-csv)
[![Downloads](https://pepy.tech/badge/dynamodb-csv)](https://pepy.tech/project/dynamodb-csv)
[![Downloads week](https://pepy.tech/badge/dynamodb-csv/week)](https://pepy.tech/project/dynamodb-csv)
[![Downloads month](https://pepy.tech/badge/dynamodb-csv/month)](https://pepy.tech/project/dynamodb-csv)

A utility that allows CSV import / export to DynamoDB on the command line

## Introduction

I wrote this script because there was no tool to satisfy my modest desire to make it easy to import CSV files into DynamoDB.  
Written in a simple Python script, it should be easy to parse and modify.  
  
it works for me.

## Getting started

### Install

```shell
$ python -m venv venv
$ . venv/bin/activate
$ pip install dynamodb-csv
$ dynamodb-csv -h
usage: dynamodb-csv [-h] [-v] [-i] [-e] [--truncate] -t TABLE [-f FILE] [-o OUTPUT]

Import CSV file into DynamoDB table utilities

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version
  -i, --imp             mode import
  -e, --exp             mode export
  --truncate            mode truncate
  -t TABLE, --table TABLE
                        DynamoDB table name
  -f FILE, --file FILE  UTF-8 CSV file path required import mode
  -o OUTPUT, --output OUTPUT
                        output file path required export mode
```

### Install for developer 

```shell
$ python -m venv venv
$ . venv/bin/activate
$ python setup.py install
$ dynamodb-csv -h
```

or

```shell
$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements-dev.txt
$ python app/main.py -h
```

Or you can use devcontainer.

### Create your config.ini file on current directory

```ini
[AWS]
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
REGION=your_dynamodb_table_region
# Option
#ENDPOINT_URL=http://dynamodb-local:8000
```

### Create your CSV and CSV spec file

Prepare a UTF-8 CSV file of the format you want to import into your DynamoDB table and a file that defines that format.  

#### For example

Please refer to this writing method.

[sample.csv](sample.csv)
```csv
StringPK,NumberSK,DecimalValue,BooleanValue,NullValue,JsonValue,StringListValues,DecimalListValues
foo,1,1.23,TRUE,,"[{""string"" : ""value""},{""number"" : 100}]",foo bar baz,10 10.1 20
foo,2,0.001,,,"[{""boolean"" : true}]",リンゴ バナナ スイカ,10 10.1 20
foo,3,1,,,"[{""boolean"" : false}]",,
```

[sample.csv.spec](sample.csv.spec)
```ini
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

```shell
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

### CSV import into Table

This command requires a CSV spec file in the same directory.  

```shell
$ dynamodb-csv -i -t my_table -f sample.csv
please wait my_table importing sample.csv
300it [00:00, 19983.03it/s]
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:07<00:00, 40.97it/s]
my_table csv imported 300 items
```

### Export table to CSV

You will also need to expand the same data to multiple tables.  
Therefore, data can be exported.  
As with import, you need a CSV spec file.

```shell
$ dynamodb-csv -e -t my_table -o sample_exp.csv 
please wait my_table exporting sample_exp.csv
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:00<00:00, 16666.77it/s]
my_table csv exported 300 items
```

### Table truncate

Also, since you may want to erase unnecessary data during the import experiment, we have prepared a command to discard it.

```shell
$ dynamodb-csv --truncate -t my_table
my_table scan 300 items
please wait my_table truncating
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:07<00:00, 40.95it/s]
my_table truncated
```

## License

See [LICENSE](LICENSE)
