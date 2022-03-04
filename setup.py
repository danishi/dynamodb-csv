from setuptools import setup

setup(
    name="DynamoDBImportCSV",
    version="1.1.0",
    packages=["app"],
    install_requires=["boto3", "configparser", "tqdm"],
    entry_points={
        "console_scripts": [
            "dynamodb_import = app.dynamodb_import:main",
            "dynamodb_truncate = app.dynamodb_truncate:main",
        ]
    }
)
