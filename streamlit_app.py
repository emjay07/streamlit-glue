import streamlit as st
import boto3 as boto
import pandas as pd
from io import StringIO
from botocore.exceptions import ClientError

def create_s3_client():
    client = boto.client(
        's3'
    )

    return client

def get_object_keys_from_s3(s3_client, bucket):
    
    try:
        s3_objects = s3_client.list_objects_v2(
            Bucket=bucket
        )['Contents']
    except ClientError as e:
        st.write(e)
        raise

    keys = []
    for obj in s3_objects:
        keys.append(obj['Key'])
    
    return keys

def get_object_content_from_s3(s3_client, bucket, key):
    
    try:
        s3_object = s3_client.get_object(
            Bucket=bucket,
            Key=key
        )['Body']
    except ClientError as e:
        st.write(e)
        raise
    
    return s3_object.read().decode('utf-8')


# constants
k_REGION = "us-west-2"
k_ACCOUNT_ID = "382152459716"
k_S3_BUCKET = "glue-output-csv-demo"
k_EXAMPLE_KEY = "run-1681502746485-part-r-00000"

# Streamlit App
st.title("Stand-In App")

s3_client = create_s3_client()
object_keys = get_object_keys_from_s3(s3_client, k_S3_BUCKET)
df_list = []
for key in object_keys:
    temp = get_object_content_from_s3(s3_client, k_S3_BUCKET, key)
    df = pd.read_csv(StringIO(temp))
    df.tail(-1) # get rid of the header of each file
    df_list.append(df)

final_df = pd.concat(df_list)
st.dataframe(final_df)

# for line in content.strip().split("\n"):
#     event, category, date, venue = line.split(",")
#     st.write(f"There is a {category} event {event} on {date} at {venue}")

