import streamlit as st
import pandas as pd
import plotly.express as px
import gdown 


file_id = "1YPIfeCvLILSuqFSoKc7rdFd90f_Ioxy0"
url = f"https://drive.google.com/uc?id={file_id}"

gdown.download(url, "cleaned_df.csv", quiet=False)

df1 = pd.read_csv('cleaned_df.csv')

st.title("Age Dataset Visualization")

min_age = int(df1['age_of_death'].min())
max_age = int(df1['age_of_death'].max())

age_range = st.slider(
    "Select Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)


filtered_df = df1[(df1['age_of_death'] >= age_range[0]) & (df1['age_of_death'] <= age_range[1])]


if st.checkbox("Show Age Distribution Histogram", value=True):
    st.subheader("Distribution of Age at Death")
    fig1 = px.histogram(filtered_df, x='age_of_death', nbins=30,
                        title=f'Distribution of Age at Death ({age_range[0]} - {age_range[1]})')
    st.plotly_chart(fig1)


option = st.selectbox(
    "Show Top 10 or Bottom 10 Countries by Max Age?",
    ("Top 10", "Bottom 10")
)

if option == "Top 10":
    max_age_by_country = df1.groupby('country')['age_of_death'].max().sort_values(ascending=False).head(10)
else:
    max_age_by_country = df1.groupby('country')['age_of_death'].max().sort_values(ascending=True).head(10)

max_age_df = max_age_by_country.reset_index()
max_age_df.columns = ['country', 'max_age']

st.subheader(f"{option} Countries by Maximum Age at Death")
fig2 = px.bar(max_age_df, x='country', y='max_age',
              title=f"{option} Countries by Maximum Age at Death")
st.plotly_chart(fig2)
