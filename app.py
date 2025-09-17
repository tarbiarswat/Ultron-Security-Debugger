# app.py
import streamlit as st
import requests
import json

st.set_page_config(page_title="Security Test Tool", layout="wide")

st.title("Security Scraper Test Tool")

st.markdown("""
⚠️ **Disclaimer:** This tool is only for **internal security testing**.  
Do not use it against systems without authorization.
""")

# Input fields
st.subheader("Authentication")
token = st.text_input("Paste your Bearer Token", type="password")

st.subheader("Request Details")
base_url = st.text_input("Base API URL", "https://example.com/graphql")
method = st.selectbox("HTTP Method", ["GET", "POST"])
headers_raw = st.text_area("Custom Headers (JSON)", '{"Content-Type": "application/json"}')
body_raw = st.text_area("Request Body (for POST/GraphQL)", '{ "query": "{ me { id name } }" }')

# Parse headers
try:
    headers = json.loads(headers_raw)
except:
    headers = {"Content-Type": "application/json"}
    st.warning("Invalid header JSON. Using default.")

# Add Authorization header if token exists
if token:
    headers["Authorization"] = f"Bearer {token}"

# Execute button
if st.button("Send Request"):
    try:
        if method == "GET":
            response = requests.get(base_url, headers=headers)
        else:
            body = json.loads(body_raw) if body_raw.strip() else {}
            response = requests.post(base_url, headers=headers, json=body)

        st.subheader("Response")
        st.code(json.dumps(response.json(), indent=2), language="json")

        st.subheader("Raw Status")
        st.write(f"Status Code: {response.status_code}")
        st.write("Headers:", dict(response.headers))

    except Exception as e:
        st.error(f"Error: {e}")
