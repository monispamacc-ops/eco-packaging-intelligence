import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sustainable Packaging Market Intelligence & Feasibility Portal",
    page_icon="📦",
    layout="wide"
)

# App Header
st.title("📦 Sustainable Packaging Market Intelligence & Feasibility Dashboard")
st.markdown("""
*Strategic Decision-Support Portal for Sustainable High-Barrier Paper Packaging Adoption in the Indian Market.*  
Designed to evaluate market sizing, techno-economic parity, and regulatory compliance (EPR) for B2B enterprise clients.
""")

st.markdown("---")

# Sidebar Controls for Simulation Parameters
st.sidebar.header("⚙️ Simulation Parameters")
target_industry = st.sidebar.selectbox(
    "Target Industry Vertical",
    ["FMCG & Dry Foods", "E-Commerce Logistics", "Pharmaceuticals", "Cosmetics & Personal Care"]
)

# Replaced slider with direct typing box
production_volume = st.sidebar.number_input(
    "Annual Packaging Units Required",
    min_value=10_000,
    max_value=100_000_000,
    value=1_500_000,
    step=50_000
)

barrier_requirement = st.sidebar.select_slider(
    "Required Moisture/Oxygen Barrier Level",
    options=["Standard", "Medium High-Barrier", "Ultra High-Barrier (Aseptic/Metalized Replacement)"]
)

epr_penalty_inclusion = st.sidebar.checkbox("Include India EPR Plastic Penalty Factor", value=True)

# Main Section: Market Demand & Regional Heatmap Data
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Regional Demand Hotspots in India")
    st.markdown("Estimated addressable market volume across key Indian industrial clusters for sustainable paper packaging.")
    
    hub_data = pd.DataFrame({
        "Hub": ["NCR (Delhi/Gurugram)", "Mumbai / Pune", "Bengaluru", "Chennai / Tamil Nadu", "Hyderabad", "Ahmedabad"],
        "State": ["Haryana/UP", "Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Gujarat"],
        "Demand Index (MT)": [42000, 55000, 38000, 31000, 24000, 29000],
        "Growth Rate (%)": [14.5, 16.2, 18.0, 12.8, 15.1, 13.4]
    })
    
    fig_map = px.bar(
        hub_data, 
        x="Hub", 
        y="Demand Index (MT)", 
        color="Growth Rate (%)",
        color_continuous_scale="Viridis",
        text="Growth Rate (%)",
        title="Annual Sustainable Packaging Demand & Growth by Industrial Cluster"
    )
    fig_map.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("📊 Segment Breakdown")
    sector_shares = {
        "FMCG & Food": 40,
        "E-Commerce": 30,
        "Pharma": 18,
        "Cosmetics": 12
    }
    fig_pie = px.pie(
        names=list(sector_shares.keys()), 
        values=list(sector_shares.values()),
        hole=0.4,
        title="Market Share Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Section 2: Techno-Economic Cost & Compliance Simulator
st.subheader("💡 Techno-Economic Cost vs. Compliance Simulator")
st.markdown("Comparing traditional multi-layer plastic films against **Bio-Based High-Barrier Paper** alternatives.")

base_plastic_cost = production_volume * 1.25  
bio_paper_cost = production_volume * 1.42      

if epr_penalty_inclusion:
    epr_plastic_tax = production_volume * 0.35 
    total_plastic_cost = base_plastic_cost + epr_plastic_tax
    total_bio_cost = bio_paper_cost - (production_volume * 0.08) 
else:
    total_plastic_cost = base_plastic_cost
    total_bio_cost = bio_paper_cost

m1, m2, m3, m4 = st.columns(4)
m1.metric("Est. Traditional Plastic Cost", f"₹ {total_plastic_cost:,.0f}", delta="High EPR Risk" if epr_penalty_inclusion else "Baseline")
m2.metric("Bio-Based Paper Solution Cost", f"₹ {total_bio_cost:,.0f}", delta=f"{(total_bio_cost - total_plastic_cost)/total_plastic_cost*100:.1f}% vs Plastic", delta_color="inverse")
m3.metric("Carbon Footprint Reduction", f"{production_volume * 0.00045:.1f} Tons CO2e", delta="-65% Emission")
m4.metric("Regulatory Compliance", "Fully Compliant", delta="EPR Exempt")

st.markdown("---")

# Section 3: Scenario Comparison Table
st.subheader("📋 Detailed Material Performance Matrix")
comparison_df = pd.DataFrame({
    "Performance Parameter": ["Oxygen Transmission Rate (OTR)", "Moisture Vapor Transmission (MVTR)", "Biodegradability / Recyclability", "Consumer Brand Appeal", "Machine Adaptability"],
    "Traditional LDPE / Plastic": ["Moderate", "Low (Good barrier)", "Non-recyclable / Landfill", "Standard", "High (Legacy setups)"],
    "Advanced Bio-Coated Paper": ["Superior (Bio-coated)", "Advanced Functional Seal", "100% Recyclable in Paper Stream", "Premium Eco-Branding", "Compatible with Retrofit Modules"]
})
st.dataframe(comparison_df, use_container_width=True)

# Export Functionality
st.markdown("---")
st.subheader("📥 Export Executive Proposal Report")
if st.button("Generate & Download BD Proposal Summary (CSV)"):
    export_data = comparison_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Click to Download Report",
        data=export_data,
        file_name="Sustainable_Packaging_Feasibility_Report.csv",
        mime="text/csv"
    )
    st.success("Proposal report successfully compiled for client presentation!")