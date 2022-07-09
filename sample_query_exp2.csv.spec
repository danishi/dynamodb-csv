# sample_query_exp2.csv data format specification

# String : S
# Integer : I
# Decimal : D
# Boolean : B (blank false)
# Json : J
# StringList : SL
# DecimalList : DL

[QUERY_OPTION]
PKAttribute=StringPK
PKAttributeValue=bar
PKAttributeType=S
SKAttribute=NumberSK
SKAttributeValues=50,100
SKAttributeType=I
SKAttributeExpression=between

[CSV_SPEC]
StringPK=S
NumberSK=I
DecimalValue=D
BooleanValue=B
NullValue=S
JsonValue=J
StringListValues=SL
DecimalListValues=DL
