# To run it
#  % conda activate market_data_processor
#  % which streamlit
# /opt/rajulocal/miniconda3/envs/market_data_processor/bin/streamlit
#  % cd $github/market_data_processor/src/company_description
#  % streamlit run ./screen1.py

import streamlit as st
import get_description

st.set_page_config(page_title="Company Description", layout='wide')
st.title("Get company description from ticker")
ticker = st.text_input("Enter a ticker")

if ticker:
    get_description.update_cache(ticker)
    description = get_description.retrieve_cache(ticker)
    # description = description.replace('\n', ' ')
    # print(description)
    st.text(description)
    # st.write(description)
