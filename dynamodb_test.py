import boto3

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")

table = dynamodb.Table("StudyAssistantHistory")

print("Connected to DynamoDB!")
print("Table name:", table.name)