from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment
)


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        myBucket = s3.Bucket(
            self,
            id="Bucket",
            public_read_access=True,
            website_index_document="index.html"
        )

        s3_deployment.BucketDeployment(
            self,
            id="bucketDeployment",
            sources=[s3_deployment.Source.asset("../frontend/build")],
            destination_bucket=myBucket
        )
