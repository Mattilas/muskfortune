import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configuration de la page
st.set_page_config(page_title="Elon Musk Real-Time Fortune", page_icon="💰", layout="centered")

# Rafraîchissement automatique toutes les 10 secondes
st_autorefresh(interval=10_000, limit=None, key="wealth_refresh")

# CSS personnalisé
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
  background: #080808;
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
  margin: 20px 0 10px;
}

.amount {
  font-size: 54px;
  font-weight: 900;
  color: #f5c40c;
  padding: 20px 30px;
  border-radius: 12px;
  background: #f8f8f8;
  margin: 10px 0 0;
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
  margin-top: 20px;
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

# Wrapper pour le contenu
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Titre de la page
st.markdown('<h1 class="title">Fortune d\'Elon Musk en temps réel</h1>', unsafe_allow_html=True)

# --- Constantes ---
TESLA_SHARES_PERCENTAGE = 0.13      # 13% des actions détenues
TESLA_OPTIONS_PERCENTAGE = 0.045      # 4.5% des options
TESLA_PERSONAL_LOANS = 3_500_000_000  # Prêts personnels

SPACEX_VALUE = 350_000_000_000
SPACEX_SHARES = 0.42

X_INITIAL_VALUE = 44_000_000_000
X_DEVALUATION = 0.72
X_VALUE = X_INITIAL_VALUE * (1 - X_DEVALUATION)
X_SHARES = 0.79

XAI_VALUE = 50_000_000_000
XAI_SHARES = 0.54

BORING_COMPANY_VALUE = 7_000_000_000
BORING_COMPANY_SHARES = 0.90

NEURALINK_VALUE = 8_000_000_000
NEURALINK_SHARES = 0.90

# --- Fonctions utilitaires ---
def format_money(amount):
    return f"{amount:,.0f} $"

# Récupération du prix de Tesla via CNBC
@st.cache_data(ttl=60)
def get_tesla_price():
    try:
        url = "https://www.cnbc.com/quotes/TSLA"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extraction du prix via la classe "QuoteStrip-lastPrice"
        price_span = soup.find('span', class_="QuoteStrip-lastPrice")
        if price_span:
            return float(price_span.text.strip().replace(',', ''))
    except Exception as e:
        st.error(f"Erreur lors de la récupération du prix de l'action Tesla : {e}")
    return None

# Calcul de la fortune détaillée
def calculate_wealth():
    price = get_tesla_price()
    if price is None:
        return None
    
    # Nombre total d'actions Tesla (données actualisées)
    tesla_shares = 3_210_000_000  # 3.21 milliards d'actions
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
        "tesla_shares": tesla_total_shares,
        "tesla_owned": tesla_owned_shares,
        "tesla_options": tesla_options_shares,
        "tesla": tesla_wealth,
        "spaceX": spacex_wealth,
        "xAI": xai_wealth,
        "x": x_wealth,
        "boring": boring_wealth,
        "neuralink": neuralink_wealth,
        "total": total_wealth,
        "timestamp": datetime.now()
    }

wealth = calculate_wealth()

if wealth:
    st.markdown(f'<div class="amount update">{format_money(wealth["total"])}</div>', unsafe_allow_html=True)
    
    details_html = f"""
    <div class="details">
        <h2>Détails du calcul</h2>
        <p>Cours actuel de Tesla : {format_money(wealth["price"])}</p>
        <p>Actions Tesla détenues : {wealth["tesla_owned"]:,.0f} ({TESLA_SHARES_PERCENTAGE*100:.1f}%)</p>
        <p>Options Tesla : {wealth["tesla_options"]:,.0f} ({TESLA_OPTIONS_PERCENTAGE*100:.1f}%)</p>
        <p>Valeur Tesla totale : {format_money(wealth["tesla"])} *</p>
        <p>SpaceX ({SPACEX_SHARES*100:.0f}%) : {format_money(wealth["spaceX"])}</p>
        <p>xAI ({XAI_SHARES*100:.0f}%) : {format_money(wealth["xAI"])}</p>
        <p>X ({X_SHARES*100:.0f}%) : {format_money(wealth["x"])}</p>
        <p>The Boring Company ({BORING_COMPANY_SHARES*100:.0f}%) : {format_money(wealth["boring"])}</p>
        <p>Neuralink ({NEURALINK_SHARES*100:.0f}%) : {format_money(wealth["neuralink"])}</p>
        <p class="total">Total : {format_money(wealth["total"])}</p>
        <p style="font-size:0.8em; color:#666;">* Après déduction des prêts personnels de {format_money(TESLA_PERSONAL_LOANS)}</p>
        <p style="margin-top:20px; color:#666;">Dernière mise à jour : {wealth["timestamp"].strftime("%H:%M:%S")}</p>
    </div>
    """
    st.markdown(details_html, unsafe_allow_html=True)
else:
    st.markdown('<div class="amount">Données indisponibles</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)