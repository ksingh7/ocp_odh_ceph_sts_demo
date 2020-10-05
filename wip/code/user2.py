import boto3


## User 2 has to add the ARN value of the role created by user-1

Role_Arn = 'arn:aws:iam::odh1:role/S3Access'


odh2_user1_sts = boto3.client('sts',
           aws_access_key_id='odh2user1',
           aws_secret_access_key='odh2user1pass',
           endpoint_url='http://ceph-rgw.odh-1.svc.cluster.local',
           region_name='')


response = odh2_user1_sts.assume_role(
            RoleArn=Role_Arn,
            RoleSessionName='session_odh2user1',
            DurationSeconds=3600
            )


aws_access_key_id = response['Credentials']['AccessKeyId']
aws_secret_access_key = response['Credentials']['SecretAccessKey']
endpoint_url='http://ceph-rgw.odh-1.svc.cluster.local'

s3client = boto3.client('s3',
            aws_access_key_id = response['Credentials']['AccessKeyId'],
            aws_secret_access_key = response['Credentials']['SecretAccessKey'],
            aws_session_token = response['Credentials']['SessionToken'],
            endpoint_url='http://ceph-rgw.odh-1.svc.cluster.local',
            region_name='',)

bucket_name = 'ufo-dataset'
#s3bucket = s3client.create_bucket(Bucket=bucket_name)
#print(s3client.list_buckets())

print("Getting files from odh1user1 dataset "+ bucket_name +" bucket, without sharing credentials \n")
for key in s3client.list_objects(Bucket=bucket_name)['Contents']:
    print(key['Key'])
    
#print("\n Creating a new bucket from odh2user1 account")
#try:
#    s3bucket = s3client.create_bucket(Bucket='odh2user1-bucket')
#except ClientError as e:
#    print("\n Bucket already exists \n")

# Retrieve the list of existing buckets
#response = s3client.list_buckets()

# Output the bucket names
#print('Existing buckets:')
#for bucket in response['Buckets']:
#    print(f'  {bucket["Name"]}')

