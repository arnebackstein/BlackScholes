import math
from scipy.stats import norm
from typing import Dict

def black_scholes(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> float:
    """
    Calculate the Black-Scholes price for a European option.
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free interest rate (as a decimal)
    sigma: Volatility of the stock (as a decimal)
    option_type: "call" for call option, "put" for put option
    
    Returns:
    Option price
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Choose 'call' or 'put'.")
    
    return price

def calculate_greeks(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> Dict[str, float]:
    """
    Calculate option Greeks (Delta, Gamma, Theta, Vega, Rho).
    
    Returns Greeks with the following conventions:
    - Delta: Change in option price for $1 change in stock price
    - Gamma: Change in delta for $1 change in stock price
    - Theta: Annual change in option price as time passes (in dollars)
    - Vega: Change in option price for 1% change in volatility
    - Rho: Change in option price for 1% change in interest rate
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    nd1 = norm.pdf(d1)
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    
    delta = Nd1 if option_type == "call" else Nd1 - 1
    gamma = nd1 / (S * sigma * math.sqrt(T))
    vega = S * math.sqrt(T) * nd1
    
    theta_term1 = -(S * sigma * nd1) / (2 * math.sqrt(T))
    if option_type == "call":
        theta = theta_term1 - r * K * math.exp(-r * T) * Nd2
    else:
        theta = theta_term1 + r * K * math.exp(-r * T) * norm.cdf(-d2)
    
    if option_type == "call":
        rho = K * T * math.exp(-r * T) * Nd2
    else:
        rho = -K * T * math.exp(-r * T) * norm.cdf(-d2)
    
    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    } 