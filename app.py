import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Restaurant Insights Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("Dataset.csv")

df = load_data()
df.dropna(subset=["Cuisines", "City", "Latitude", "Longitude"], inplace=True)

# Sidebar
st.sidebar.title("🍽 Filter Options")
selected_city = st.sidebar.selectbox("Select City", options=["All"] + sorted(df["City"].unique().tolist()))

filtered_df = df if selected_city == "All" else df[df["City"] == selected_city]

# Metrics
st.title("📊 Restaurant Insights Dashboard")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏙️ Total Cities", df["City"].nunique())
col2.metric("🍴 Total Restaurants", len(filtered_df))
col3.metric("⭐ Avg. Rating", round(filtered_df["Aggregate rating"].mean(), 2))
col4.metric("🗳️ Avg. Votes", int(filtered_df["Votes"].mean()))

# Top Cuisines
st.markdown("### 🍛 Top 3 Cuisines")
top_cuisines = filtered_df["Cuisines"].str.split(", ").explode().value_counts().head(3).reset_index()
top_cuisines.columns = ["Cuisine", "Count"]
fig1 = px.bar(top_cuisines, x="Cuisine", y="Count", color="Cuisine")
st.plotly_chart(fig1, use_container_width=True)

# Price Range
st.markdown("### 💰 Price Range Distribution")
fig2 = px.histogram(filtered_df, x="Price range", nbins=4, title="Price Range")
st.plotly_chart(fig2, use_container_width=True)

# Rating Distribution
st.markdown("### ⭐ Rating Distribution")
fig3 = px.histogram(filtered_df, x="Aggregate rating", nbins=20)
st.plotly_chart(fig3, use_container_width=True)

# Online Delivery & Table Booking
col5, col6 = st.columns(2)
with col5:
    st.markdown("### 🚚 Online Delivery")
    fig4 = px.pie(filtered_df, names="Has Online delivery", title="Online Delivery Availability")
    st.plotly_chart(fig4, use_container_width=True)

with col6:
    st.markdown("### 📅 Table Booking")
    fig5 = px.pie(filtered_df, names="Has Table booking", title="Table Booking Availability")
    st.plotly_chart(fig5, use_container_width=True)

# Map
st.markdown("### 🗺️ Restaurant Locations (⭐ 5-Star Highlighted)")
filtered_df["Rating Label"] = filtered_df["Aggregate rating"].apply(lambda x: "⭐ 5-Star" if x == 5.0 else "Others")
fig_map = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Rating Label",
    hover_name="Restaurant Name",
    hover_data=["City", "Cuisines"],
    zoom=3,
    height=500
)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# Top Restaurants Table
st.markdown("### 🏆 Top 10 Rated Restaurants")
top10 = filtered_df.sort_values(by="Aggregate rating", ascending=False).head(10)
top10["Restaurant Name"] = top10.apply(
    lambda row: "⭐ " + row["Restaurant Name"] if row["Aggregate rating"] == 5.0 else row["Restaurant Name"],
    axis=1
)
st.dataframe(top10[["Restaurant Name", "City", "Aggregate rating", "Votes"]], use_container_width=True)

# 📬 Contact Section
st.markdown("---")
st.markdown("## 📬 Get in Touch!")
st.markdown(
    """
    <p style='font-size:18px; color:#ccc;'>
        Feel free to connect with me on LinkedIn or check out more projects on GitHub.
    </p>
    <p style='font-size:20px; font-weight:bold; color:#ffffff;'>
        🔗 Mangesh Ambekar
    </p>
    <div style="display: flex; justify-content: left; gap: 20px;">
        <a href="https://www.linkedin.com/in/mangeshsanjayambekar/" target="_blank">
            <img src="https://www.svgrepo.com/show/448234/linkedin.svg" style="width: 40px;" />
        </a>
        <a href="https://github.com/Mangesh0101" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" style="width: 40px;" />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
