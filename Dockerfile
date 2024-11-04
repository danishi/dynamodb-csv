# Package the 'dynamodb-csv' as a docker image.
#
# To build:
# $ cd <project directory>
# $ docker build -t dynamodb-csv -f Dockerfile .
#
# To run:
# To display the command line options:
# $ docker run --rm -it dynamodb-csv --help
# .. will display the command line help
#
# for Windows
# > docker run --rm -v %cd%/:/local dynamodb-csv -i -t my_table -f sample.csv
# for Linux
# $ docker run --rm -v ${PWD}/:/local dynamodb-csv -i -t my_table -f sample.csv
FROM python:3.13-slim

RUN pip install --no-cache-dir dynamodb-csv

WORKDIR /local

ENTRYPOINT ["dynamodb-csv"]
CMD []
