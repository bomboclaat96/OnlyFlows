import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="OI Tracker Mobile", layout="wide")

st.title("🔥 Open Interest Tracker")
st.markdown("Deine Live-Daten direkt aus der GitHub-Cloud.")

# CSV einlesen
csv_path = "data/oi_snapshot.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    # Dropdown für Ticker-Auswahl
    tickers = df['ticker'].unique()
    selected_ticker = st.selectbox("Wähle ein Asset:", tickers)
    
    # Filtern nach Ticker
    df_filtered = df[df['ticker'] == selected_ticker]
    
    # Metriken anzeigen
    total_oi = df_filtered['openInterest'].sum()
    st.metric(label=f"Total Open Interest ({selected_ticker})", value=f"{total_oi:,.0f}")
    
    # Verfallstage Filter
    expirations = df_filtered['expiry'].unique()
    selected_expiry = st.selectbox("Verfallstag wählen:", expirations)
    
    df_expiry = df_filtered[df_filtered['expiry'] == selected_expiry]
    
    st.subheader(f"Open Interest nach Strikes ({selected_expiry})")
    
    # Bar Chart für Calls & Puts nach Strike
    fig = px.bar(
        df_expiry, 
        x='strike', 
        y='openInterest', 
        color='type', 
        barmode='group',
        title=f"{selected_ticker} Open Interest (Expiry: {selected_expiry})",
        labels={'strike': 'Strike Price ($)', 'openInterest': 'Open Interest'}
    )
    fig.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    # Rohdaten anzeigen (aufklappbar)
    with st.expander("Rohdaten anzeigen"):
        st.dataframe(df_expiry)
        
else:
    st.warning("Noch keine Daten gefunden! Bitte führe zuerst die GitHub Action aus, damit die CSV erstellt wird.")
