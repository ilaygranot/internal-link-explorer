import pandas as pd

# open the csv file from local machine
df_cluster = pd.read_csv(r"C:\Users\ilayg\Downloads\Raw Data For Internal Link (Explorer)\Wix_blog_cluster_with_crawl_data.csv")
df_Xpath = pd.read_csv(r"C:\Users\ilayg\Downloads\Raw Data For Internal Link (Explorer)\www_blog_xpath_update.csv")

# rename column number 3 to "Body"
df_Xpath.rename(columns={df_Xpath.columns[3]: "Body" },inplace=True)

# show the first 5 rows of the dataframe df_Xpath
df_Xpath.head(5)

# merge the two dataframes on address column base on right join and call it df_merge
df_merge = pd.merge(df_cluster, df_Xpath, on="Address", how="right")

# Create variable for target page
target_page = "https://www.wix.com/logo/maker"
# Create variable for target keyword
target_kw = "logo maker"

# Filter by Target Page & Target Keyword - See all pages that NOT link to target page AND CONTAIN the target keywrods
lp_filter = ~df_Xpath['Body'].str.contains(target_page)
kw_filter = df_Xpath['Body'].str.contains(target_kw, case=False)

# create new df base on the filter and call it new_df and drop the column body, status code and  status
new_df = df_merge[lp_filter & kw_filter].drop(columns=['Body', 'Status Code', 'Status'])

# create new column called intent and if the address contain "how-to" then set the value to "how-to" and if the intent contain "create" then set the value to "create"
new_df['Intent'] = new_df['Address'].apply(lambda x: "how-to" if "how-to" in x else "create")

# show the first 5 rows of the dataframe new_df
new_df


