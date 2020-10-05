import boto3
import json
import logging
from botocore.exceptions import ClientError
logging.basicConfig(filename="boto.log", level=logging.DEBUG)

from botocore.handlers import validate_bucket_name


## (S3 resource) --> Policy --> Role --> User

## odh2user1 will assume a role, which is created by odh1user1 to access s3 resources owned by odh1user1
## according to the permission policy attached to the role

odh1_user1_iam = boto3.client('iam',
           aws_access_key_id='odh1user1',
           aws_secret_access_key='odh1user1pass',
           endpoint_url='http://ceph-rgw',
           region_name='')


policy_document = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"AWS\":[\"arn:aws:iam::odh2:user/odh2user1\"]},\"Action\":[\"sts:AssumeRole\"]}]}"



role_response = ""
print("\n Getting Role \n")
#  Getting Role

try:
    role_response = odh1_user1_iam.get_role(
        RoleName='S3Access'
    )
    #print(role_response)

## on first run it was blank
    
except ClientError as e:
    print("\n Creating Role \n")
#  Creating Role 
    role_response = odh1_user1_iam.create_role(
       AssumeRolePolicyDocument=policy_document,
       Path='/',
       RoleName='S3Access',
    )
    print(role_response)


role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":{\"Effect\":\"Allow\",\"Action\":\"s3:*\",\"Resource\":\"arn:aws:s3:::*\"}}"

response = odh1_user1_iam.put_role_policy(
                RoleName='S3Access',
                PolicyName='Policy1',
                PolicyDocument=role_policy
                )

print("IAM Role and Policy is now available. Other user can now access dataset")
## User 2 has to add the ARN value of the role created by user-1

Role_Arn = 'arn:aws:iam::odh1:role/S3Access'


odh2_user1_sts = boto3.client('sts',
           aws_access_key_id='odh2user1',
           aws_secret_access_key='odh2user1pass',
           endpoint_url='http://ceph-rgw',
           region_name='')


response = odh2_user1_sts.assume_role(
            RoleArn=Role_Arn,
            RoleSessionName='session_odh2user1',
            DurationSeconds=3600
            )

s3client = boto3.client('s3',
            aws_access_key_id = response['Credentials']['AccessKeyId'],
            aws_secret_access_key = response['Credentials']['SecretAccessKey'],
            aws_session_token = response['Credentials']['SessionToken'],
            endpoint_url='http://ceph-rgw',
            region_name='',)

#bucket_name = 'bucket-1'
#s3bucket = s3client.create_bucket(Bucket=bucket_name)
#print(s3client.list_buckets())

print("Getting files from odh1user1 dataset bucket-1, without sharing credentials \n")
for key in s3client.list_objects(Bucket='bucket-1')['Contents']:
    print(key['Key'])
    
print("\n Creating a new bucket from odh2user1 account")
try:
    s3bucket = s3client.create_bucket(Bucket='odh2user1-bucket')
except ClientError as e:
    print("\n Bucket already exists \n")

# Retrieve the list of existing buckets
response = s3client.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')