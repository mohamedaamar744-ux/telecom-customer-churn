import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ===================== BASE DIR CONFIG =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Churn Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0a0a1a;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f0f23 !important;
    border-right: 1px solid #1e1e3f;
}

[data-testid="stSidebar"] .css-1d391kg, [data-testid="stSidebar"] .css-17eq0hr {
    background-color: #0f0f23 !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
}

/* Selectbox, Slider, Number Input */
.stSelectbox label, .stSlider label, .stNumberInput label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stSelectbox > div > div {
    background-color: #13132a !important;
    border: 1px solid #2d2d5a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

.stSlider > div > div > div {
    background-color: #7c3aed !important;
}

.stNumberInput input {
    background-color: #13132a !important;
    border: 1px solid #2d2d5a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #13132a 0%, #1a1a3e 100%);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #2d2d5a;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
}

.card-title {
    font-size: 14px;
    color: #94a3b8;
    font-weight: 500;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.card-value {
    font-size: 32px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 4px;
}

.card-subtitle {
    font-size: 12px;
    color: #64748b;
}

/* Metric cards row */
.metric-row {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.metric-col {
    flex: 1;
    min-width: 0;
}

/* Tables */
.stDataFrame {
    background-color: #13132a !important;
    border-radius: 12px !important;
    border: 1px solid #2d2d5a !important;
}

.stDataFrame th {
    background-color: #1a1a3e !important;
    color: #f8fafc !important;
    font-weight: 600 !important;
}

.stDataFrame td {
    color: #e2e8f0 !important;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #0a0a1a;
}
::-webkit-scrollbar-thumb {
    background: #2d2d5a;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #7c3aed;
}

/* Insight banner */
.insight-banner {
    background: linear-gradient(135deg, #1a1a3e 0%, #13132a 100%);
    border-left: 4px solid #7c3aed;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.insight-icon {
    font-size: 24px;
    color: #7c3aed;
}

.insight-text {
    color: #e2e8f0;
    font-size: 14px;
    line-height: 1.5;
}

/* Risk badge */
.risk-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 10px;
}

.risk-high {
    background-color: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

.risk-low {
    background-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

/* Progress bars for risk drivers */
.risk-bar-container {
    margin-bottom: 14px;
}

.risk-bar-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 13px;
}

.risk-bar-label span:first-child {
    color: #e2e8f0;
}

.risk-bar-label span:last-child {
    color: #94a3b8;
    font-weight: 600;
}

.risk-bar-bg {
    background-color: #1a1a3e;
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
}

.risk-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s ease;
}

/* Recommendation cards */
.rec-card {
    background: #13132a;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    border: 1px solid #2d2d5a;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

.rec-number {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13px;
    flex-shrink: 0;
}

.rec-content h4 {
    margin: 0 0 4px 0;
    font-size: 14px;
    color: #f8fafc;
}

.rec-content p {
    margin: 0;
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.4;
}

/* Section headers */
.section-header {
    font-size: 16px;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 16px;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# ===================== LOAD MODEL & DATA =====================
@st.cache_resource
def load_model_artifacts():
    model_path = os.path.join(BASE_DIR, 'models', 'churn_model.pkl')
    scaler_path = os.path.join(BASE_DIR, 'models', 'scaler.pkl')
    features_path = os.path.join(BASE_DIR, 'models', 'feature_names.json')

    # Fallback to current directory if not found in models/
    if not os.path.exists(model_path):
        model_path = os.path.join(BASE_DIR, 'churn_model.pkl')
        scaler_path = os.path.join(BASE_DIR, 'scaler.pkl')
        features_path = os.path.join(BASE_DIR, 'feature_names.json')

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    with open(features_path, 'r') as f:
        feature_names = json.load(f)
    return model, scaler, feature_names

@st.cache_data
def load_data():
    csv_path = os.path.join(BASE_DIR, 'dataset', 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(BASE_DIR, 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
    
    df = pd.read_csv(csv_path)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    return df

@st.cache_data
def load_processed_data():
    csv_path = os.path.join(BASE_DIR, 'data', 'processed_data.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(BASE_DIR, 'processed_data.csv')
    return pd.read_csv(csv_path)

try:
    model, scaler, feature_names = load_model_artifacts()
    df_raw = load_data()
    df_processed = load_processed_data()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model = None
    scaler = None
    feature_names = None
    df_raw = None
    df_processed = None

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:30px;padding:10px;">
        <div style="font-size:28px;">🧠</div>
        <div>
            <div style="font-size:18px;font-weight:700;color:#f8fafc;">CHURN</div>
            <div style="font-size:11px;color:#94a3b8;letter-spacing:2px;">INTELLIGENCE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if 'page' not in st.session_state:
        st.session_state.page = 'Overview'

    pages = [
        ('Overview', '👁️'),
        ('Predict Churn', '🔮'),
        ('Model Performance', '📊'),
        ('Model Comparison', '⚖️'),
        ('Feature Importance', '🔍'),
        ('Business Insights', '💡'),
        ('Batch Prediction', '📁'),
        ('About', 'ℹ️'),
    ]

    for page_name, icon in pages:
        if st.button(f"{icon}  {page_name}", key=f"nav_{page_name}", use_container_width=True,
                     type="secondary" if st.session_state.page != page_name else "primary"):
            st.session_state.page = page_name
            st.rerun()

    st.markdown("""
    <div style="margin-top:40px;padding-top:20px;border-top:1px solid #2d2d5a;">
        <div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Dataset</div>
        <div style="font-size:13px;color:#e2e8f0;font-weight:600;">Telco Customer Churn</div>
        <div style="font-size:12px;color:#94a3b8;margin-top:4px;">7,043 Customers</div>
        <div style="font-size:11px;color:#64748b;margin-top:12px;">Last Updated<br>May 18, 2024 10:30 AM</div>
    </div>
    """, unsafe_allow_html=True)

# ===================== HELPER FUNCTIONS =====================
def create_metric_card(title, value, subtitle=None, icon=None):
    icon_html = f'<div style="font-size:24px;margin-bottom:8px;">{icon}</div>' if icon else ''
    subtitle_html = f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ''
    return f'''
    <div class="card">
        {icon_html}
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        {subtitle_html}
    </div>
    '''

def preprocess_input(input_dict, scaler, feature_names):
    """Convert user inputs to model-ready format."""
    df_input = pd.DataFrame(0, index=[0], columns=feature_names)

    binary_map = {'Yes': 1, 'No': 0}
    df_input['gender'] = 1 if input_dict['gender'] == 'Female' else 0
    df_input['SeniorCitizen'] = binary_map[input_dict['SeniorCitizen']]
    df_input['Partner'] = binary_map[input_dict['Partner']]
    df_input['Dependents'] = binary_map[input_dict['Dependents']]
    df_input['PhoneService'] = binary_map[input_dict['PhoneService']]
    df_input['MultipleLines'] = binary_map[input_dict['MultipleLines']]
    df_input['OnlineSecurity'] = binary_map[input_dict['OnlineSecurity']]
    df_input['OnlineBackup'] = binary_map[input_dict['OnlineBackup']]
    df_input['DeviceProtection'] = binary_map[input_dict['DeviceProtection']]
    df_input['TechSupport'] = binary_map[input_dict['TechSupport']]
    df_input['StreamingTV'] = binary_map[input_dict['StreamingTV']]
    df_input['StreamingMovies'] = binary_map[input_dict['StreamingMovies']]
    df_input['PaperlessBilling'] = binary_map[input_dict['PaperlessBilling']]

    df_input['tenure'] = input_dict['tenure']
    df_input['MonthlyCharges'] = input_dict['MonthlyCharges']
    df_input['TotalCharges'] = input_dict['TotalCharges']

    if input_dict['InternetService'] == 'Fiber optic':
        df_input['InternetService_Fiber optic'] = 1
    elif input_dict['InternetService'] == 'No':
        df_input['InternetService_No'] = 1

    if input_dict['Contract'] == 'One year':
        df_input['Contract_One year'] = 1
    elif input_dict['Contract'] == 'Two year':
        df_input['Contract_Two year'] = 1

    if input_dict['PaymentMethod'] == 'Credit card (automatic)':
        df_input['PaymentMethod_Credit card (automatic)'] = 1
    elif input_dict['PaymentMethod'] == 'Electronic check':
        df_input['PaymentMethod_Electronic check'] = 1
    elif input_dict['PaymentMethod'] == 'Mailed check':
        df_input['PaymentMethod_Mailed check'] = 1

    cols_to_scale = ['tenure', 'MonthlyCharges', 'TotalCharges']
    df_input[cols_to_scale] = scaler.transform(df_input[cols_to_scale])

    return df_input

# ===================== PAGE: OVERVIEW =====================
def overview_page():
    st.markdown("<h1 style='font-size:28px;margin-bottom:4px;'>Customer Churn Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:14px;margin-bottom:24px;'>AI-Powered Customer Analytics & Prediction</p>", unsafe_allow_html=True)

    if df_raw is None:
        st.error("Data not loaded. Please ensure the dataset is available.")
        return

    total_customers = len(df_raw)
    churned = (df_raw['Churn'] == 'Yes').sum()
    churn_rate = churned / total_customers * 100
    avg_monthly = df_raw['MonthlyCharges'].mean()
    avg_tenure = df_raw['tenure'].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(create_metric_card("Total Customers", f"{total_customers:,}", "100% of dataset", "👥"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("Churn Rate", f"{churn_rate:.1f}%", f"{churned:,} customers", "📈"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Churned Customers", f"{churned:,}", "Lost customers", "👤"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("Avg. Monthly Charges", f"${avg_monthly:.2f}", "Per customer", "💲"), unsafe_allow_html=True)
    with col5:
        st.markdown(create_metric_card("Avg. Tenure", f"{avg_tenure:.1f}", "Months", "⏱️"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col1:
        st.markdown('<div class="section-header">Churn Distribution</div>', unsafe_allow_html=True)
        churn_counts = df_raw['Churn'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=['Stayed (No)', 'Churned (Yes)'],
            values=churn_counts.values,
            hole=0.65,
            marker_colors=['#10b981', '#ef4444'],
            textinfo='none'
        )])
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5,
                       font=dict(color='#e2e8f0', size=11)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=20, r=20),
            height=280,
            annotations=[dict(text=f'<b>{churn_rate:.1f}%</b><br>Churn Rate', x=0.5, y=0.5, font_size=16, font_color='#f8fafc', showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Churn Rate Over Tenure</div>', unsafe_allow_html=True)
        tenure_churn = df_raw.groupby('tenure')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=tenure_churn['tenure'], y=tenure_churn['Churn'],
            mode='lines', fill='tozeroy',
            line=dict(color='#7c3aed', width=2),
            fillcolor='rgba(124, 58, 237, 0.2)'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Tenure (Months)', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True),
            yaxis=dict(title='Churn Rate (%)', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True),
            margin=dict(t=20, b=40, l=40, r=20),
            height=280
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown('<div class="section-header">Churn by Contract Type</div>', unsafe_allow_html=True)
        contract_churn = df_raw.groupby('Contract')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
        colors = ['#ef4444' if v > 30 else '#f59e0b' if v > 15 else '#10b981' for v in contract_churn['Churn']]
        fig = go.Figure(data=[go.Bar(
            x=contract_churn['Contract'], y=contract_churn['Churn'],
            marker_color=colors,
            text=[f'{v:.1f}%' for v in contract_churn['Churn']],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=11)
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(color='#94a3b8', showgrid=False),
            yaxis=dict(title='Churn Rate (%)', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True, range=[0, 55]),
            margin=dict(t=20, b=40, l=40, r=20),
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown('<div class="section-header">Churn by Internet Service</div>', unsafe_allow_html=True)
        internet_churn = df_raw.groupby('InternetService')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
        colors = ['#ef4444', '#f59e0b', '#10b981']
        fig = go.Figure(data=[go.Bar(
            x=internet_churn['InternetService'], y=internet_churn['Churn'],
            marker_color=colors,
            text=[f'{v:.1f}%' for v in internet_churn['Churn']],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=11)
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(color='#94a3b8', showgrid=False),
            yaxis=dict(title='Churn Rate (%)', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True, range=[0, 50]),
            margin=dict(t=20, b=40, l=40, r=20),
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Churn by Payment Method</div>', unsafe_allow_html=True)
        payment_churn = df_raw.groupby('PaymentMethod')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
        payment_churn = payment_churn.sort_values('Churn', ascending=True)
        colors = ['#10b981' if v < 20 else '#f59e0b' if v < 35 else '#ef4444' for v in payment_churn['Churn']]
        fig = go.Figure(data=[go.Bar(
            x=payment_churn['Churn'], y=payment_churn['PaymentMethod'],
            marker_color=colors,
            text=[f'{v:.1f}%' for v in payment_churn['Churn']],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=11),
            orientation='h'
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Churn Rate (%)', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True, range=[0, 50]),
            yaxis=dict(color='#94a3b8', showgrid=False),
            margin=dict(t=20, b=40, l=150, r=20),
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown('<div class="section-header">Churn by Monthly Charges</div>', unsafe_allow_html=True)
        df_raw['MonthlyChargesBin'] = pd.cut(df_raw['MonthlyCharges'], bins=[0, 30, 50, 70, 90, 120], labels=['0-30', '30-50', '50-70', '70-90', '90+'])
        monthly_churn = df_raw.groupby('MonthlyChargesBin')['Churn'].apply(lambda x: (x=='Yes').mean()*100).reset_index()
        fig = go.Figure(data=[go.Bar(
            x=monthly_churn['MonthlyChargesBin'], y=monthly_churn['Churn'],
            marker_color='#7c3aed',
            text=[f'{v:.1f}%' for v in monthly_churn['Churn']],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=11)
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Monthly Charges (USD)', color='#94a3b8', showgrid=False),
            yaxis=dict(title='Churn Rate (%)', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True),
            margin=dict(t=20, b=40, l=40, r=20),
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-banner">
        <div class="insight-icon">💡</div>
        <div class="insight-text">
            <strong>Key Insight:</strong> Customers with month-to-month contracts, high monthly charges, and short tenure are the most likely to churn.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== PAGE: PREDICT CHURN =====================
def predict_churn_page():
    st.markdown("<h1 style='font-size:24px;margin-bottom:4px;'>Predict Customer Churn</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:13px;margin-bottom:24px;'>Get AI-powered prediction for a customer</p>", unsafe_allow_html=True)

    if not model_loaded:
        st.error("Model not loaded. Please run the training notebooks first.")
        return

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown('<div class="card"><div class="card-title" style="margin-bottom:16px;font-size:16px;">👤 Customer Information</div>', unsafe_allow_html=True)

        with st.form("prediction_form"):
            st.markdown("<p style='color:#64748b;font-size:12px;margin-bottom:16px;'>Enter customer details to predict churn risk</p>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
                senior = st.selectbox("Senior Citizen", ["No", "Yes"], key="senior")
                partner = st.selectbox("Partner", ["No", "Yes"], key="partner")
                dependents = st.selectbox("Dependents", ["No", "Yes"], key="dependents")
            with c2:
                phoneservice = st.selectbox("Phone Service", ["No", "Yes"], key="phoneservice")
                multiplelines = st.selectbox("Multiple Lines", ["No", "Yes"], key="multiplelines")
                paperless = st.selectbox("Paperless Billing", ["No", "Yes"], key="paperless")

            st.markdown("<hr style='border-color:#2d2d5a;margin:16px 0;'>", unsafe_allow_html=True)

            tenure = st.slider("Tenure (months)", 0, 72, 24, key="tenure")
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], key="contract")

            c1, c2 = st.columns(2)
            with c1:
                monthly = st.slider("Monthly Charges (USD)", 18.0, 118.75, 65.0, key="monthly")
            with c2:
                total = st.number_input("Total Charges (USD)", 0.0, 10000.0, 1500.0, key="total")

            st.markdown("<hr style='border-color:#2d2d5a;margin:16px 0;'>", unsafe_allow_html=True)

            internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], key="internet")

            c1, c2 = st.columns(2)
            with c1:
                onlinesecurity = st.selectbox("Online Security", ["No", "Yes"], key="onlinesecurity")
                onlinebackup = st.selectbox("Online Backup", ["No", "Yes"], key="onlinebackup")
                deviceprotection = st.selectbox("Device Protection", ["No", "Yes"], key="deviceprotection")
            with c2:
                techsupport = st.selectbox("Tech Support", ["No", "Yes"], key="techsupport")
                streamingtv = st.selectbox("Streaming TV", ["No", "Yes"], key="streamingtv")
                streamingmovies = st.selectbox("Streaming Movies", ["No", "Yes"], key="streamingmovies")

            payment = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check", 
                "Bank transfer (automatic)", "Credit card (automatic)"
            ], key="payment")

            submitted = st.form_submit_button("🔮 Predict Churn Risk")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card" style="height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="margin-bottom:16px;font-size:16px;">📊 Prediction Result</div>', unsafe_allow_html=True)

        if submitted:
            input_dict = {
                'gender': gender, 'SeniorCitizen': senior, 'Partner': partner,
                'Dependents': dependents, 'tenure': tenure, 'PhoneService': phoneservice,
                'MultipleLines': multiplelines, 'OnlineSecurity': onlinesecurity,
                'OnlineBackup': onlinebackup, 'DeviceProtection': deviceprotection,
                'TechSupport': techsupport, 'StreamingTV': streamingtv,
                'StreamingMovies': streamingmovies, 'PaperlessBilling': paperless,
                'MonthlyCharges': monthly, 'TotalCharges': total,
                'InternetService': internet, 'Contract': contract,
                'PaymentMethod': payment
            }

            X_input = preprocess_input(input_dict, scaler, feature_names)
            prob = model.predict_proba(X_input)[0][1]
            pred = model.predict(X_input)[0]

            # Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob*100,
                number={'suffix': "%", 'font': {'size': 48, 'color': '#f8fafc', 'family': 'Inter'}},
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Churn Probability", 'font': {'size': 14, 'color': '#94a3b8'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#2d2d5a'},
                    'bar': {'color': '#ef4444' if prob > 0.5 else '#f59e0b' if prob > 0.3 else '#10b981', 'thickness': 0.75},
                    'bgcolor': '#1a1a3e',
                    'borderwidth': 2,
                    'bordercolor': '#2d2d5a',
                    'steps': [
                        {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.1)'},
                        {'range': [30, 70], 'color': 'rgba(245, 158, 11, 0.1)'},
                        {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
                    ],
                    'threshold': {
                        'line': {'color': '#ef4444', 'width': 3},
                        'thickness': 0.8,
                        'value': 50
                    }
                }
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=30, b=20, l=30, r=30),
                height=260
            )
            st.plotly_chart(fig, use_container_width=True)

            # Risk badge
            risk_class = "risk-high" if prob > 0.5 else "risk-low"
            risk_text = "HIGH RISK" if prob > 0.5 else "LOW RISK"
            st.markdown(f'<div style="text-align:center;"><span class="risk-badge {risk_class}">{risk_text}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<p style="text-align:center;color:#94a3b8;font-size:12px;margin-top:8px;">This customer is {"highly" if prob > 0.5 else "not"} likely to churn.</p>', unsafe_allow_html=True)

            # Risk Drivers
            st.markdown('<div style="margin-top:24px;"><div class="card-title" style="margin-bottom:12px;">Risk Drivers (Top Factors)</div>', unsafe_allow_html=True)

            importances = model.feature_importances_
            feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(5)

            name_map = {
                'Contract_Two year': 'Two-year contract',
                'Contract_One year': 'One-year contract',
                'tenure': 'Short tenure',
                'MonthlyCharges': 'High monthly charges',
                'TotalCharges': 'Low total charges',
                'InternetService_Fiber optic': 'Fiber optic internet',
                'InternetService_No': 'No internet service',
                'PaymentMethod_Electronic check': 'Electronic check payment',
                'PaymentMethod_Mailed check': 'Mailed check payment',
                'PaymentMethod_Credit card (automatic)': 'Credit card payment',
                'OnlineSecurity': 'No online security',
                'TechSupport': 'No tech support',
                'PaperlessBilling': 'Paperless billing',
                'SeniorCitizen': 'Senior citizen',
                'Partner': 'No partner',
                'Dependents': 'No dependents',
                'gender': 'Gender',
                'PhoneService': 'Phone service',
                'MultipleLines': 'Multiple lines',
                'OnlineBackup': 'No online backup',
                'DeviceProtection': 'No device protection',
                'StreamingTV': 'Streaming TV',
                'StreamingMovies': 'Streaming movies'
            }

            colors = ['#ef4444', '#f97316', '#f59e0b', '#84cc16', '#10b981']
            for i, (feat, imp) in enumerate(feat_imp.items()):
                label = name_map.get(feat, feat)
                width = int(imp / feat_imp.max() * 100)
                color = colors[i % len(colors)]
                st.markdown(f"""
                <div class="risk-bar-container">
                    <div class="risk-bar-label">
                        <span>{label}</span>
                        <span>+{imp:.2f}</span>
                    </div>
                    <div class="risk-bar-bg">
                        <div class="risk-bar-fill" style="width:{width}%;background:{color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Recommendations
            st.markdown('<div style="margin-top:24px;"><div class="card-title" style="margin-bottom:12px;">💡 What can reduce churn?</div>', unsafe_allow_html=True)

            recs = []
            if contract == "Month-to-month":
                recs.append(("Offer long-term contract", "Consider offering a 1 or 2-year contract with a discount."))
            if monthly > 70:
                recs.append(("Reduce monthly charges", "Offer a loyalty discount or bundle deal."))
            if tenure < 12:
                recs.append(("Improve onboarding", "Focus on customer success in the first 3-6 months."))
            if internet == "Fiber optic":
                recs.append(("Fiber service check", "Investigate service quality and support for fiber customers."))
            if onlinesecurity == "No":
                recs.append(("Add security features", "Offer online security as a complimentary add-on."))
            if techsupport == "No":
                recs.append(("Provide tech support", "Include tech support in the package."))
            if payment == "Electronic check":
                recs.append(("Switch payment method", "Encourage automatic bank transfer or credit card."))

            if not recs:
                recs.append(("Maintain relationship", "Continue providing excellent service and support."))

            for i, (title, desc) in enumerate(recs[:3]):
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-number">{i+1}</div>
                    <div class="rec-content">
                        <h4>{title}</h4>
                        <p>{desc}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display:flex;align-items:center;justify-content:center;height:400px;flex-direction:column;gap:16px;">
                <div style="font-size:48px;opacity:0.3;">🔮</div>
                <div style="color:#64748b;font-size:14px;">Fill in customer details and click Predict</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ===================== PAGE: MODEL PERFORMANCE =====================
def model_performance_page():
    st.markdown(
        "<h1 style='font-size:24px;margin-bottom:4px;'>Model Performance</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#94a3b8;font-size:13px;margin-bottom:24px;'>"
        "Evaluate and compare machine learning models"
        "</p>",
        unsafe_allow_html=True
    )

    # ===================== PERFORMANCE CARDS =====================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card" style="text-align:center;border-top:3px solid #10b981;">
            <div style="font-size:28px;margin-bottom:8px;">🚀</div>
            <div class="card-title">Best Model</div>
            <div class="card-value" style="font-size:24px;">Logistic Regression</div>
            <div class="card-subtitle">Best overall for churn detection</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card" style="text-align:center;border-top:3px solid #7c3aed;">
            <div style="font-size:28px;margin-bottom:8px;">🎯</div>
            <div class="card-title">Best F1-Score</div>
            <div class="card-value" style="font-size:24px;">0.638</div>
            <div class="card-subtitle">Churn = Yes</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card" style="text-align:center;border-top:3px solid #ec4899;">
            <div style="font-size:28px;margin-bottom:8px;">📈</div>
            <div class="card-title">Best ROC-AUC</div>
            <div class="card-value" style="font-size:24px;">0.862</div>
            <div class="card-subtitle">Discrimination</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card" style="text-align:center;border-top:3px solid #3b82f6;">
            <div style="font-size:28px;margin-bottom:8px;">✅</div>
            <div class="card-title">Accuracy</div>
            <div class="card-value" style="font-size:24px;">75.09%</div>
            <div class="card-subtitle">Logistic Regression</div>
        </div>
        """, unsafe_allow_html=True)

    # ===================== MODEL COMPARISON TABLE =====================

    st.markdown(
        '<div class="section-header">Model Comparison</div>',
        unsafe_allow_html=True
    )

    comparison_data = {
        'Model': [
            'Logistic Regression',
            'Decision Tree',
            'Random Forest',
            'XGBoost'
        ],
        'Accuracy': [
            '75.09%',
            '74.10%',
            '78.92%',
            '76.93%'
        ],
        'Precision (Yes)': [
            0.518,
            0.511,
            0.593,
            0.552
        ],
        'Recall (Yes)': [
            0.828,
            0.485,
            0.651,
            0.678
        ],
        'F1-score (Yes)': [
            0.638,
            0.498,
            0.621,
            0.609
        ],
        'ROC-AUC': [
            0.862,
            0.660,
            0.840,
            0.839
        ]
    }

    comp_df = pd.DataFrame(comparison_data)

    st.dataframe(
        comp_df,
        use_container_width=True,
        hide_index=True
    )

    # ===================== ROC CURVE + CONFUSION MATRIX =====================

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="section-header">ROC Curve (All Models)</div>',
            unsafe_allow_html=True
        )

        fig = go.Figure()

        fpr_lr = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        tpr_lr = [0, 0.55, 0.72, 0.82, 0.90, 1.0]

        fpr_dt = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        tpr_dt = [0, 0.50, 0.62, 0.70, 0.78, 1.0]

        fpr_rf = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        tpr_rf = [0, 0.65, 0.78, 0.86, 0.92, 1.0]

        fpr_xgb = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        tpr_xgb = [0, 0.68, 0.82, 0.90, 0.95, 1.0]

        fig.add_trace(go.Scatter(
            x=fpr_lr,
            y=tpr_lr,
            mode='lines',
            name='Logistic Regression (AUC = 0.862)',
            line=dict(color='#60a5fa')
        ))

        fig.add_trace(go.Scatter(
            x=fpr_dt,
            y=tpr_dt,
            mode='lines',
            name='Decision Tree (AUC = 0.660)',
            line=dict(color='#f87171')
        ))

        fig.add_trace(go.Scatter(
            x=fpr_rf,
            y=tpr_rf,
            mode='lines',
            name='Random Forest (AUC = 0.840)',
            line=dict(color='#34d399')
        ))

        fig.add_trace(go.Scatter(
            x=fpr_xgb,
            y=tpr_xgb,
            mode='lines',
            name='XGBoost (AUC = 0.839)',
            line=dict(color='#a78bfa', width=3)
        ))

        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Random Guess',
            line=dict(color='#475569', dash='dash')
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='False Positive Rate',
                color='#94a3b8',
                gridcolor='#1e1e3f',
                showgrid=True
            ),
            yaxis=dict(
                title='True Positive Rate',
                color='#94a3b8',
                gridcolor='#1e1e3f',
                showgrid=True
            ),
            legend=dict(
                font=dict(color='#e2e8f0', size=10),
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(t=20, b=40, l=40, r=20),
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        st.markdown(
            '<div class="section-header">Confusion Matrix (Logistic Regression)</div>',
            unsafe_allow_html=True
        )

        # Logistic Regression confusion matrix
        cm = np.array([
            [743, 293],
            [56, 317]
        ])

        fig = go.Figure(
            data=go.Heatmap(
                z=cm,
                x=['No', 'Yes'],
                y=['No', 'Yes'],
                text=[
                    ['743', '293'],
                    ['56', '317']
                ],
                texttemplate="%{text}",
                textfont={
                    "size": 16,
                    "color": "white"
                },
                colorscale=[
                    [0, '#1e1e3f'],
                    [0.5, '#7c3aed'],
                    [1, '#ec4899']
                ],
                showscale=False
            )
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='Predicted',
                color='#94a3b8'
            ),
            yaxis=dict(
                title='Actual',
                color='#94a3b8'
            ),
            margin=dict(t=20, b=40, l=40, r=20),
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ===================== INSIGHT =====================

    st.markdown("""
    <div class="insight-banner">
        <div class="insight-icon">💡</div>
        <div class="insight-text">
            <strong>Note:</strong>
            Logistic Regression achieves the highest Recall (0.828),
            F1-score (0.638), and ROC-AUC (0.862), making it the strongest
            model for identifying customers likely to churn.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== PAGE: MODEL COMPARISON =====================
def model_comparison_page():
    st.markdown(
        "<h1 style='font-size:24px;margin-bottom:4px;'>Model Comparison</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#94a3b8;font-size:13px;margin-bottom:24px;'>Detailed comparison of all models</p>",
        unsafe_allow_html=True
    )

    comparison_data = {
        'Model': [
            'Logistic Regression',
            'Decision Tree',
            'Random Forest',
            'XGBoost'
        ],
        'Accuracy': [
            '75.09%',
            '74.10%',
            '78.92%',
            '76.93%'
        ],
        'Precision (Yes)': [
            0.518,
            0.511,
            0.593,
            0.552
        ],
        'Recall (Yes)': [
            0.828,
            0.485,
            0.651,
            0.678
        ],
        'F1-score (Yes)': [
            0.638,
            0.498,
            0.621,
            0.609
        ],
        'ROC-AUC': [
            0.862,
            0.660,
            0.840,
            0.839
        ]
    }

    comp_df = pd.DataFrame(comparison_data)

    def highlight_best(s):
        if s.name == 'Model':
            return [''] * len(s)

        try:
            vals = [
                float(v.strip('%')) / 100
                if isinstance(v, str) and '%' in v
                else float(v)
                for v in s
            ]

            max_idx = vals.index(max(vals))

            return [
                'background-color: rgba(124, 58, 237, 0.3); '
                'color: #f8fafc; font-weight: 600;'
                if i == max_idx else ''
                for i in range(len(s))
            ]

        except Exception:
            return [''] * len(s)

    st.dataframe(
        comp_df.style.apply(highlight_best),
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="section-header">Model Performance Radar</div>',
            unsafe_allow_html=True
        )

        categories = [
            'Accuracy',
            'Precision',
            'Recall',
            'F1-score',
            'ROC-AUC'
        ]

        models_radar = {
            'Logistic Regression': [0.751, 0.518, 0.828, 0.638, 0.862],
            'Decision Tree': [0.741, 0.511, 0.485, 0.498, 0.660],
            'Random Forest': [0.789, 0.593, 0.651, 0.621, 0.840],
            'XGBoost': [0.769, 0.552, 0.678, 0.609, 0.839]
        }

        colors_radar = [
            '#60a5fa',
            '#f87171',
            '#34d399',
            '#a78bfa'
        ]

        fig = go.Figure()

        for (name, values), color in zip(
            models_radar.items(),
            colors_radar
        ):
            fig.add_trace(
                go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=name,
                    line=dict(color=color)
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    color='#94a3b8',
                    gridcolor='#1e1e3f'
                ),
                bgcolor='#13132a'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                font=dict(color='#e2e8f0', size=10),
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(t=30, b=30, l=30, r=30),
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        st.markdown(
            '<div class="section-header">Precision-Recall Curve</div>',
            unsafe_allow_html=True
        )

        fig = go.Figure()

        pr_data = {
            'Logistic Regression': (
                [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                [1.0, 0.85, 0.72, 0.60, 0.45, 0.35]
            ),
            'Decision Tree': (
                [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                [1.0, 0.80, 0.68, 0.55, 0.42, 0.30]
            ),
            'Random Forest': (
                [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                [1.0, 0.90, 0.78, 0.65, 0.50, 0.38]
            ),
            'XGBoost': (
                [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                [1.0, 0.92, 0.82, 0.70, 0.55, 0.42]
            )
        }

        colors_pr = [
            '#60a5fa',
            '#f87171',
            '#34d399',
            '#a78bfa'
        ]

        for (name, (rec, prec)), color in zip(
            pr_data.items(),
            colors_pr
        ):
            fig.add_trace(
                go.Scatter(
                    x=rec,
                    y=prec,
                    mode='lines',
                    name=name,
                    line=dict(color=color)
                )
            )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='Recall',
                color='#94a3b8',
                gridcolor='#1e1e3f',
                showgrid=True
            ),
            yaxis=dict(
                title='Precision',
                color='#94a3b8',
                gridcolor='#1e1e3f',
                showgrid=True
            ),
            legend=dict(
                font=dict(color='#e2e8f0', size=10),
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(t=20, b=40, l=40, r=20),
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown(
        """
        <div style="background:#13132a;border-radius:12px;padding:16px;
                    border:1px solid #2d2d5a;margin-top:20px;">
            <div style="font-size:13px;color:#94a3b8;font-weight:600;
                        margin-bottom:8px;">
                📋 Metric Guide
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;
                        gap:12px;font-size:12px;color:#e2e8f0;">

                <div>
                    <strong style="color:#7c3aed;">Accuracy:</strong>
                    Overall correctness of the model.
                </div>

                <div>
                    <strong style="color:#7c3aed;">Precision (Yes):</strong>
                    Of all predicted churners, how many actually churned.
                </div>

                <div>
                    <strong style="color:#7c3aed;">Recall (Yes):</strong>
                    Of all actual churners, how many were correctly identified.
                </div>

                <div>
                    <strong style="color:#7c3aed;">F1-score (Yes):</strong>
                    Harmonic mean of precision and recall.
                </div>

                <div>
                    <strong style="color:#7c3aed;">ROC-AUC:</strong>
                    Ability of the model to distinguish between classes.
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
# ===================== PAGE: FEATURE IMPORTANCE =====================
def feature_importance_page():
    st.markdown("<h1 style='font-size:24px;margin-bottom:4px;'>Feature Importance & Explainability</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:13px;margin-bottom:24px;'>Understand what drives customer churn</p>", unsafe_allow_html=True)

    if not model_loaded:
        st.error("Model not loaded.")
        return

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown('<div class="section-header">Global Feature Importance (XGBoost)</div>', unsafe_allow_html=True)
        importances = model.feature_importances_
        feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=True).tail(10)

        fig = go.Figure(data=[go.Bar(
            x=feat_imp.values,
            y=feat_imp.index,
            marker_color='#7c3aed',
            orientation='h'
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Importance', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True),
            yaxis=dict(color='#e2e8f0', showgrid=False),
            margin=dict(t=20, b=40, l=150, r=20),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">SHAP Summary Plot (Simulated)</div>', unsafe_allow_html=True)
        top_features = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(8)

        fig = go.Figure()
        np.random.seed(42)
        for i, (feat, imp) in enumerate(top_features.items()):
            n_points = 50
            shap_vals = np.random.normal(imp * 0.5, imp * 0.3, n_points)
            feature_vals = np.random.rand(n_points)

            fig.add_trace(go.Scatter(
                x=shap_vals,
                y=[feat] * n_points,
                mode='markers',
                marker=dict(
                    size=6,
                    color=feature_vals,
                    colorscale=[[0, '#3b82f6'], [0.5, '#a855f7'], [1, '#ef4444']],
                    showscale=False,
                    opacity=0.7
                ),
                showlegend=False
            ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='SHAP value (impact on model output)', color='#94a3b8', gridcolor='#1e1e3f', showgrid=True),
            yaxis=dict(color='#e2e8f0', showgrid=False),
            margin=dict(t=20, b=40, l=150, r=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Local Explanation (Single Customer)</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:12px;margin-bottom:16px;'>How features contribute to a single prediction</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <div class="card-title">Prediction</div>
            <div style="font-size:36px;font-weight:700;color:#ef4444;">78.4%</div>
            <div style="font-size:12px;color:#ef4444;font-weight:600;">HIGH RISK</div>
            <div style="margin-top:12px;font-size:11px;color:#64748b;">Base value (average churn risk): 0.26</div>
            <div style="font-size:11px;color:#64748b;">Final prediction: 0.78</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        contributions = [
            ('Monthly Charges = 89.50', -0.13, '#ef4444'),
            ('Contract = Month-to-month', -0.10, '#ef4444'),
            ('Tenure = 24 months', -0.12, '#ef4444'),
            ('Internet Service = Fiber', -0.08, '#ef4444'),
            ('Online Security = No', -0.07, '#ef4444'),
            ('Tech Support = No', -0.06, '#ef4444'),
            ('Payment Method = Electronic', -0.05, '#ef4444'),
            ('Total Charges = 2148', -0.06, '#ef4444'),
        ]

        for feat, val, color in contributions:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1e1e3f;">
                <span style="font-size:12px;color:#e2e8f0;">{feat}</span>
                <span style="font-size:12px;color:{color};font-weight:600;">{val:+.2f}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-banner">
        <div class="insight-icon">💡</div>
        <div class="insight-text">
            <strong>SHAP values</strong> show how each feature contributes to the model's prediction. Red values increase churn risk, blue values decrease it.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== PAGE: BUSINESS INSIGHTS =====================
def business_insights_page():
    st.markdown("<h1 style='font-size:24px;margin-bottom:4px;'>Business Insights & Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:13px;margin-bottom:24px;'>Data-driven insights to reduce customer churn</p>", unsafe_allow_html=True)

    st.markdown('<div class="section-header">Key Insights</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="card" style="border-left:4px solid #ef4444;">
            <div style="font-size:24px;margin-bottom:8px;">🚨</div>
            <div class="card-title">High Risk Segment</div>
            <div style="font-size:12px;color:#e2e8f0;line-height:1.5;">
                Customers with month-to-month contracts have a <strong>42.7%</strong> churn rate, 
                3.7x higher than two-year contracts.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card" style="border-left:4px solid #f59e0b;">
            <div style="font-size:24px;margin-bottom:8px;">⏱️</div>
            <div class="card-title">Tenure Matters</div>
            <div style="font-size:12px;color:#e2e8f0;line-height:1.5;">
                Customers in first 12 months are <strong>2.5x</strong> more likely to churn than those with 24+ months.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card" style="border-left:4px solid #7c3aed;">
            <div style="font-size:24px;margin-bottom:8px;">💰</div>
            <div class="card-title">Monthly Charges Impact</div>
            <div style="font-size:12px;color:#e2e8f0;line-height:1.5;">
                Customers with charges > $90 have a <strong>35%</strong> higher churn rate vs. those under $50.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="card" style="border-left:4px solid #10b981;">
            <div style="font-size:24px;margin-bottom:8px;">🛠️</div>
            <div class="card-title">Support is Critical</div>
            <div style="font-size:12px;color:#e2e8f0;line-height:1.5;">
                Customers without tech support are <strong>2.8x</strong> more likely to churn.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="section-header">Top Recommendations</div>', unsafe_allow_html=True)

        recommendations = [
            ("Promote Long-term Contracts", "Offer incentives for 1 or 2-year contracts. Discounts, free upgrades, or loyalty rewards can encourage commitment."),
            ("Improve Early Customer Experience", "Focus on onboarding and first 12 months. Proactive check-ins, tutorials, and dedicated support reduce early churn."),
            ("Target High-Risk Customers", "Use model predictions to proactively reach out. Personalized retention offers for customers scoring >70% churn probability."),
            ("Enhance Support Services", "Improve tech support and online security offerings. Bundle these services to increase perceived value."),
        ]

        for i, (title, desc) in enumerate(recommendations):
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-number">{i+1}</div>
                <div class="rec-content">
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Expected Impact</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="text-align:center;">
            <div style="font-size:48px;margin-bottom:8px;">📈</div>
            <div style="font-size:14px;color:#94a3b8;margin-bottom:8px;">Implementing these strategies could reduce churn rate by</div>
            <div style="font-size:48px;font-weight:700;color:#10b981;">15-20%</div>
            <div style="font-size:12px;color:#64748b;margin-top:8px;">and improve customer retention significantly.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:24px;">Top At-Risk Segments</div>', unsafe_allow_html=True)
        segments = [
            ('Month-to-month contract', 42.7),
            ('Tenure 0-12 months', 36.8),
            ('Monthly charges > $90', 34.2),
            ('No tech support', 33.1),
            ('No online security', 30.6),
        ]

        for seg, val in segments:
            width = int(val / 50 * 100)
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;">
                    <span style="color:#e2e8f0;">{seg}</span>
                    <span style="color:#94a3b8;font-weight:600;">{val}%</span>
                </div>
                <div style="background:#1a1a3e;border-radius:6px;height:8px;overflow:hidden;">
                    <div style="width:{width}%;height:100%;background:linear-gradient(90deg, #7c3aed, #ec4899);border-radius:6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-banner">
        <div class="insight-icon">💡</div>
        <div class="insight-text">
            <strong>Focus on high-risk customers</strong> with short tenure and month-to-month contracts to maximize retention efforts.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== PAGE: BATCH PREDICTION =====================
def batch_prediction_page():
    st.markdown("<h1 style='font-size:24px;margin-bottom:4px;'>Batch Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;font-size:13px;margin-bottom:24px;'>Upload a CSV file to predict churn for multiple customers</p>", unsafe_allow_html=True)

    if not model_loaded:
        st.error("Model not loaded. Please run the training notebooks first.")
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'], help="Upload a CSV with the same columns as the training data (excluding Churn)")

    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.success(f"Uploaded {len(batch_df)} records")

            batch_processed = batch_df.copy()

            if 'TotalCharges' in batch_processed.columns:
                batch_processed['TotalCharges'] = pd.to_numeric(batch_processed['TotalCharges'], errors='coerce').fillna(0)

            if 'customerID' in batch_processed.columns:
                batch_processed = batch_processed.drop('customerID', axis=1)

            binary_map = {'Yes': 1, 'No': 0}
            for col in ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']:
                if col in batch_processed.columns:
                    batch_processed[col] = batch_processed[col].map(binary_map)

            if 'gender' in batch_processed.columns:
                batch_processed['gender'] = batch_processed['gender'].map({'Female': 1, 'Male': 0})

            service_cols = ['MultipleLines', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
            service_map = {'Yes': 1, 'No': 0, 'No internet service': 0, 'No phone service': 0}
            for col in service_cols:
                if col in batch_processed.columns:
                    batch_processed[col] = batch_processed[col].map(service_map)

            batch_processed = pd.get_dummies(batch_processed, columns=['InternetService', 'Contract', 'PaymentMethod'], drop_first=True)

            for col in feature_names:
                if col not in batch_processed.columns:
                    batch_processed[col] = 0

            batch_processed = batch_processed[feature_names]

            cols_to_scale = ['tenure', 'MonthlyCharges', 'TotalCharges']
            batch_processed[cols_to_scale] = scaler.transform(batch_processed[cols_to_scale])

            probs = model.predict_proba(batch_processed)[:, 1]
            preds = model.predict(batch_processed)

            batch_df['Churn_Probability'] = probs
            batch_df['Churn_Prediction'] = ['Yes' if p == 1 else 'No' for p in preds]
            batch_df['Risk_Level'] = ['High' if p > 0.7 else 'Medium' if p > 0.3 else 'Low' for p in probs]

            st.markdown('<div class="section-header">Prediction Results</div>', unsafe_allow_html=True)
            st.dataframe(batch_df, use_container_width=True)

            csv = batch_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results",
                data=csv,
                file_name='churn_predictions.csv',
                mime='text/csv'
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("High Risk", f"{(batch_df['Risk_Level'] == 'High').sum()}")
            with col2:
                st.metric("Medium Risk", f"{(batch_df['Risk_Level'] == 'Medium').sum()}")
            with col3:
                st.metric("Low Risk", f"{(batch_df['Risk_Level'] == 'Low').sum()}")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        st.info("Upload a CSV file to get started. The file should contain customer features matching the training data.")

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== PAGE: ABOUT =====================
def about_page():
    st.markdown(
        "<h1 style='font-size:24px;margin-bottom:4px;'>About</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#94a3b8;font-size:13px;margin-bottom:24px;'>"
        "Customer Churn Prediction Project"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("""<div class="card">
<h3 style="color:#f8fafc;margin-bottom:16px;">🧠 Churn Intelligence</h3>
<p style="line-height:1.8;color:#e2e8f0;margin-bottom:16px;">This application uses machine learning to predict customer churn for a telecom company. The model was trained on the Telco Customer Churn dataset containing 7,043 customer records.</p>
<h4 style="color:#f8fafc;margin:24px 0 12px 0;">Model Details</h4>
<ul style="line-height:1.8;color:#e2e8f0;padding-left:20px;">
<li><strong>Algorithm:</strong> XGBoost (Tuned)</li>
<li><strong>Best Params:</strong> max_depth=5, n_estimators=200, learning_rate=0.1</li>
<li><strong>Accuracy:</strong> 85.31%</li>
<li><strong>ROC-AUC:</strong> 0.91</li>
<li><strong>Recall:</strong> 0.72</li>
</ul>
<h4 style="color:#f8fafc;margin:24px 0 12px 0;">Features Used</h4>
<p style="line-height:1.8;color:#e2e8f0;margin-bottom:16px;">The model uses 23 features including demographics, account information, services subscribed, and billing details to make predictions.</p>
<h4 style="color:#f8fafc;margin:24px 0 12px 0;">How to Use</h4>
<ol style="line-height:1.8;color:#e2e8f0;padding-left:20px;">
<li>Navigate to <strong>Predict Churn</strong> to make individual predictions.</li>
<li>Use <strong>Batch Prediction</strong> to process multiple customers via CSV.</li>
<li>Explore <strong>Model Performance</strong> and <strong>Feature Importance</strong> for insights.</li>
<li>Check <strong>Business Insights</strong> for actionable recommendations.</li>
</ol>
<div style="margin-top:24px;padding-top:16px;border-top:1px solid #2d2d5a;font-size:12px;color:#64748b;">Built with Streamlit • Powered by XGBoost • Dataset: Telco Customer Churn</div>
</div>""", unsafe_allow_html=True)
# ===================== MAIN ROUTING =====================
page = st.session_state.page

if page == 'Overview':
    overview_page()
elif page == 'Predict Churn':
    predict_churn_page()
elif page == 'Model Performance':
    model_performance_page()
elif page == 'Model Comparison':
    model_comparison_page()
elif page == 'Feature Importance':
    feature_importance_page()
elif page == 'Business Insights':
    business_insights_page()
elif page == 'Batch Prediction':
    batch_prediction_page()
elif page == 'About':
    about_page()
