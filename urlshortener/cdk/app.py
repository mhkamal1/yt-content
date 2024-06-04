#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.cdk_stack import UrlShortenerServiceStack


app = cdk.App()
UrlShortenerServiceStack(app, "CdkStack")

app.synth()
