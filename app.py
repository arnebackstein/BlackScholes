import streamlit as st
import numpy as np
import plotly.graph_objects as go
from black_scholes import black_scholes, calculate_greeks

st.set_page_config(
    page_title="Black-Scholes Calculator",
    page_icon="📈"  
)

st.title("Black-Scholes European Option Price Calculator")

col1, col2 = st.columns(2)

with col1:
    S = st.number_input(
        "Current Stock Price ($)", 
        min_value=1.0, 
        value=100.0, 
        step=1.0,
        help="The current market price of the underlying stock"
    )
    K = st.number_input(
        "Strike Price ($)", 
        min_value=1.0, 
        value=100.0, 
        step=1.0,
        help="The price at which the option can be exercised"
    )
    T = st.number_input(
        "Time to Expiration (years)", 
        min_value=0.1, 
        value=1.0, 
        step=0.1,
        help="Time until the option expires (in years). E.g., 0.5 for 6 months"
    )

with col2:
    r = st.number_input(
        "Risk-free Rate (%)", 
        min_value=0.0, 
        value=5.0, 
        step=0.1,
        help="The risk-free interest rate (usually based on government bonds with the same maturity)"
    ) / 100
    sigma = st.number_input(
        "Volatility (%)", 
        min_value=1.0, 
        value=20.0, 
        step=1.0,
        help="Expected volatility of the underlying stock (standard deviation of annual returns)"
    ) / 100
    option_type = st.selectbox(
        "Option Type", 
        ["call", "put"],
        help="Call option gives right to buy, Put option gives right to sell"
    )

price = black_scholes(S, K, T, r, sigma, option_type)
st.markdown(f"### {option_type.title()} Option Price: ${price:.2f}")

st.markdown("### Option Greeks")
greeks = calculate_greeks(S, K, T, r, sigma, option_type)

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns([1, 2])

with col1:
    st.metric(
        "Delta", 
        f"{greeks['delta']:.4f}", 
        help="Delta measures the rate of change in option value for a 1 dollar change in the underlying stock price. "
             "A delta of 0.5 means the option gains/loses 50 cents for every 1 dollar move in the stock."
    )

with col2:
    st.metric(
        "Gamma", 
        f"{greeks['gamma']:.6f}",
        help="Gamma measures the rate of change in delta for a 1 dollar change in the underlying stock price. "
             "Higher gamma means the option value is more sensitive to price changes."
    )

with col3:
    st.metric(
        "Theta", 
        f"${greeks['theta']:.4f}/year",
        help="Theta measures the rate of time decay in option value per year. "
             "A theta of -10 means the option loses 10 dollars in value per year, all else being equal."
    )

with col4:
    st.metric(
        "Vega", 
        f"${greeks['vega']:.4f}/σ%",
        help="Vega measures the change in option value for a 1% change in volatility. "
             "A vega of 0.15 means the option value changes 15 cents for each 1% change in volatility."
    )

with col5:
    st.metric(
        "Rho", 
        f"${greeks['rho']:.4f}/r%",
        help="Rho measures the change in option value for a 1% change in interest rates. "
             "A rho of 0.10 means the option value changes 10 cents for each 1% change in interest rate."
    )

tab1, tab2, tab3 = st.tabs(["Stock Price Sensitivity", "Volatility Sensitivity", "Greeks Analysis"])

with tab1:
    stock_prices = np.linspace(max(1, S - 50), S + 50, 100)
    prices = [black_scholes(s, K, T, r, sigma, option_type) for s in stock_prices]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_prices, y=prices, mode='lines', name='Option Price'))
    fig.add_vline(x=S, line_dash="dash", annotation_text="Current Stock Price")
    
    fig.update_layout(
        title="Option Price vs Stock Price",
        xaxis_title="Stock Price ($)",
        yaxis_title="Option Price ($)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    vol_range = np.linspace(0.05, 1.0, 100)
    prices = [black_scholes(S, K, T, r, v, option_type) for v in vol_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vol_range * 100, y=prices, mode='lines', name='Option Price'))
    fig.add_vline(x=sigma * 100, line_dash="dash", annotation_text="Current Volatility")
    
    fig.update_layout(
        title="Option Price vs Volatility",
        xaxis_title="Volatility (%)",
        yaxis_title="Option Price ($)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    greek_choice = st.selectbox("Select Greek", ["Delta", "Gamma", "Theta", "Vega", "Rho"])
    stock_prices = np.linspace(max(1, S - 50), S + 50, 100)
    greek_values = [calculate_greeks(s, K, T, r, sigma, option_type)[greek_choice.lower()] 
                   for s in stock_prices]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_prices, y=greek_values, mode='lines', name=f'{greek_choice}'))
    fig.add_vline(x=S, line_dash="dash", annotation_text="Current Stock Price")
    
    fig.update_layout(
        title=f"{greek_choice} vs Stock Price",
        xaxis_title="Stock Price ($)",
        yaxis_title=greek_choice,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True) 