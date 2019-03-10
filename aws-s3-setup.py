
import boto3
import json

# Specify the region to create the AWS resources in
DEFAULT_REGION = 'eu-west-1'

# Create S3 resource
s3 = boto3.resource('s3')

# Set a bucket name which will be our domain name.
# bucket_name = "demo123456.com"
bucket_name = "life-stats-logger"

# Create a new S3 bucket, using a demo bucket name
s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={
    'LocationConstraint': DEFAULT_REGION
})

# We need to set an S3 policy for our bucket to
# allow anyone read access to our bucket and files.
# If we do not set this policy, people will not be
# able to view our S3 static web site.
bucket_policy = s3.BucketPolicy(bucket_name)
policy_payload = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "Allow Public Access to All Objects",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::%s/*" % (bucket_name)
    }
    ]
}

# Add the policy to the bucket
response = bucket_policy.put(Policy=json.dumps(policy_payload))

# Next we'll set a basic configuration for the static
# website.
website_payload = {
    'ErrorDocument': {
        'Key': 'error.html'
    },
    'IndexDocument': {
        'Suffix': 'index.html'
    }
}

# Make our new S3 bucket a static website
bucket_website = s3.BucketWebsite(bucket_name)

# And configure the static website with our desired index.html
# and error.html configuration.
bucket_website.put(WebsiteConfiguration=website_payload)