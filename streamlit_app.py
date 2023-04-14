import streamlit as st
import boto3 as boto
from botocore.exceptions import ClientError

def create_glue_client(region_id):
    glue_client = boto.client(
        'glue',
        region_name = region_id
    )

    return glue_client

def create_s3_client():
    client = boto.client(
        's3'
    )

    return client

def get_database(glue_client, catalog_id, database_name):

    # Note: This does not properly paginate past 100.
    try:
        return glue_client.get_database(
            CatalogId=catalog_id,
            Name=database_name
        )
    
    except ClientError as e:
        st.write(e)
        return {}

def get_table(glue_client, catalog_id, database_name, table_name):

    # Note: This does not properly paginate past 100.
    try:
        return glue_client.get_table(
            CatalogId=catalog_id,
            DatabaseName=database_name,
            Name=table_name
        )
    
    except ClientError as e:
        st.write(e)
        return {}

def get_content_from_s3(s3_client, bucket, key):
    
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
k_EXAMPLE_DB_NAME = "output-s3-database"
k_EXAMPLE_TABLE_NAME = "output-table-demo"
k_EXAMPLE_S3_BUCKET = "test-catalog-bucket-ejjohnso"
k_EXAMPLE_KEY = "run-1681502746485-part-r-00000"

# Streamlit App
st.title("Stand-In App")

glue_client = create_glue_client(k_REGION)
example_table = get_table(glue_client, k_ACCOUNT_ID, k_EXAMPLE_DB_NAME, k_EXAMPLE_TABLE_NAME)

storage = example_table['Table']['StorageDescriptor']

st.write(storage)
s3_bucket_location = storage['Location']
# s3_bucket_location = k_EXAMPLE_S3_BUCKET

s3_client = create_s3_client()
content = get_content_from_s3(s3_client, s3_bucket_location, k_EXAMPLE_KEY)

for line in content.strip().split("\n"):
    event, category, date, venue = line.split(",")
    st.write(f"There is a {category} event {event} on {date} at {venue}")


st.write(example_table['Table'])
