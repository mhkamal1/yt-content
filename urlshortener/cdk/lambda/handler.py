import boto3
import json
import hashlib

print('Loading function')

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('urlMapping2') ## hardcoded, in reality should be fetched from env vars
tableName = 'urlMapping2'


def handler(event, context):

    if event['body']: ## assume it's a POST request
        r_body = json.loads(event['body'])

        if r_body["longUrl"]: 

            # the long_url is the URL that the user wants to shorten
            # we use md5 hashing to generate a unique hash for the URL
            # we save the hash and the URL in the database
            long_url = r_body["longUrl"]
            short_url = hashlib.md5(long_url.encode()).hexdigest()

            # take first 7 characters of hash as short_url
            # if it already exists in db, increment by 1 character until unique
            for i in range(7, len(short_url)):
                res=table.get_item(Key={'s_url': short_url[:i]})
                try:
                    res['Item']
                except KeyError: ## store in db
                    short_url = short_url[:i]
                    break

            # store in db the short_url and long_url as key-value pair  
            table.put_item(
                Item={
                    's_url': short_url,
                    'l_url': long_url
                }
            )

            return {
                'statusCode': 200,
                'body': json.dumps({"shortenedUrl": short_url})
                }
        
    else: ## assume it's a GET request
        s_url = event["pathParameters"]["short_url"]

        l_url = table.get_item(
            Key={
                's_url': s_url
            })
        
        # redirect to the long_url
        return {
                'statusCode': 302,
                'headers': {
                    'Location': l_url["Item"]["l_url"]
                }
            }    
    