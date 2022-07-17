---
layout: default
title: dynamodb-csv 使い方ガイド
---
![DynamoDBCSV](https://user-images.githubusercontent.com/56535085/159007555-e72d1c26-eb44-46ca-bc38-c752164995bf.png)

# はじめに

これはDynamoDBのテーブルデータをCSVでより簡単にインポート/エクスポートするためのコマンドラインユーティリティです。

# インストール

Pythonが実行できる環境が必要です。

```shell
$ pip install dynamodb-csv
$ dynamodb-csv -h
usage: dynamodb-csv [-h] [-v] [-i] [-e] [--truncate] -t TABLE [-idx INDEX] [-f FILE] [-o OUTPUT] [--ignore]

Import CSV file into DynamoDB table utilities

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version
  -i, --imp             mode import
  -e, --exp             mode export
  --truncate            mode truncate
  -t TABLE, --table TABLE
                        DynamoDB table name
  -idx INDEX, --index INDEX
                        DynamoDB index name
  -f FILE, --file FILE  UTF-8 CSV file path required import mode
  -o OUTPUT, --output OUTPUT
                        output file path required export mode
  --ignore              ignore import error
```

# 接続設定ファイル
`config.ini.example`をコピーして`config.ini`を作成し、接続先情報を記述します。

```ini
[AWS]
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
REGION=your_dynamodb_table_region
# Option
#ENDPOINT_URL=http://dynamodb-local:8000
```

`ENDPOINT_URL`を指定してDynamoDB-localを利用することも可能です。

# CSV定義ファイル

インポート/エクスポート操作を行うためにDynamoDBテーブルの属性情報と合わせたCSV定義ファイルを作成する必要があります。
インポートを行う場合は合わせてUTF-8で取り込むCSVファイルを作成します。
## 例
* CSVファイル
  * [sample.csv](https://github.com/danishi/dynamodb-csv/blob/master/sample.csv)
* CSV定義ファイル
  * [sample.csv.spec](https://github.com/danishi/dynamodb-csv/blob/master/sample.csv.spec) : インポートの定義
  * [sample_exp.csv.spec](https://github.com/danishi/dynamodb-csv/blob/master/sample_exp.csv.spec) : エクスポートの定義
  * [sample_gsi_exp.csv.spec](https://github.com/danishi/dynamodb-csv/blob/master/sample_gsi_exp.csv.spec) : GSIを使ったエクスポートの定義
  * [sample_query_exp.csv.spec](https://github.com/danishi/dynamodb-csv/blob/master/sample_query_exp.csv.spec) : パーティションキーを使ったクエリー指定のエクスポートの定義
  * [sample_query_exp2.csv.spec](https://github.com/danishi/dynamodb-csv/blob/master/sample_query_exp2.csv.spec) : ソートキーを使ったクエリー指定のエクスポートの定義

# コマンド実行例

## テスト用テーブルの作成
```shell
$ aws dynamodb create-table --cli-input-json file://my_table.json --region ap-northeast-1
```

## インポート
```shell
$ dynamodb-csv -i -t my_table -f sample.csv
```

ignoreオプションを付けると、CSV行をインポートする際にエラーがあった場合も処理中断せず、その行を無視して進めます。  

```shell
$ dynamodb-csv -i -t my_table -f sample.csv --ignore
```

ignoreオプションを付けた場合インポート速度が遅くなります。

## エクスポート
```shell
$ dynamodb-csv -e -t my_table -o sample_exp.csv
```

## GSIを使ったエクスポート
```shell
$ dynamodb-csv -e -t my_table -idx NumberSK-index -o sample_gsi_exp.csv
```

## パーティションキーを使ったクエリー指定のエクスポートの定義
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

### クエリー条件
クエリー条件として以下が指定できます。

* `PKAttribute` : パーティションキー属性名
* `PKAttributeValue` : パーティションキー属性値
* `PKAttributeType` : パーティションキー属性のデータ型
* `SKAttribute` : ソートキー属性名
* `SKAttributeValues` : ソートキー属性値（複数可）
  * 例: `foo` or `foo,bar`
* `SKAttributeType` : ソートキー属性のデータ型
* `SKAttributeExpression` : ソートキーへのクエリー条件 [指定の例](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#dynamodb-conditions)
* `begins_with` `between` `eq` `gt` `gte` `lt` `lte`

## ソートキーを使ったクエリー指定のエクスポートの定義

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

## テーブルのクリア
テーブルの項目を全て削除することもできます。

```shell
$ dynamodb-csv --truncate -t my_table
```
