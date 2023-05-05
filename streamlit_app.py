import streamlit as st
import boto3 as boto
import pandas as pd
import plotly.express as px
from datetime import datetime as dt
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

def df_filter(message, df):
        
    date_format = '%Y-%m-%d'
    min_date = dt.strptime(final_df['caldate'].min(), date_format)
    max_date = dt.strptime(final_df['caldate'].max(), date_format)

    slider_min, slider_max = st.slider('%s' % (message),min_date,max_date,[min_date,max_date])

    # while len(str(df.iloc[slider_1][1]).replace('.0','')) < 4:
    #     df.iloc[slider_1,1] = '0' + str(df.iloc[slider_1][1]).replace('.0','')
        
    # while len(str(df.iloc[slider_2][1]).replace('.0','')) < 4:
    #     df.iloc[slider_2,1] = '0' + str(df.iloc[slider_1][1]).replace('.0','')

    # start_date = dt.strptime(str(df.iloc[slider_1][0]).replace('.0','') + str(df.iloc[slider_1][1]).replace('.0',''),'%Y%m%d%H%M%S')
    # start_date = start_date.strftime('%d %b %Y, %I:%M%p')
    
    # end_date = dt.strptime(str(df.iloc[slider_2][0]).replace('.0','') + str(df.iloc[slider_2][1]).replace('.0',''),'%Y%m%d%H%M%S')
    # end_date = end_date.strftime('%d %b %Y, %I:%M%p')

    # st.info('Start: **%s** End: **%s**' % (start_date,end_date))
    
    filtered_df = df[(df['caldate'] >= slider_min) & (df['caldate'] <= slider_max)]
    # filtered_df = df

    return filtered_df

# constants
k_REGION = 'us-west-2'
k_S3_BUCKET = 'glue-output-csv-demo'
k_EXAMPLE_KEY = 'run-1681502746485-part-r-00000' # test

# Streamlit App Config
# st.set_page_config(layout='wide')

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

# filter data
filtered_df = df_filter('Move sliders to filter date', final_df)

col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(filtered_df)

with col2:
    tab1, tab2, tab3 = st.tabs(["Categories", "Venues", "Chart 3"])
    with tab1:
        counts = filtered_df['catgroup'].value_counts()
        cat_df = pd.DataFrame({'index':counts.index, 'count':counts.values})
        fig = px.pie(cat_df, values='count', names='index')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        counts = filtered_df['venuename'].value_counts()
        ven_df = pd.DataFrame({'index':counts.index, 'count':counts.values})
        fig = px.bar(ven_df, y='count', x='index')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.write("Under Construction :construction:")
