
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('city_day.csv')

# Clean
df = df.drop(columns=['Xylene', 'NH3', 'PM10','NO', 'NO2', 
                       'NOx', 'CO', 'SO2', 'O3', 'Benzene', 
                       'Toluene', 'AQI_Bucket'])
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month_name()
df['AQI'] = df.groupby('City')['AQI'].transform(
    lambda x: x.fillna(x.mean()))
df['PM2.5'] = df.groupby('City')['PM2.5'].transform(
    lambda x: x.fillna(x.mean()))

# App
st.title("🇮🇳 India Air Quality Dashboard")
st.markdown("Real AQI analysis across Indian cities")

# Sidebar filter
cities = st.sidebar.multiselect(
    "Select Cities",
    options=df['City'].unique(),
    default=['Delhi', 'Mumbai', 'Ahmedabad']
)

filtered = df[df['City'].isin(cities)]

# Metric cards
col1, col2, col3 = st.columns(3)
col1.metric("Average AQI", round(filtered['AQI'].mean(), 1))
col2.metric("Worst City", 
    filtered.groupby('City')['AQI'].mean().idxmax())
col3.metric("Worst Month",
    filtered.groupby('Month')['AQI'].mean().idxmax())

# Chart 1 - City comparison
st.subheader("Average AQI by City")
city_aqi = filtered.groupby('City')['AQI'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10,4))
ax.bar(city_aqi.index, city_aqi.values, color='crimson')
ax.set_ylabel('Average AQI')
plt.xticks(rotation=45)
st.pyplot(fig)

# Chart 2 - Yearly trend
st.subheader("AQI Trend Over Years")
yearly = filtered.groupby('Year')['AQI'].mean()
fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.plot(yearly.index, yearly.values, 
         marker='o', color='steelblue', linewidth=2)
ax2.set_ylabel('Average AQI')
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

# Chart 3 - Monthly pattern
st.subheader("AQI by Month")
monthly = filtered.groupby('Month')['AQI'].mean().sort_values(ascending=False)
fig3, ax3 = plt.subplots(figsize=(10,4))
ax3.bar(monthly.index, monthly.values, color='orange')
ax3.set_ylabel('Average AQI')
plt.xticks(rotation=45)
st.pyplot(fig3)

# Raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered)
