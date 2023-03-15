import boto3, json


dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('ciclistas')
records = []

try:
    with open('view_ciclista.json') as f:
        raw_records = json.load(f)
        records = raw_records['RECORDS']
except Exception as e:
    print(f'Issue reading from json file: {e}')


for record in records:
    table.put_item(Item=record)
    print(f'Record.ID: {record.get("ID")}, inserted!')

