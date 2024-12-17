import streamlit as st
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configuration de la page
st.set_page_config(page_title="Fortune d'Elon Musk", page_icon="💰", layout="wide")

# Actualisation automatique toutes les 10 secondes
st_autorefresh(interval=10_000, limit=None, key="wealth_refresh")

# CSS moderne avec design épuré
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

/* Reset et configurations globales */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Masquer les éléments Streamlit non désirés */
#MainMenu, footer, header[data-testid="stHeader"] {
    display: none;
}

/* Style principal */
.dashboard {
    font-family: 'Inter', sans-serif;
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.header {
    text-align: center;
    margin-bottom: 2rem;
}

.title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 1rem;
}

.wealth-display {
    background: linear-gradient(135deg, #2193b0, #6dd5ed);
    color: white;
    padding: 2rem;
    border-radius: 1rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.amount {
    font-size: 3.5rem;
    font-weight: 800;
    margin: 1rem 0;
}

.details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.detail-card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.8rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.detail-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #666;
    margin-bottom: 0.5rem;
}

.detail-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1a1a1a;
}

.timestamp {
    text-align: center;
    color: #666;
    font-size: 0.9rem;
    margin-top: 2rem;
}

@media (max-width: 768px) {
    .amount {
        font-size: 2.5rem;
    }
    
    .details-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# Constantes et fonctions de calcul identiques au code original
TESLA_SHARES = 411_930_000
SPACEX_VALUE = 147_000_000_000
XAI_VALUE = 27_000_000_000
X_VALUE = 19_000_000_000

def format_money(amount):
    return f"{amount:,.0f} $"

# Reste des fonctions de calcul identiques...

# Affichage avec le nouveau design
wealth = calculate_wealth()

if wealth:
    st.markdown("""
    <div class="dashboard">
        <div class="header">
            <h1 class="title">Fortune d'Elon Musk</h1>
        </div>
        
        <div class="wealth-display">
            <div class="amount">{}</div>
        </div>
        
        <div class="details-grid">
            <div class="detail-card">
                <div class="detail-title">Tesla</div>
                <div class="detail-value">{}</div>
            </div>
            <div class="detail-card">
                <div class="detail-title">SpaceX</div>
                <div class="detail-value">{}</div>
            </div>
            <div class="detail-card">
                <div class="detail-title">xAI</div>
                <div class="detail-value">{}</div>
            </div>
            <div class="detail-card">
                <div class="detail-title">X (Twitter)</div>
                <div class="detail-value">{}</div>
            </div>
        </div>
        
        <div class="timestamp">
            Dernière mise à jour : {}
        </div>
    </div>
    """.format(
        format_money(wealth["total"]),
        format_money(wealth["tesla"]),
        format_money(wealth["spaceX"]),
        format_money(wealth["xAI"]),
        format_money(wealth["x"]),
        wealth["timestamp"].strftime("%H:%M:%S")
    ), unsafe_allow_html=True)
else:
    st.markdown('<div class="dashboard"><div class="wealth-display">Données indisponibles</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close content-wrapper
