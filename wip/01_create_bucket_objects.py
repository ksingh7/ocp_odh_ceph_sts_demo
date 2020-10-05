import boto3
import urllib3

more_binary_data = b'Here we have some more data'

def main():
    urllib3.disable_warnings()
    s3 = boto3.client('s3',
                      endpoint_url='http://ceph-rgw',
                      aws_access_key_id='odh1user1',
                      aws_secret_access_key='odh1user1pass', 
                      use_ssl=False,
                      verify=False
                      )
    s3.create_bucket(Bucket="bucket-1")
    response = s3.list_buckets()
    for item in response['Buckets']:
        print(item['CreationDate'], item['Name'])
        s3.put_object(Body=more_binary_data, Bucket=item['Name'], Key='file1.txt')
    response = s3.list_buckets()

    for key in s3.list_objects(Bucket='bucket-1')['Contents']:
        print(key['Key'])

if __name__ == '__main__':
    main()