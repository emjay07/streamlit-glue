import streamlit as st
import boto3 as boto
import pandas as pd
import plotly.express as px
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
k_S3_BUCKET = "glue-output-csv-demo"
k_EXAMPLE_KEY = "run-1681502746485-part-r-00000" # test

# Streamlit App Config
st.set_page_config(layout="wide")

# Pandas Config
pd.options.plotting.backend = "plotly"

# App Code
st.title("What Can Streamlit Do?")

s3_client = create_s3_client()
object_keys = get_object_keys_from_s3(s3_client, k_S3_BUCKET)
df_list = []
for key in object_keys:
    temp = get_object_content_from_s3(s3_client, k_S3_BUCKET, key)
    df = pd.read_csv(StringIO(temp))
    df.tail(-1) # get rid of the header of each file
    df_list.append(df)

final_df = pd.concat(df_list)

col1, col2 = st.columns([1, 2])
tab1, tab2, tab3 = st.tabs(["Categories", "Venues", "Chart 3"])



with col1:
    st.dataframe(final_df)

with col2:
    with tab1:
        counts = final_df["catgroup"].value_counts()
        cat_df = pd.DataFrame({'index':counts.index, 'count':counts.values})
        fig = px.pie(cat_df, values='count', names='index')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        counts = final_df["venuename"].value_counts()
        ven_df = pd.DataFrame({'index':counts.index, 'count':counts.values})
        fig = px.pie(ven_df, values='count', names='index')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.write("Under Construction :construction:")
