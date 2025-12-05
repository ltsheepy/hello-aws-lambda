def lambda_handler(event, context):
    """
    Simple Lambda function that returns a greeting
    """
    return {
        'statusCode': 200,
        'body': 'Hello from AWS Lambda! 🚀',
        'headers': {
            'Content-Type': 'text/plain'
        }
    }
