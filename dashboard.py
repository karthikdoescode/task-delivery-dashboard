import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Task Delivery Tracker", page_icon="📊", layout="wide")

st.markdown("""<style>.stMetric{background-color:#ffffff;padding:15px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);}</style>""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    data = {'Date': ['14 Nov']*52, 'CS Spoc': ['Ritesh', 'Tanvi', 'Zeeshan', 'Sukhada']*13, 'Brand': ['JP Infra', 'Biogenomics', 'Alcon', 'BookAChange']*13, 'Task': ['Mobile pages', 'LinkedIn Banner', 'Emailer', 'Website']*13, 'Status': ['Pending For Long', 'Delivered', 'WIP', 'Delivered']*13, 'Writer': ['Tanvi', 'Zeeshan', 'Sukhada', 'Ashmita']*13, 'Designer': ['Vishal', 'Mishrin', 'Syona', 'Karen']*13}
    return pd.DataFrame(data)

df = load_data()

st.sidebar.markdown("## 🔍 Filters")
cs_spoc_options = ['All'] + sorted(df['CS Spoc'].unique().tolist())
selected_cs_spoc = st.sidebar.multiselect("CS Spoc", options=cs_spoc_options, default=['All'])
brand_options = ['All'] + sorted(df['Brand'].unique().tolist())
selected_brand = st.sidebar.multiselect("Brand/Client", options=brand_options, default=['All'])
status_options = ['All'] + sorted(df['Status'].unique().tolist())
selected_status = st.sidebar.multiselect("Status", options=status_options, default=['All'])

df_filtered = df.copy()
if 'All' not in selected_cs_spoc:
    df_filtered = df_filtered[df_filtered['CS Spoc'].isin(selected_cs_spoc)]
if 'All' not in selected_brand:
    df_filtered = df_filtered[df_filtered['Brand'].isin(selected_brand)]
if 'All' not in selected_status:
    df_filtered = df_filtered[df_filtered['Status'].isin(selected_status)]

col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Task Delivery Dashboard")
    st.markdown("**Real-time Performance Tracking**")
with col2:
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)
total = len(df_filtered)
delivered = len(df_filtered[df_filtered['Status'] == 'Delivered'])
wip = len(df_filtered[df_filtered['Status'] == 'WIP'])
pending = len(df_filtered[df_filtered['Status'] == 'Pending For Long'])
rate = (delivered / total * 100) if total > 0 else 0

with col1:
    st.metric("📋 Total Tasks", total)
with col2:
    st.metric("✅ Delivered", delivered, f"{rate:.1f}%")
with col3:
    st.metric("🔄 WIP", wip)
with col4:
    st.metric("⏳ Pending", pending, delta_color="inverse")
with col5:
    st.metric("🎯 Delivery Rate", f"{rate:.1f}%")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏆 Leaderboard", "👥 Team"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Status Distribution")
        status_counts = df_filtered['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("CS Spoc Performance")
        cs_perf = df_filtered.groupby('CS Spoc').agg({'Status': lambda x: (x == 'Delivered').sum() / len(x) * 100}).round(1).reset_index()
        cs_perf.columns = ['CS Spoc', 'Delivery Rate %']
        fig2 = px.bar(cs_perf, x='CS Spoc', y='Delivery Rate %', color='Delivery Rate %', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("🏆 CS Spoc Leaderboard")
    lb = df_filtered.groupby('CS Spoc').agg({'Status': [('Total', 'count'), ('Delivered', lambda x: (x == 'Delivered').sum()), ('WIP', lambda x: (x == 'WIP').sum())]})
    lb.columns = ['Total', 'Delivered', 'WIP']
    lb['Delivery %'] = (lb['Delivered'] / lb['Total'] * 100).round(1)
    lb = lb.sort_values('Delivery %', ascending=False)
    st.dataframe(lb.style.background_gradient(cmap='RdYlGn', subset=['Delivery %']), use_container_width=True)

with tab3:
    st.subheader("👥 Team Workload")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Writers**")
        st.dataframe(df_filtered['Writer'].value_counts().head(10), use_container_width=True)
    with col2:
        st.markdown("**Designers**")
        st.dataframe(df_filtered['Designer'].value_counts().head(10), use_container_width=True)
