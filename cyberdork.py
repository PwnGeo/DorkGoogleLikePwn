import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import random

# Khóa API và Custom Search Engine ID
API_KEY = "AIzaSyD_rzgjQhpk9X-gBDQhfY-yZmZpnwNXt9s"
CSE_ID = "7436e5db7733242d8"

MIN_DELAY = 1  # Giây
MAX_DELAY = 10  # Giây

@st.cache_data(show_spinner=False)
def perform_search_all_dorks(api_key, cse_id, site, dork_list):
    service = build("customsearch", "v1", developerKey=api_key)
    results_count = {}
    results_per_page = 10
    
    for dork in dork_list:
        full_query = f"{site} {dork.strip()}"
        
        # Thực hiện delay ngẫu nhiên giữa các tìm kiếm
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)
        
        try:
            response = service.cse().list(q=full_query, cx=cse_id, num=results_per_page, start=1).execute()
            total_results = int(response.get('searchInformation', {}).get('totalResults', 0))
            results_count[dork.strip()] = total_results
        except HttpError as e:
            error_msg = str(e)
            if "Request contains an invalid argument." in error_msg:
                st.error("Số lượng query trong ngày của bạn đã hết, vui lòng thử lại vào ngày mai.")
            else:
                st.error(f"Lỗi xảy ra: {error_msg}")

    return results_count

st.set_page_config(page_title="GoogleDorker", page_icon="🔍", layout="wide")

st.markdown("""
    <div style="background-color: #f2f2f2; padding: 20px;">
        <h1 style="text-align: center;">GoogleDorker 🕵️‍♂️</h1>
        <p style="text-align: center;">A professional Google Dorking tool designed for bug hunters and penetration testers.</p>
    </div>
""", unsafe_allow_html=True)

site = st.text_input("Website domain:", placeholder="Enter site:target.com...")

uploaded_file = st.file_uploader("Choose a file containing dorks (one per line)", type=["txt"])

if st.button("Search Dorks") and uploaded_file is not None:
    if not site.startswith("site:"):
        st.warning("Please enter a valid 'site:target.com' format.")
    else:
        dork_list = uploaded_file.read().decode('utf-8').splitlines()
        results_count = perform_search_all_dorks(API_KEY, CSE_ID, site, dork_list)
        
        if results_count:
            st.success("Search completed. See the results below.")
            df_results = pd.DataFrame(list(results_count.items()), columns=["Dork", "Number of Results"])
            st.dataframe(df_results)
            
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="Export Results",
                data=csv,
                file_name="dork_results_summary.csv",
                mime="text/csv",
            )

st.markdown("""
    **Disclaimer:** This tool is for educational and ethical use only. Always obtain proper authorization before conducting any security assessments.
""")

st.sidebar.markdown("## Usage Instructions")
st.sidebar.markdown("""
1. Enter the site in the format: site:target.com
2. Upload a file containing dorks (one per line)
3. Click "Search Dorks"
4. Download the summary of results
""")
