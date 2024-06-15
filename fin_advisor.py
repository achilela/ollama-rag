import streamlit as st
from babel.numbers import format_currency

# Function to perform compound interest calculation
def calculate_compound_interest(principal, annual_rate, years, compounding_periods=12):
    r = annual_rate / 100  # Convert percentage to decimal
    n = compounding_periods
    t = years
    A = principal * (1 + r/n)**(n*t)
    return A

# Function to format currency
def format_kwanza(amount):
    return format_currency(amount, 'AOA', locale='en_US')

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
        'financial_advice': "Financial Advice",
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
        'financial_advice': "Conselho Financeiro",
    }
}

# Sidebar for language selection
language = st.sidebar.selectbox("Choose Language / Escolha o Idioma", ('en', 'pt'))
trans = translations[language]

# Dropdown options
years_options = list(range(1, 21))  # Years from 1 to 20
interest_rate_options = [i / 2 for i in range(0, 101)]  # Interest rates from 0% to 50% in 0.5% increments
principal_options = [i * 5000000 for i in range(1, 21)]  # Principal amounts from 5M to 100M in 5M increments

# Sidebar for user inputs
st.sidebar.header(trans['title'])
years = st.sidebar.selectbox(trans['years'], years_options, index=6)
interest_rate = st.sidebar.selectbox(trans['interest_rate'], interest_rate_options, index=42)
principal = st.sidebar.selectbox(trans['principal'], principal_options, index=9)
monthly_payment = 775000.0

# Main app
st.title(trans['title'])

if st.sidebar.button(trans['calculate']):
    final_amount = calculate_compound_interest(principal, interest_rate, years)
    interest_earned = final_amount - principal
    total_monthly_payments = monthly_payment * 12 * years
    
    st.subheader(trans['financial_advice'])
    st.write(f"{trans['final_amount']}: {format_kwanza(final_amount)}")
    st.write(f"{trans['interest_earned']}: {format_kwanza(interest_earned)}")
    st.write(f"{trans['monthly_payment']}: {format_kwanza(monthly_payment)}")
    st.write(f"{trans['total_monthly_payments']}: {format_kwanza(total_monthly_payments)}")
    
    # Financial advice in chosen language
    if language == 'en':
        st.write(f"""
            With an initial investment of {format_kwanza(principal)} at an annual interest rate of {interest_rate}% over {years} years,
            your final amount will be {format_kwanza(final_amount)}. This includes the principal amount of {format_kwanza(principal)} and interest earned of {format_kwanza(interest_earned)}.
            
            The bank offers a monthly payment of {format_kwanza(monthly_payment)}, totaling {format_kwanza(total_monthly_payments)} over the investment period. 
            This monthly payment is part of the interest accrued, but the compounding effect and remaining balance will continue to grow your investment.
        """)
    else:
        st.write(f"""
            Com um investimento inicial de {format_kwanza(principal)} a uma taxa de juros anual de {interest_rate}% durante {years} anos,
            o seu montante final será de {format_kwanza(final_amount)}. Isso inclui o valor principal de {format_kwanza(principal)} e juros ganhos de {format_kwanza(interest_earned)}.
            
            O banco oferece um pagamento mensal de {format_kwanza(monthly_payment)}, totalizando {format_kwanza(total_monthly_payments)} durante o período de investimento.
            Este pagamento mensal é parte dos juros acumulados, mas o efeito de capitalização e o saldo remanescente continuarão a aumentar seu investimento.
        """)
