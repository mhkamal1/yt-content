AWS Lambda and API Gateway demonstration by building a serverless URL shortener service.

## To run locally
This is just for checking the functionality and the like, does not use any AWS services. I installed a local dynamodb instance for this (https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html). Once installed use the command: `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb` to run. 

The app itself is a FastAPI based app using pymondo to provide a pythonic interface for dynamodb.  

To run the app first make sure dynamodb is running locally on a separate terminal then run the main python file using: `python main.py` from inside the app directory. This should spin up the backend server. It should also host the static (html) file on the server meaning you can access it using `localhost:8080`.

## To deploy as a cdk stack
`cd` into the `cdk` directory and run `cdk deploy`