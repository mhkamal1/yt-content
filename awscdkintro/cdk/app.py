#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack


app = cdk.App()
CdkStack(app, "myFirstCdkProject")

app.synth()
