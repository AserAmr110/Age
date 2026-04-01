import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile


@st.cache_data
def load_data():
    with zipfile.ZipFile("cleaned_df.zip", 'r') as z:
        df = pd.read_csv(z.open("cleaned_df.csv"))  
    return df

df1 = load_data()

st.title("Age Dataset Visualization")


min_age = int(df1['age_of_death'].min())
max_age = int(df1['age_of_death'].max())

age_range = st.slider(
    "Select Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

filtered_df = df1[
    (df1['age_of_death'] >= age_range[0]) &
    (df1['age_of_death'] <= age_range[1])
]


if st.checkbox("Show Age Distribution Histogram", value=True):
    st.subheader("Distribution of Age at Death")
    fig1 = px.histogram(
        filtered_df,
        x='age_of_death',
        nbins=30,
        title=f'Distribution of Age at Death ({age_range[0]} - {age_range[1]})'
    )
    st.plotly_chart(fig1)

# اختيار Top أو Bottom
option = st.selectbox(
    "Show Top 10 or Bottom 10 Countries by Max Age?",
    ("Top 10", "Bottom 10")
)

# استخدم filtered_df (أحسن)
if option == "Top 10":
    max_age_by_country = filtered_df.groupby('country')['age_of_death'].max().sort_values(ascending=False).head(10)
else:
    max_age_by_country = filtered_df.groupby('country')['age_of_death'].max().sort_values(ascending=True).head(10)

max_age_df = max_age_by_country.reset_index()
max_age_df.columns = ['country', 'max_age']

st.subheader(f"{option} Countries by Maximum Age at Death")
fig2 = px.bar(
    max_age_df,
    x='country',
    y='max_age',
    title=f"{option} Countries by Maximum Age at Death"
)

st.plotly_chart(fig2)