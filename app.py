import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile

st.set_page_config(page_title="Age Insights Dashboard", layout="wide")

@st.cache_data
def load_data():
    zip_path = 'cleaned_df.zip'
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            with z.open('cleaned_df.csv') as f:
                return pd.read_csv(f)
    except:
        return None

df1 = load_data()

if df1 is not None:
    st.title("Global Longevity Insights")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Distribution Analysis", "Geographical Insights", "Data Explorer"])

    with tab1:
        st.header("Age Distribution")
        col_a, col_b = st.columns([1, 3])

        with col_a:
            st.subheader("Filters")
            min_age = int(df1['age_of_death'].min())
            max_age = int(df1['age_of_death'].max())

            age_range = st.slider(
                "Select Age Range:",
                min_value=min_age,
                max_value=max_age,
                value=(min_age, max_age),
                key="dist_slider"
            )

        filtered_df = df1[(df1['age_of_death'] >= age_range[0]) & (df1['age_of_death'] <= age_range[1])]

        with col_b:
            fig1 = px.histogram(
                filtered_df, 
                x='age_of_death', 
                nbins=30,
                title=f'Distribution of Age at Death ({age_range[0]} - {age_range[1]})',
                template="plotly_dark",
                color_discrete_sequence=['#00CC96']
            )
            st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.header("Country-wise Comparison")
        col_c, col_d = st.columns([1, 4])

        with col_c:
            option = st.selectbox(
                "Ranking Type:",
                ("Top 10", "Bottom 10"),
                key="geo_select"
            )

        is_ascending = True if option == "Bottom 10" else False

        max_age_by_country = df1.groupby('country')['age_of_death'].max().sort_values(ascending=is_ascending).head(10)
        max_age_df = max_age_by_country.reset_index()
        max_age_df.columns = ['country', 'max_age']

        with col_d:
            fig2 = px.bar(  
                max_age_df, 
                x='country', 
                y='max_age',
                color='max_age',
                title=f"{option} Countries by Maximum Age at Death",
                color_continuous_scale=px.colors.sequential.Viridis,
                template="plotly_dark"
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.header("Raw Dataset")
        st.info(f"Total records found: {len(df1)}")
        search_query = st.text_input("Search records (e.g. name or country):", "")

        if search_query:
            mask = df1.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            st.dataframe(df1[mask], use_container_width=True)
        else:
            st.dataframe(df1.head(100), use_container_width=True)
