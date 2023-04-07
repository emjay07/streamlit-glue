import streamlit as st
import boto3 as boto
from botocore.exceptions import ClientError

def create_glue_client(region_id):
    # Create quicksight client
    glue_client = boto.client(
        'glue',
        region_name = region_id
    )

    return glue_client

def get_database(glue_client, database_name):

    # Note: This does not properly paginate past 100.
    try:
        return glue_client.get_database(Name=database_name)
    
    except ClientError as e:
        st.write(e)
        return {}


# constants
k_REGION = "us-west-2"
k_ACCOUNT_ID = "110561467685"
k_EXAMPLE_DB_NAME = "test-catalog-db"

# Streamlit App
st.title("Stand-In App")

glue_client = create_glue_client(k_REGION)
example_db = get_database(glue_client, k_EXAMPLE_DB_NAME)

if example_db.has_key("Database"):
    st.write(example_db["Database"]["LocationURI"])
else:
    st.write("there was an error fetching the databse")
