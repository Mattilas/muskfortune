import streamlit as st
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configure the page
st.set_page_config(page_title="Elon Musk Real-Time Fortune", page_icon="💰", layout="centered")

# Auto-refresh every 10 seconds
st_autorefresh(interval=10_000, limit=None, key="wealth_refresh")

# Updated CSS with no white bar under the title
st.markdown("""
<style>
/* Hide Streamlit's main menu and footer */
#MainMenu, footer {
    visibility: hidden;
}
/* Hide the header */
header[data-testid="stHeader"] {
    display: none;
}

/* Import custom font */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;900&display=swap');

html, body {
  margin: 0;
  padding: 0;
}

body {
  background: #fff;
  font-family: 'Space Grotesk', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

.content-wrapper {
  width: 90%;
  max-width: 700px;
  text-align: center;
  margin: 0;
  padding: 0;
}

.title-amount-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0;
  line-height: 1;
}

.amount {
  font-size: 54px;
  font-weight: 900;
  color: #f5c40c;
  padding: 5px 15px;
  border-radius: 12px;
  background: transparent;
  margin: 0;
  display: block;
}

.details {
  background: #f5f5f5;
  border-radius: 10px;
  padding: 20px;
  font-size: 0.95rem;
  line-height: 1.5;
  color: #333;
  margin-top: 0;
  box-shadow: none;
  border: 1px solid #ccc; /* Added for visualization */
}

.details h2 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 15px;
  color: #f5c40c;
}

.details p {
  margin-bottom: 10px;
}

.total {
  font-weight: bold;
  font-size: 1.2em;
  color: #f5c40c;
  margin-top: 20px;
}

/* Override Streamlit's default padding */
div[data-testid="stAppViewContainer"] {
  padding: 0 !important;
}

/* Include padding and border in element's width */
* {
  box-sizing: border-box;
}

/* Remove margins from Streamlit markdown elements */
.stMarkdown {
  margin: 0;
}

@media (max-width: 600px) {
  .title {
    font-size: 24px;
  }

  .amount {
    font-size: 36px;
    padding: 5px 15px;
  }
}
</style>
""", unsafe_allow_html=True)

# Wrapper for content
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Constants
TESLA_SHARES = 411_930_000
SPACEX_VALUE = 147_000_000_000
XAI_VALUE = 27_000_000_000
X_VALUE = 19_000_000_000

def format_money(amount):
    return f"{amount:,.0f} $"

def get_tesla_price():
    ticker = yf.Ticker("TSLA")  # Corrected ticker symbol
    hist = ticker.history(period="1d")
    if not hist.empty and 'Close' in hist.columns:
        return hist['Close'].iloc[-1]
    return None

def calculate_wealth():
    price = get_tesla_price()
    if price is None:
        return None

    tesla_wealth = price * TESLA_SHARES
    total_wealth = tesla_wealth + SPACEX_VALUE + XAI_VALUE + X_VALUE

    return {
        "price": price,
        "tesla_shares": TESLA_SHARES,
        "tesla": tesla_wealth,
        "spaceX": SPACEX_VALUE,
        "xAI": XAI_VALUE,
        "x": X_VALUE,
        "total": total_wealth,
        "timestamp": datetime.now()
    }

# Calculate wealth
wealth = calculate_wealth()

# Debug statement
# st.write(wealth)

# Title and amount wrapper
st.markdown('<div class="title-amount-wrapper">', unsafe_allow_html=True)
st.markdown('<h1 class="title">Fortune d\'Elon Musk en temps réel</h1>', unsafe_allow_html=True)
if wealth:
    st.markdown(f'<div class="amount update">{format_money(wealth["total"])}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="amount">Données indisponibles</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Details section
if wealth:
    st.markdown('<div class="details">', unsafe_allow_html=True)
    st.markdown('<h2>Détails du calcul</h2>', unsafe_allow_html=True)
    st.markdown(f'<p>Cours actuel de Tesla : {format_money(wealth["price"])} par action</p>', unsafe_allow_html=True)
    st.markdown(f'<p>Actions Tesla détenues : {wealth["tesla_shares"]:,}</p>', unsafe_allow_html=True)
    st.markdown(f'<p>Valeur Tesla = {format_money(wealth["price"])} × {wealth["tesla_shares"]:,} = {format_money(wealth["tesla"])} </p>', unsafe_allow_html=True)
    st.markdown(f'<p>SpaceX : {format_money(wealth["spaceX"])} </p>', unsafe_allow_html=True)
    st.markdown(f'<p>xAI : {format_money(wealth["xAI"])} </p>', unsafe_allow_html=True)
    st.markdown(f'<p>X (Twitter) : {format_money(wealth["x"])} </p>', unsafe_allow_html=True)
    st.markdown(f'<p class="total">Total : {format_money(wealth["total"])}</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="margin-top:20px; color:#666;">Dernière mise à jour : {wealth["timestamp"].strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="amount">Données indisponibles</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close content-wrapper
