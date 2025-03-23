import streamlit as st
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# Set Dark Theme
st.set_page_config(layout="wide", page_title="Black-Scholes Pricing Model")
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #1E1E1E;
    }
    .stSidebar {
        background-color: #2E2E2E;
    }
    .stNumberInput > div > div > input {
        background-color: #3E3E3E;
        color: #FFFFFF;
    }
    .stSlider > div > div > div > div {
        background-color: #3E3E3E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Black-Scholes Formula
def black_scholes(S, K, T, r, sigma, option_type="call"):
    """Calculate Black-Scholes option price for call or put."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    return price

# Heatmap Function with Fixed X-Axis Spacing
def generate_heatmap(S, K, T, r, sigma, spot_range, vol_range, option_type="call"):
    """Generate a heatmap of option prices with a white background and adjusted x-axis."""
    prices = np.zeros((len(vol_range), len(spot_range)))
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            prices[i, j] = black_scholes(spot, K, T, r, vol, option_type)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        prices, 
        xticklabels=np.round(spot_range, 1),  # Round to 1 decimal point
        yticklabels=np.round(vol_range, 3), 
        annot=True, 
        fmt=".2f", 
        cmap="viridis", 
        ax=ax,
        cbar_kws={'label': option_type.upper()},
        vmin=0  # Ensure color bar starts at 0
    )
    ax.set_title(f"{option_type.capitalize()} Price Heatmap", color="white")
    ax.set_xlabel("Spot Price", color="white")
    ax.set_ylabel("Volatility", color="white")
    ax.tick_params(colors="white")
    
    # Adjust x-axis tick labels to avoid overlap
    ax.set_xticks(ax.get_xticks()[::2])  # Show every other label
    ax.set_xticklabels(np.round(spot_range[::2], 1), rotation=45, ha="right")  # Rotate for better readability
    
    # Set heatmap background to white
    ax.set_facecolor("white")
    # Set figure background to match the dark theme
    fig.patch.set_facecolor("#1E1E1E")
    # Ensure the colorbar label and ticks are white
    cbar = ax.collections[0].colorbar
    cbar.set_label(option_type.upper(), color="white")
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.get_yticklabels(), color="white")
    
    return fig

# Streamlit App
st.title("Black-Scholes Pricing Model")

# Sidebar with Name and LinkedIn at the Top
st.sidebar.markdown(
    """
    **Syed Sharjeel Jafri**  
    [LinkedIn](https://www.linkedin.com/in/sharjeel-jafri-904475149/)
    """,
    unsafe_allow_html=True
)

# Sidebar Inputs
st.sidebar.header("Input Parameters")
S = st.sidebar.number_input("Current Asset Price", min_value=1.0, value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price", min_value=1.0, value=100.0, step=1.0)
T = st.sidebar.number_input("Time to Maturity (Years)", min_value=0.01, value=1.0, step=0.01)
sigma = st.sidebar.number_input("Volatility (σ)", min_value=0.01, value=0.2, step=0.01)
r = st.sidebar.number_input("Risk-Free Interest Rate", min_value=0.0, value=0.05, step=0.01)

# Heatmap Parameters
st.sidebar.header("Heatmap Parameters")
spot_min = st.sidebar.number_input("Min Spot Price", value=S * 0.8, step=1.0)
spot_max = st.sidebar.number_input("Max Spot Price", value=S * 1.2, step=1.0)
vol_min = st.sidebar.slider("Min Volatility for Heatmap", 0.01, 1.0, sigma * 0.5)
vol_max = st.sidebar.slider("Max Volatility for Heatmap", 0.01, 1.0, sigma * 1.5)

# Display Input Parameters in Main Panel
st.subheader("Input Parameters")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Current Asset Price", f"{S:,.2f}")
col2.metric("Strike Price", f"{K:,.2f}")
col3.metric("Time to Maturity (Years)", f"{T:.2f}")
col4.metric("Volatility (σ)", f"{sigma:.2f}")
col5.metric("Risk-Free Interest Rate", f"{r:.2f}")

# Calculate Option Prices
call_price = black_scholes(S, K, T, r, sigma, "call")
put_price = black_scholes(S, K, T, r, sigma, "put")

# Display Option Prices
st.subheader("Option Prices")
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f"""
        <div style='background-color: #D4EFDF; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: black;'>CALL Value</h3>
            <h2 style='color: black;'>${call_price:.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div style='background-color: #FADBD8; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: black;'>PUT Value</h3>
            <h2 style='color: black;'>${put_price:.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Heatmap Section
st.subheader("Options Price - Interactive Heatmap")
st.markdown(
    "Explore how option prices fluctuate with varying 'Spot Price' and 'Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price':",
    unsafe_allow_html=True
)

# Generate Heatmaps
spot_range = np.linspace(spot_min, spot_max, 10)
vol_range = np.linspace(vol_min, vol_max, 10)

col1, col2 = st.columns(2)
with col1:
    fig_call = generate_heatmap(S, K, T, r, sigma, spot_range, vol_range, "call")
    st.pyplot(fig_call)
with col2:
    fig_put = generate_heatmap(S, K, T, r, sigma, spot_range, vol_range, "put")
    st.pyplot(fig_put)