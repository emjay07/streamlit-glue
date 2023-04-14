import streamlit as st
import boto3 as boto
from botocore.exceptions import ClientError
import s3fs

def create_glue_client(region_id):
    # Create quicksight client
    glue_client = boto.client(
        'glue',
        region_name = region_id
    )

    return glue_client

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

def get_content_from_s3(s3_path):
    fs = s3fs.S3FileSystem(anon=False)

    def read_file(filename):
        with fs.open(filename) as f:
            return f.read().decode("utf-8")
    
    content = read_file(s3_path)
    
    return content


# constants
k_REGION = "us-west-2"
k_ACCOUNT_ID = "382152459716"
k_EXAMPLE_DB_NAME = "output-s3-database"
k_EXAMPLE_TABLE_NAME = "output-table-demo"
k_EXAMPLE_S3_PATH = "s3://test-catalog-bucket-ejjohnso/run-1681502746485-part-r-00000"

# Streamlit App
st.title("Stand-In App")

content = get_content_from_s3(k_EXAMPLE_S3_PATH)

for line in content.strip().split("\n"):
    event, category, date, venue = line.split(",")
    st.write(f"There is a {category} event {event} on {date} at {venue}")

glue_client = create_glue_client(k_REGION)
example_db = get_database(glue_client, k_ACCOUNT_ID, k_EXAMPLE_DB_NAME)
example_table = get_table(glue_client, k_ACCOUNT_ID, k_EXAMPLE_DB_NAME, k_EXAMPLE_TABLE_NAME)

if "Database" in example_db:
    st.write(example_db)
    st.write(example_table)
else:
    st.write("there was an error fetching the databse")
