import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

# Cấu hình trang
st.set_page_config(page_title="GoogleDorker", page_icon="🔍", layout="wide")

# Tiêu đề và mô tả
st.markdown("""
    <div style="background-color: #f2f2f2; padding: 20px;">
        <h1 style="text-align: center;">GoogleDorker 🕵️‍♂️</h1>
        <p style="text-align: center;">A professional Google Dorking tool designed for bug hunters and penetration testers.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar cho cấu hình
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Google API Key", type="password")
    cse_id = st.text_input("Custom Search Engine ID")

# Main content
with st.container():
    dork = st.text_input("Google Dork:", placeholder="Enter your Google Dork here...")
    start_index = st.number_input("Start Index", min_value=1, value=1, step=1, key="start_index")

    if st.button("Search"):
        if not api_key or not cse_id:
            st.error("Please provide both Google API Key and Custom Search Engine ID in the sidebar.")
        elif not dork:
            st.warning("Please enter a Google Dork to search.")
        else:
            try:
                service = build("customsearch", "v1", developerKey=api_key)
                
                # Tạo DataFrame để lưu kết quả
                data = []
                
                # Thực hiện tìm kiếm
                response = service.cse().list(q=dork, cx=cse_id, start=start_index).execute()
                
                if 'items' in response:
                    for item in response['items']:
                        data.append({
                            'Title': item['title'],
                            'Link': item['link'],
                            'Snippet': item['snippet']
                        })
                
                df = pd.DataFrame(data)
                
                # Tạo nút Export Results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Export Results",
                    data=csv,
                    file_name="google_dork_results.csv",
                    mime="text/csv",
                )
                
                st.success(f"Found {len(df)} results")
                
                # Hiển thị kết quả
                for index, row in df.iterrows():
                    st.markdown(f"### [{row['Title']}]({row['Link']})")
                    st.markdown(row['Snippet'])
                    st.markdown("---")

                # Hiển thị số trang
                total_items = int(response.get('searchInformation', {}).get('totalResults', 0))
                items_per_page = 10

                # Tạo layout cho nút điều hướng
                col1, col2, col3 = st.columns([1, 0.2, 1])
                
                with col1:
                    if start_index > 1:
                        if st.button("Previous Page"):
                            start_index -= 1  # Giảm 1 đơn vị khi bấm Previous
                            st.session_state.start_index = start_index
                            st.experimental_rerun()

                with col3:
                    if 'queries' in response and 'nextPage' in response['queries']:
                        if st.button("Next Page"):
                            start_index += 1  # Tăng 1 đơn vị khi bấm Next
                            st.session_state.start_index = start_index
                            st.experimental_rerun()

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("""
    **Disclaimer:** This tool is for educational and ethical use only. Always obtain proper authorization before conducting any security assessments.
""")

st.sidebar.markdown("## Features")
st.sidebar.markdown("""
- Google Dorking
- Bug Hunting
- Penetration Testing
- Free Google APIs
- Cross-platform compatibility
- Export results to CSV
""")
