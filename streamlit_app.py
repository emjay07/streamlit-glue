import streamlit as st
import boto3 as boto
from botocore.exceptions import ClientError

# constants
k_REGION = "us-west-2"
k_ACCOUNT_ID = "110561467685"


st.title("Stand-In App")

