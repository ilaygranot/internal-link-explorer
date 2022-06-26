import pandas as pd
import streamlit as st

@st.cache
def convert_df(df):
 # IMPORTANT: Cache the conversion to prevent computation on every rerun
 return df.to_csv().encode('utf-8')

st.title("Internal Linking Explorer 🎃")

# Handle Download Button State
can_download = False
csv = None

# Upload excel File
uploaded_file = st.file_uploader("Choose an .xlsx file", "xlsx")
have_file = False
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    have_file = True
else:
    have_file = False

# Generate Interactive Form
with st.form("form"):
    # Ask for user input
    col1, col2 = st.columns(2)
    with col1:
       target_page = st.text_input('Target Page')
    with col2:
       target_kw = st.text_input('Target Keywords')
    # Submit button
    submitted = st.form_submit_button("Apply")
    if submitted:
        if uploaded_file is None:
            st.write('Please select a file first!')
        else:
            # Simple validation
            if target_page is '':
                st.write('Don\'t forget the target_page!')
            elif target_kw is '':
                st.write('Don\'t forget the target_kw!')
            else:
                # Filter by Target Page & Target Keyword - See all pages that NOT link to target page AND CONTAIN the target keywrods
                lp_filter = ~df['Body'].str.contains(target_page)
                kw_filter = df['Body'].str.contains(target_kw, case=False)
                new_df = df['Address'][lp_filter & kw_filter].to_frame()
                # Preview Data
                st.dataframe(new_df)
                # Generate CSV
                csv = convert_df(new_df)
                can_download = True
# Show CSV Download Button
if can_download and csv is not None:
    st.download_button("Press to Download",csv,"file.csv","text/csv",key='download-csv')