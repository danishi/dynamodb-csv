# DynamoDB CSV utility

[![Release Notes](https://img.shields.io/github/release/danishi/dynamodb-csv)](https://github.com/danishi/dynamodb-csv/releases)
[![Contributors](https://img.shields.io/github/contributors/danishi/dynamodb-csv)](https://github.com/danishi/dynamodb-csv/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/danishi/dynamodb-csv)](https://github.com/danishi/dynamodb-csv/last-commit)
[![Open Issues](https://img.shields.io/github/issues-raw/danishi/dynamodb-csv)](https://github.com/danishi/dynamodb-csv/issues)
[![LRepo-size](https://img.shields.io/github/repo-size/danishi/dynamodb-csv)](https://github.com/danishi/dynamodb-csv/repo-size)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/danishi/dynamodb-csv)
[![MIT](https://img.shields.io/github/license/danishi/DynamoDB-CSV)](https://github.com/danishi/dynamodb-csv/blob/master/LICENSE)
[![ci](https://github.com/danishi/DynamoDB-CSV/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/danishi/DynamoDBImportCSV/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/danishi/dynamodb-csv/branch/master/graph/badge.svg?token=KRA27MJN42)](https://codecov.io/gh/danishi/dynamodb-csv)
[![Maintainability](https://api.codeclimate.com/v1/badges/c1d2a51bbd72d6198e0c/maintainability)](https://codeclimate.com/github/danishi/dynamodb-csv/maintainability)
![Supported Python versions](https://img.shields.io/pypi/pyversions/dynamodb-csv.svg?color=%2334D058)
[![PyPI](https://badge.fury.io/py/dynamodb-csv.svg)](https://badge.fury.io/py/dynamodb-csv)
[![Downloads](https://static.pepy.tech/badge/dynamodb-csv)](https://pepy.tech/project/dynamodb-csv)
[![Downloads week](https://static.pepy.tech/badge/dynamodb-csv/week)](https://pepy.tech/project/dynamodb-csv)
[![Downloads month](https://static.pepy.tech/badge/dynamodb-csv/month)](https://pepy.tech/project/dynamodb-csv)
[![Docker Pulls](https://img.shields.io/docker/pulls/danishi/dynamodb-csv)](https://hub.docker.com/r/danishi/dynamodb-csv)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/danishi/dynamodb-csv) [![Open in Codeanywhere](https://img.shields.io/badge/Open%20in-Codeanywhere-blue?style=for-the-badge&logo=codeanywhere)](https://app.codeanywhere.com/#https://github.com/danishi/dynamodb-csv)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/danishi)

![DynamoDBCSV](https://user-images.githubusercontent.com/56535085/159007555-e72d1c26-eb44-46ca-bc38-c752164995bf.png)

A utility that allows CSV import / export to DynamoDB on the command line

Give a ⭐️ if you like this tool!

## Introduction

I made this command because I didn't have any tools to satisfy my modest desire to make it easy to import CSV files into DynamoDB.
Written in a simple Python script, it's easy to parse and modify.

It works for me.

![terminalizer](https://user-images.githubusercontent.com/13270461/237145047-ec815dad-1ff6-4678-baa4-fd182ee35269.gif)

## Getting started 🚀

### Install

```shell
$ pip install dynamodb-csv
$ dynamodb-csv -h
usage: dynamodb-csv [-h] [-v] [-i] [-e] [--truncate] [--move] -t [TABLE ...] [-idx INDEX] [-f FILE] [-o OUTPUT] [--ignore]
               [--profile PROFILE]

Import CSV file into DynamoDB table utilities

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version
  -i, --imp             mode import
  -e, --exp             mode export
  --truncate            mode truncate
  --move                mode move
  -t [TABLE ...], --table [TABLE ...]
                        DynamoDB table name
  -idx INDEX, --index INDEX
                        DynamoDB index name
  -f FILE, --file FILE  UTF-8 CSV file path required import mode
  -o OUTPUT, --output OUTPUT
                        output file path required export mode
  --ignore              ignore import error
  --profile PROFILE     using AWS profile
```

### Install for developer

<details>
  <summary>Setup and install</summary>

```shell
$ python -m venv venv
$ . venv/bin/activate
$ python setup.py install
$ dynamodb-csv -h
```

Or

```shell
$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements-dev.txt
$ export PYTHONPATH=`pwd`
$ python app/main.py -h
```

For Windows

```shell
> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements-dev.txt
> set PYTHONPATH=%cd%
> python app/main.py -h
```

Or you can use devcontainer.

</details>

### [Use Docker image](https://hub.docker.com/r/danishi/dynamodb-csv)

```shell
$ docker run --rm -v ${PWD}/:/local danishi/dynamodb-csv:tagname -i -t my_table -f sample.csv
```

For Windows

```shell
> docker run --rm -v %cd%/:/local danishi/dynamodb-csv:tagname -i -t my_table -f sample.csv
```

Or [GitHub Packages](https://github.com/danishi/dynamodb-csv/pkgs/container/dynamodb-csv)

### Create your config.ini file on current directory

```ini
[AWS]
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
REGION=your_dynamodb_table_region
# Option
#ENDPOINT_URL=http://dynamodb-local:8000
```

Not required if AWS profile is specified as a parameter.

### Create your CSV and CSV spec file

> [!NOTE]
> Prepare a UTF-8 CSV file of the format you want to import into your DynamoDB table and a file that defines that format.

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
# Boolean : B (blank false)
# Json : J
# StringList : SL
# StringSet : SS
# DecimalList : DL
# DecimalSet : DS

[CSV_SPEC]
StringPK=S
NumberSK=I
DecimalValue=D
BooleanValue=B
NullValue=S
JsonValue=J
StringListValues=SL
StringSetValues=SS
DecimalListValues=DL
DecimalSetValues=DS

# [DELIMITER_OPTION]
# DelimiterCharacter=|
```

The CSV_SPEC type is mapped to the [DynamoDB attribute type](https://docs.aws.amazon.com/en_us/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html#HowItWorks.DataTypeDescriptors) in this way.

|     CSV_SPEC     | DynamoDB attribute data type | example value                                   |
| :--------------: | :--------------------------: | :---------------------------------------------- |
|    String : S    |            String            | `foo`                                           |
|   Integer : I    |            Number            | `1`                                             |
|   Decimal : D    |            Number            | `1.23`                                          |
|   Boolean : B    |           Boolean            | `TRUE`                                          |
|     Json : J     |             Map              | `[{""string"" : ""value""},{""number"" : 100}]` |
| StringList : SL  |             List             | `foo bar baz`                                   |
|  StringSet : SS  |          String Set          | `foo bar baz`                                   |
| DecimalList : DL |             List             | `10 10.1 20`                                    |
| DecimalSet : DS  |          Number Set          | `10 10.1 20`                                    |

Sorry, Binary type and Binary Set type is not supported.
Null type, look [here](https://github.com/danishi/dynamodb-csv?tab=readme-ov-file#import-options).

The default delimiter for list and set types is a space.  
If you want to set it, please comment out `DELIMITER_OPTION` and `DelimiterCharacter`.

### Create DynamoDB table

> [!NOTE]
> You need to have created a DynamoDB table that meets your specifications.

```shell
$ aws dynamodb create-table --cli-input-json file://my_table.json --region ap-northeast-1
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
        "CreationDateTime": "2022-06-26T21:19:21.767000+09:00",
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:ap-northeast-1:XXXXXXXXXXX:table/my_table",
        "TableId": "XXXXXXXX-925b-4cb1-8e3a-604158118c3f",
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "NumberSK-index",
                "KeySchema": [
                    {
                        "AttributeName": "NumberSK",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "DecimalValue",
                        "JsonValue"
                    ]
                },
                "IndexStatus": "ACTIVE",
                "ProvisionedThroughput": {
                    "NumberOfDecreasesToday": 0,
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                },
                "IndexSizeBytes": 0,
                "ItemCount": 0,
                "IndexArn": "arn:aws:dynamodb:ap-northeast-1:XXXXXXXXXXX:table/my_table/index/NumberSK-index"
            }
        ]
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

It is processed at high speed by batch write.

#### Ignore option

If there is an error such as a key schema mismatch, you can give the option to ignore the CSV record.

```shell
$ dynamodb-csv -i -t my_table -f sample.csv --ignore
please wait my_table importing sample.csv
300it [00:00, 19983.03it/s]
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:07<00:00, 40.97it/s]
my_table csv imported 299 items and 1 error items
```

No batch write is done when this option is used.

#### Import options

By default, if CSV has an empty value, it will be set to empty.  
There are options to convert this to Null or not to set the attribute itself.

```ini
[IMPORT_OPTION]
ConvertBlankToNullAttrs=NullValue,JsonValue
ConvertBlankToDropAttrs=DecimalValue
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

#### Use index

```shell
$ dynamodb-csv -e -t my_table -idx NumberSK-index -o sample_gsi_exp.csv
```

#### Use Query

```shell
$ dynamodb-csv -e -t my_table -idx NumberSK-index -o sample_query_exp.csv
```

```ini
# sample_query_exp.csv data format specification

# Integer : I
# String : S
# Decimal : D
# Json : J

[QUERY_OPTION]
PKAttribute=NumberSK
PKAttributeValue=1
PKAttributeType=I

[CSV_SPEC]
NumberSK=I
StringPK=S
DecimalValue=D
JsonValue=J
```

##### Query options

|           key           | description                              | example                                                                                                                                                                      |
| :---------------------: | :--------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|      `PKAttribute`      | Partition key attribute name             |                                                                                                                                                                              |
|   `PKAttributeValue`    | Partition key attribute query value      |                                                                                                                                                                              |
|    `PKAttributeType`    | Partition key attribute data type        |                                                                                                                                                                              |
|      `SKAttribute`      | Sort key attribute name                  |                                                                                                                                                                              |
|   `SKAttributeValues`   | Sort key attribute query value or values | ex. `foo` or `foo,bar`                                                                                                                                                       |
|    `SKAttributeType`    | Sort key attribute data type             |                                                                                                                                                                              |
| `SKAttributeExpression` | Sort key attribute query expression      | [ex.](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#dynamodb-conditions) `begins_with` `between` `eq` `gt` `gte` `lt` `lte` |

```shell
$ dynamodb-csv -e -t my_table -o sample_query_exp2.csv
```

```ini
[QUERY_OPTION]
PKAttribute=StringPK
PKAttributeValue=bar
PKAttributeType=S
SKAttribute=NumberSK
SKAttributeValues=50,100
SKAttributeType=I
SKAttributeExpression=between
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

> [!CAUTION]
> This operation is irreversible. Take care.

### Table move

Move all items from table to table.
A table with the same schema must be prepared in advance.  
Table items is not deleted and behaves like a copy.

```shell
$ dynamodb-csv --move -t my_table_from my_table_to
my_table_from scan 300 items
please wait my_table_to moving
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [00:15<00:00, 20.00it/s]
my_table_to moved 300 items
```

## License

See [LICENSE](LICENSE)

## Special Thanks

### Code contributors 🤝

<a href="https://github.com/danishi/dynamodb-csv/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=danishi/dynamodb-csv" />
</a>

## Appendix

### User guide

- [User guide (for japanese)](https://danishi.github.io/dynamodb-csv/)
