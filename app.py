import streamlit as st
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configuration de la page
st.set_page_config(page_title="Elon Musk Real-Time Fortune", page_icon="💰", layout="centered")

# Rafraîchissement automatique toutes les 10 secondes
st_autorefresh(interval=10_000, limit=None, key="wealth_refresh")

# CSS modifié avec fond blanc
st.markdown("""
<style>
/* Cacher le menu et le footer de Streamlit */
#MainMenu, footer {
    visibility: hidden;
}
/* Masquer le header */
header[data-testid="stHeader"] {
    display: none;
}

/* Import de la police */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;900&display=swap');

body {
  background: #fff;
  font-family: 'Space Grotesk', sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.content-wrapper {
  width: 90%;
  max-width: 700px;
  text-align: center;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 20px 0 10px; /* Adjusted margins */
}

.amount {
  font-size: 54px;
  font-weight: 900;
  color: #f5c40c;
  padding: 20px 30px;
  border-radius: 12px;
  background: #f8f8f8;
  margin: 10px 0 0; /* Removed bottom margin */
}

.amount.update {
  animation: update 0.5s ease-in-out;
}

@keyframes update {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

.details {
  background: #f5f5f5;
  border-radius: 10px;
  padding: 20px;
  font-size: 0.95rem;
  line-height: 1.5;
  color: #333;
  margin-top: 20px; /* Added top margin for spacing */
  box-shadow: none;
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
    padding: 15px 20px;
  }
}
</style>
""", unsafe_allow_html=True)

# Wrapper for content
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Titre de la page
st.markdown('<h1 class="title">Fortune d\'Elon Musk en temps réel</h1>', unsafe_allow_html=True)

# Constantes
TESLA_SHARES = 411_930_000
SPACEX_VALUE = 147_000_000_000
XAI_VALUE = 27_000_000_000
X_VALUE = 19_000_000_000

def format_money(amount):
    return f"{amount:,.0f} $"

def get_tesla_price():
    def attempt():
        ticker = yf.Ticker("TSLA")
        hist = ticker.history(period="1d")
        if not hist.empty and 'Close' in hist.columns:
            return hist['Close'].iloc[-1]
        return None

    price = attempt()
    if price is None:
        price = attempt()
    return price

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

wealth = calculate_wealth()

if wealth:
    st.markdown(f'<div class="amount update">{format_money(wealth["total"])}</div>', unsafe_allow_html=True)
    
    # Consolidate the details section into a single HTML string
    details_html = f"""
    <div class="details">
        <h2>Détails du calcul</h2>
        <p>Cours actuel de Tesla : {format_money(wealth["price"])}</p>
        <p>Actions Tesla détenues : {wealth["tesla_shares"]:,}</p>
        <p>Valeur Tesla = {format_money(wealth["price"])} × {wealth["tesla_shares"]:,} = {format_money(wealth["tesla"])} </p>
        <p>SpaceX : {format_money(wealth["spaceX"])} </p>
        <p>xAI : {format_money(wealth["xAI"])} </p>
        <p>X (Twitter) : {format_money(wealth["x"])} </p>
        <p class="total">Total : {format_money(wealth["total"])}</p>
        <p style="margin-top:20px; color:#666;">Dernière mise à jour : {wealth["timestamp"].strftime("%H:%M:%S")}</p>
    </div>
    """
    st.markdown(details_html, unsafe_allow_html=True)
else:
    st.markdown('<div class="amount">Données indisponibles</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close content-wrapper
