import pandas as pd
import streamlit as st

@st.cache
def convert_df_cluster(df_cluster):
 # IMPORTANT: Cache the conversion to prevent computation on every rerun
 return df_cluster.to_csv().encode('utf-8')

st.title("Internal Linking Explorer 🎯")

# Handle Download Button State
can_download = False
csv = None
df_cluster = None
uploaded_df_cluster = None
df_xpath = None
uploaded_df_xpath = None

# Upload excel File
col1, col2 = st.columns(2)
with col1:
    uploaded_df_cluster = st.file_uploader("Upload privat_data.csv file", "csv")
    if uploaded_df_cluster is not None:
        df_cluster = pd.read_csv(uploaded_df_cluster)
with col2:
    uploaded_df_xpath = st.file_uploader("Upload sf_data.csv file", "csv")
    if uploaded_df_xpath is not None:
        df_xpath = pd.read_csv(uploaded_df_xpath)

# Generate Interactive Form
with st.form("form"):
    # Ask for user input
    col1, col2 = st.columns(2)
    with col1:
       target_page = st.text_input('Target Page') # Create variable for target page
    with col2:
       target_kw = st.text_input('Target Keywords') # Create variable for target keyword
    # Submit button
    submitted = st.form_submit_button("Apply")
    if submitted:
        if uploaded_df_cluster is None and uploaded_df_xpath is None:
            st.write('Please upload both files first!')
        else:
            # Simple validation
            if target_page == '':
                st.write('Don\'t forget the target_page!')
            elif target_kw == '':
                st.write('Don\'t forget the target_kw!')
            else:
                # rename columns number 3 to "Body" and number 4 to "Text"
                df_xpath.rename(columns={df_xpath.columns[3]: "Body" },inplace=True)
                # rename columns number 4 to "Text"
                df_xpath.rename(columns={df_xpath.columns[4]: "Text" },inplace=True)
                # merge the two dataframes on address column base on right join and call it df_merge
                df_merge = pd.merge(df_cluster, df_xpath, on="Address", how="right")
                # if value = Nan then replace with "No crawl data"
                df_merge.fillna("No Crawl Data", inplace=True)
                # Filter by Target Page & Target Keyword - See all pages that NOT link to target page AND CONTAIN the target keywrods
                lp_filter = ~df_xpath['Body'].str.contains(target_page)
                kw_filter = df_xpath['Text'].str.contains(target_kw, case=False)
                # create new df base on the filter and call it new_df and drop the column body, status code and  status
                new_df = df_merge[lp_filter & kw_filter].drop(columns=['Body','Status Code', 'Status', 'Text'])
                # Preview Data
                st.dataframe(new_df)
                st.write(len(new_df))
                # Generate CSV
                csv = convert_df_cluster(new_df)
                can_download = True
# Show CSV Download Button
if can_download and csv is not None:
    st.download_button("Press to Download",csv,"file.csv","text/csv",key='download-csv')
