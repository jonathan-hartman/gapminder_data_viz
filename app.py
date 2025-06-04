import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")
st.title("Interact with Gapminder Data")

df = pd.read_csv("Data/gapminder_tidy.csv")

metric_labels = {
    "gdpPercap": "GDP per Capita",
    "lifeExp": "Average Life Expectancy",
    "pop": "Population"
}

def format_metric(metric_raw):
    return metric_labels[metric_raw]

continent_list = list(df["continent"].unique())
metric_list = list(df["metric"].unique())
years_min = int(df["year"].unique().min())
years_max = int(df["year"].unique().max())

with st.sidebar:
    st.subheader("Configure the plot")
    continent = st.selectbox(label="Choose a continent", options=continent_list)
    metric = st.selectbox(
        label="Choose a metric", 
        options=metric_list, 
        format_func=format_metric
    )
    years_to_show = st.slider(
        label="What years should be plotted?", 
        min_value=years_min,
        max_value=years_max,
        value=(years_min, years_max))
    show_data = st.checkbox(label="Show the dataframe used for the plot", value=False)

query = f"continent=='{continent}' & metric=='{metric}'"
df_filtered = df.query(query)
df_filtered = df_filtered[(df_filtered.year >= years_to_show[0]) & (df_filtered.year <= years_to_show[1])]
    
title = f"{metric_labels[metric]} for countries in {continent}"
fig = px.line(
    df_filtered, 
    x="year", 
    y="value", 
    color="country", 
    title=title, 
    labels={"value":"GDP Percap"}
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"This plot shows the {metric_labels[metric]} for countries in {continent}")

if show_data:
    st.dataframe(df_filtered)
