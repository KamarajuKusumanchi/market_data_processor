# To run it
#  % conda activate market_data_processor
#  % which streamlit
# /opt/rajulocal/miniconda3/envs/market_data_processor/bin/streamlit
#  % cd $github/market_data_processor
#  % streamlit run ./src/company_description/screen2.py
#  or
#  % python -m streamlit run ./screen2.py

import streamlit as st
import get_description
import subprocess
import pathlib

st.set_page_config(page_title="Discover companies", layout='wide')
st.title('Company finder')
search_by = st.radio(
    'search by',
    ('ticker', 'keywords'),
    horizontal=True
)

if search_by == 'ticker':
    ticker = st.text_input("Enter a ticker")
    if ticker:
        get_description.update_cache(ticker)
        description = get_description.retrieve_cache(ticker)
        # description = description.replace('\n', ' ')
        # print(description)
        st.text(description)
        # st.write(description)
elif search_by == 'keywords':
    keywords = st.text_input('Enter keywords')
    if keywords:
        words = keywords.split()
        # st.text(keywords)

        cache_dir = get_description.get_cache_dir()
        cache_dir = pathlib.Path(cache_dir)
        cmd = ['git', 'grep', '-i', '--all-match']
        for word in words:
            cmd += ['-e', word]
        # st.text(cmd)

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            cwd=cache_dir
        )
        st.text(result.stdout)
        st.text(result.stderr)