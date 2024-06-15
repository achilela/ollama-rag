import streamlit as st

# Function to perform compound interest calculation
def calculate_compound_interest(principal, annual_rate, years, compounding_periods=12):
    r = annual_rate / 100  # Convert percentage to decimal
    n = compounding_periods
    t = years
    A = principal * (1 + r/n)**(n*t)
    return A

# Translation dictionary for English and Portuguese
translations = {
    'en': {
        'title': "Financial Advisor",
        'years': "Years",
        'interest_rate': "Annual Interest Rate (%)",
        'principal': "Investment Capital (Kwanzas)",
        'calculate': "Calculate",
        'final_amount': "Final Amount (including principal)",
        'interest_earned': "Interest Earned",
        'monthly_payment': "Monthly Payment",
        'total_monthly_payments': "Total of Monthly Payments",
    },
    'pt': {
        'title': "Consultor Financeiro",
        'years': "Anos",
        'interest_rate': "Taxa de Juros Anual (%)",
        'principal': "Capital de Investimento (Kwanzas)",
        'calculate': "Calcular",
        'final_amount': "Montante Final (incluindo principal)",
        'interest_earned': "Juros Ganhos",
        'monthly_payment': "Pagamento Mensal",
        'total_monthly_payments': "Total de Pagamentos Mensais",
    }
}

# Sidebar for language selection
language = st.sidebar.selectbox("Choose Language / Escolha o Idioma", ('en', 'pt'))
trans = translations[language]

# Sidebar for user inputs
st.sidebar.header(trans['title'])
years = st.sidebar.number_input(trans['years'], min_value=1, value=7)
interest_rate = st.sidebar.number_input(trans['interest_rate'], min_value=0.0, value=21.0)
principal = st.sidebar.number_input(trans['principal'], min_value=0.0, value=50000000.0)
monthly_payment = 775000.0

# Main app
st.title(trans['title'])

if st.sidebar.button(trans['calculate']):
    final_amount = calculate_compound_interest(principal, interest_rate, years)
    interest_earned = final_amount - principal
    total_monthly_payments = monthly_payment * 12 * years
    
    st.write(f"{trans['final_amount']}: {final_amount:,.2f} Kwanzas")
    st.write(f"{trans['interest_earned']}: {interest_earned:,.2f} Kwanzas")
    st.write(f"{trans['monthly_payment']}: {monthly_payment:,.2f} Kwanzas")
    st.write(f"{trans['total_monthly_payments']}: {total_monthly_payments:,.2f} Kwanzas")
