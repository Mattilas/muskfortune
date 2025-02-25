import streamlit as st
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configuration de la page
st.set_page_config(page_title="Elon Musk Real-Time Fortune", page_icon="💰", layout="centered")
st_autorefresh(interval=10_000, limit=None, key="wealth_refresh")

def format_money(amount):
    return f"{amount:,.0f} $"

# Utilisation de st.cache_resource pour éviter de re-créer le Ticker trop souvent
@st.cache_resource
def get_ticker():
    return yf.Ticker("TSLA")

def get_tesla_price():
    ticker = get_ticker()
    price = None
    try:
        # Utilisation de fast_info pour une récupération plus légère
        price = ticker.fast_info.get("lastPrice")
    except Exception as e:
        st.error(f"Erreur via fast_info : {e}")

    # Fallback sur l'historique intraday en cas d'échec
    if price is None:
        try:
            hist = ticker.history(period="1d", interval="1m")
            if not hist.empty and "Close" in hist.columns:
                price = hist["Close"].iloc[-1]
        except Exception as e:
            st.error(f"Erreur via l'historique : {e}")
    return price

def calculate_wealth():
    price = get_tesla_price()
    if price is None:
        return None

    TESLA_SHARES_PERCENTAGE = 0.13
    TESLA_OPTIONS_PERCENTAGE = 0.045
    TESLA_PERSONAL_LOANS = 3_500_000_000

    SPACEX_VALUE = 350_000_000_000
    SPACEX_SHARES = 0.42

    XAI_VALUE = 50_000_000_000
    XAI_SHARES = 0.54

    X_INITIAL_VALUE = 44_000_000_000
    X_DEVALUATION = 0.72
    X_VALUE = X_INITIAL_VALUE * (1 - X_DEVALUATION)
    X_SHARES = 0.79

    BORING_COMPANY_VALUE = 7_000_000_000
    BORING_COMPANY_SHARES = 0.90

    NEURALINK_VALUE = 8_000_000_000
    NEURALINK_SHARES = 0.90

    tesla_shares = 3_210_000_000
    tesla_owned_shares = tesla_shares * TESLA_SHARES_PERCENTAGE
    tesla_options_shares = tesla_shares * TESLA_OPTIONS_PERCENTAGE
    tesla_total_shares = tesla_owned_shares + tesla_options_shares
    tesla_wealth = (price * tesla_total_shares) - TESLA_PERSONAL_LOANS

    spacex_wealth = SPACEX_VALUE * SPACEX_SHARES
    xai_wealth = XAI_VALUE * XAI_SHARES
    x_wealth = X_VALUE * X_SHARES
    boring_wealth = BORING_COMPANY_VALUE * BORING_COMPANY_SHARES
    neuralink_wealth = NEURALINK_VALUE * NEURALINK_SHARES

    total_wealth = (tesla_wealth + spacex_wealth + xai_wealth +
                    x_wealth + boring_wealth + neuralink_wealth)

    return {
        "price": price,
        "total": total_wealth,
        "timestamp": datetime.now()
    }

wealth = calculate_wealth()

if wealth:
    st.markdown(f'<h2>Fortune d\'Elon Musk : {format_money(wealth["total"])}</h2>', unsafe_allow_html=True)
    st.write(f"Prix de l'action Tesla : {format_money(wealth['price'])}")
    st.write(f"Dernière mise à jour : {wealth['timestamp'].strftime('%H:%M:%S')}")
else:
    st.markdown('<h2>Données indisponibles</h2>', unsafe_allow_html=True)
