import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Khóa API cố định và Custom Search Engine ID
API_KEY = "AIzaSyBaYH0muWGmDoi7cOM39RFw0hYlplJZIc0"
CSE_ID = "76c666bdc600c4b61"

# Hàm tìm kiếm nâng cao với caching để lưu trữ kết quả tìm kiếm
@st.cache_data(show_spinner=False)
def perform_search(api_key, cse_id, dork, start_index):
    service = build("customsearch", "v1", developerKey=api_key)
    results_per_page = 10  # Số kết quả mỗi trang
    data = []
    total_results = 0

    try:
        response = service.cse().list(q=dork, cx=cse_id, num=results_per_page, start=start_index).execute()
        items = response.get('items', [])
        data.extend([
            {'Title': item.get('title'), 'Link': item.get('link'), 'Snippet': item.get('snippet')}
            for item in items
        ])
        
        # Lấy số lượng kết quả tổng chỉ khi là trang đầu tiên
        if start_index == 1:
            total_results = int(response.get('searchInformation', {}).get('totalResults', 0))
    except HttpError as e:
        error_msg = str(e)
        if "Request contains an invalid argument." in error_msg:
            st.error("Số lượng query trong ngày của bạn đã hết, vui lòng thử lại vào ngày mai.")
        else:
            st.error(f"Lỗi xảy ra: {error_msg}")
    
    return pd.DataFrame(data), total_results

# Khởi tạo cấu hình giao diện Streamlit
st.set_page_config(page_title="GoogleDorker", page_icon="🔍", layout="wide")

# Tiêu đề và mô tả
st.markdown("""
    <div style="background-color: #f2f2f2; padding: 20px;">
        <h1 style="text-align: center;">GoogleDorker 🕵️‍♂️</h1>
        <p style="text-align: center;">A professional Google Dorking tool designed for bug hunters and penetration testers.</p>
    </div>
""", unsafe_allow_html=True)

# Khởi tạo session state cho start_index, tổng số kết quả và kết quả tìm kiếm
if 'start_index' not in st.session_state:
    st.session_state.start_index = 1
if 'results_df' not in st.session_state:
    st.session_state.results_df = pd.DataFrame()  # Khởi tạo DataFrame rỗng
if 'total_results' not in st.session_state:
    st.session_state.total_results = 0  # Số lượng kết quả tổng

# Main content
with st.container():
    dork = st.text_input("Google Dork:", placeholder="Enter your Google Dork here...")
    start_index = st.session_state.start_index

    if st.button("Search"):
        if not dork:
            st.warning("Please enter a Google Dork to search.")
        else:
            # Đặt lại dữ liệu khi tìm kiếm mới
            st.session_state.start_index = 1
            st.session_state.results_df, st.session_state.total_results = perform_search(API_KEY, CSE_ID, dork, st.session_state.start_index)

    # Hiển thị kết quả nếu đã có kết quả tìm kiếm
    if not st.session_state.results_df.empty:
        df = st.session_state.results_df

        # Hiển thị số lượng kết quả tìm thấy từ lần tìm kiếm đầu tiên
        st.success(f"Found {st.session_state.total_results} results" if st.session_state.total_results else "Found results")

        # Hiển thị kết quả trong bảng
        st.dataframe(df)

        # Tạo layout cho nút điều hướng
        col1, col2, col3 = st.columns([1, 0.2, 1])

        with col1:
            if start_index > 1:
                if st.button("Previous Page"):
                    st.session_state.start_index -= 10
                    # Không cần query lại mà lấy từ cache
                    st.session_state.results_df, _ = perform_search(API_KEY, CSE_ID, dork, st.session_state.start_index)

        with col3:
            if st.button("Next Page"):
                st.session_state.start_index += 10
                st.session_state.results_df, _ = perform_search(API_KEY, CSE_ID, dork, st.session_state.start_index)

        # Tạo nút Export Results nằm ở cuối cùng
        csv = df.to_csv(index=False)
        st.download_button(
            label="Export Results",
            data=csv,
            file_name="google_dork_results.csv",
            mime="text/csv",
        )

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
