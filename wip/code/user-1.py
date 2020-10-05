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
           endpoint_url='http://ceph-rgw.odh-1.svc.cluster.local',
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