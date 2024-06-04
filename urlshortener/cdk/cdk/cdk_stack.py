from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    RemovalPolicy,
    aws_s3_deployment as s3_deployment,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_logs as logs
)

class UrlShortenerServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket for storing the static website file
        # there are probaby ways to make this more secure
        bucket = s3.Bucket(self, 
            "MyBucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,  # NOT recommended for production code
            auto_delete_objects=True,               # NOT recommended for production code
            website_index_document="index.html", # static site
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(block_public_acls=False, block_public_policy=False, ignore_public_acls=False, restrict_public_buckets=False)
        )

        # Upload static files to s3 bucket
        s3_deployment.BucketDeployment(self, 
            "DeployStaticWebsite",
            sources=[s3_deployment.Source.asset("static")],
            destination_bucket=bucket
        )

        # Create a Lambda function for shortening URLs and redirecting to the original URL
        my_function = _lambda.Function(self, 
            "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lambda")
        )

        # Create an API Gateway
        apigw = apigateway.RestApi(self, "MyApi", deploy=True)

        # Since the bucket is publicly accessible, we can use HTTP integration to serve the static website
        apigw.root.add_method(
            "GET",
            apigateway.HttpIntegration(
                url="http://"+bucket.bucket_name + ".s3.eu-central-1.amazonaws.com/index.html",
                http_method="GET"
            )
        )

        # Add endpoints for shortening URLs and redirecting to the original URL, passing lambda as argument
        apigw.root.add_resource("create").add_method("POST", apigateway.LambdaIntegration(my_function))
        apigw.root.add_resource("{short_url}").add_method("GET", apigateway.LambdaIntegration(my_function))

        # Create a DynamoDB table for storing the URL mappings using short URL as the primary key
        dtable = dynamodb.TableV2(self, "urlMapping2",
            table_name="urlMapping2",
            partition_key=dynamodb.Attribute(name="s_url", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
            # billing=dynamodb.Billing.provisioned(read_capacity=dynamodb.Capacity.fixed(1), write_capacity=dynamodb.Capacity.autoscaled(max_capacity=2))
        )

        ## allow lambda to read and write to dynamodb
        dtable.grant_read_write_data(my_function) 