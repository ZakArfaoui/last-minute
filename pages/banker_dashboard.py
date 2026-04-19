import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Assessment · Banker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #f8f9fb !important;
    color: #111827 !important;
}
.stApp { background: #f8f9fb !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 2rem 2.5rem; max-width: 1200px; }

.page-header {
    display: flex; justify-content: space-between; align-items: center;
    background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 1rem 1.5rem; margin-bottom: 2rem;
}
.header-title { font-size: 1rem; font-weight: 600; color: #111827; }
.header-sub { font-size: 0.75rem; color: #6b7280; margin-top: 2px; }
.header-badge {
    font-size: 0.7rem; font-weight: 600;
    background: #eff6ff; color: #1d4ed8;
    border: 1px solid #bfdbfe; border-radius: 20px; padding: 4px 12px;
}
.header-time { font-size: 0.75rem; color: #9ca3af; }

.section-title {
    font-size: 0.68rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px; color: #6b7280;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e5e7eb;
}
.form-card {
    background: #fff; border: 1px solid #e5e7eb;
    border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem;
}

.stNumberInput input, .stTextInput input {
    background: #f9fafb !important; border: 1px solid #d1d5db !important;
    border-radius: 6px !important; color: #111827 !important; font-size: 0.875rem !important;
}
.stSelectbox > div > div {
    background: #f9fafb !important; border: 1px solid #d1d5db !important;
    border-radius: 6px !important; color: #111827 !important;
}
label { color: #374151 !important; font-size: 0.8rem !important; font-weight: 500 !important; }
.stSlider > div > div > div { background: #e5e7eb !important; }
.stSlider > div > div > div > div { background: #2563eb !important; }

.stButton > button {
    background: #1d4ed8 !important; color: #fff !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.875rem !important; padding: 0.65rem 1rem !important;
}
.stButton > button:hover { background: #1e40af !important; }

.banner { border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 1rem; }
.banner-approve { background: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid #16a34a; }
.banner-review  { background: #fffbeb; border: 1px solid #fcd34d; border-left: 4px solid #d97706; }
.banner-decline { background: #fef2f2; border: 1px solid #fca5a5; border-left: 4px solid #dc2626; }
.banner-label   { font-size: 0.68rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
.banner-verdict { font-size: 1.15rem; font-weight: 600; }
.banner-score   { font-size: 0.78rem; margin-top: 4px; color: #4b5563; }
.banner-note    { font-size: 0.8rem; color: #6b7280; margin-top: 8px; line-height: 1.55; }

.kpi-chip {
    background: #f9fafb; border: 1px solid #e5e7eb;
    border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.75rem;
}
.kpi-label { font-size: 0.68rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.kpi-value { font-size: 1.35rem; font-weight: 600; }
.kpi-sub   { font-size: 0.7rem; color: #9ca3af; margin-top: 2px; }

.mtable { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.mtable th {
    background: #f3f4f6; color: #6b7280; font-size: 0.68rem; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
    padding: 0.6rem 0.85rem; text-align: left; border-bottom: 1px solid #e5e7eb;
}
.mtable td { padding: 0.65rem 0.85rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
.mtable td:last-child { font-weight: 500; color: #111827; text-align: right; }
.mtable tr:last-child td { border-bottom: none; }

.note-card {
    background: #f9fafb; border: 1px solid #e5e7eb;
    border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.65rem;
}
.note-title { font-size: 0.8rem; font-weight: 600; color: #111827; margin-bottom: 3px; }
.note-body  { font-size: 0.78rem; color: #6b7280; line-height: 1.55; }

.divider { border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }

.footer-note {
    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;
    padding: 0.85rem 1.1rem; font-size: 0.78rem; color: #1e40af; line-height: 1.6; margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Feature columns (must match model training order) ────────────────────────────
FEATURE_COLUMNS = [
    'debt_ratio', 'saving_rate', 'stability_points', 'CREDIT_DAY_OVERDUE',
    'NAME_CONTRACT_STATUS', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
    'credit_income_ratio', 'annuity_income_ratio', 'AMT_CREDIT', 'DAYS_EMPLOYED'
]

@st.cache_resource
def load_model():
    try:
        return joblib.load('tunisian_credit_model.pkl')
    except Exception:
        return None

model = load_model()
if model is None:
    st.info("Model file not found — running in demo mode with a rule-based estimator.", icon="ℹ️")

# ── Header ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div>
        <div class="header-title">Credit Risk Assessment</div>
        <div class="header-sub">Internal use only · Banking officer interface</div>
    </div>
    <div class="header-badge">INTERNAL TOOL</div>
    <div class="header-time">{datetime.now().strftime('%d %b %Y · %H:%M')}</div>
</div>
""", unsafe_allow_html=True)

# ── FORM ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="form-card"><div class="section-title">Client Information</div>', unsafe_allow_html=True)
ci1, ci2, ci3 = st.columns(3)
with ci1:
    client_ref = st.text_input("Client reference / ID", value="CLT-2024-0047")
with ci2:
    contract_type = st.selectbox("Contract type", ["Cash loan", "Revolving loan"])
with ci3:
    officer = st.text_input("Officer name", placeholder="Optional")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="section-title">Financial Data</div>', unsafe_allow_html=True)
cf1, cf2, cf3, cf4 = st.columns(4)
with cf1:
    income = st.number_input("Monthly net income (TND)", min_value=1, value=2800, step=100)
with cf2:
    amt_credit = st.number_input("Credit amount (TND)", min_value=1, value=25000, step=1000)
with cf3:
    annuity = st.number_input("Monthly installment (TND)", min_value=1, value=520, step=50)
with cf4:
    years_employed = st.number_input("Years employed", min_value=0.0, value=5.0, step=0.5)

cf5, cf6, cf7 = st.columns(3)
with cf5:
    overdue = st.number_input("BCT overdue days", min_value=0, value=0)
with cf6:
    saving_pct = st.number_input("Savings rate (% of income)", min_value=0, max_value=100, value=10)
with cf7:
    stability = st.slider("Employment stability score", 0, 100, 70)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="form-card"><div class="section-title">External Bureau Scores</div>', unsafe_allow_html=True)
cb1, cb2, cb3 = st.columns(3)
with cb1:
    ext_1 = st.slider("Score BCT (Centrale des Risques)", 0.0, 1.0, 0.72, step=0.01)

with cb2:
    ext_2 = st.slider("Score Comportemental (Digital)", 0.0, 1.0, 0.65, step=0.01)

with cb3:
    ext_3 = st.slider("Score Bureaux Externes", 0.0, 1.0, 0.58, step=0.01)
st.markdown('</div>', unsafe_allow_html=True)

run_btn = st.button("Analyse credit risk", use_container_width=True)

# ── Results ──────────────────────────────────────────────────────────────────────
if run_btn:
    # All safe computed values
    income_safe  = max(income, 1)
    credit_safe  = max(amt_credit, 1)
    days_employed = -int(years_employed * 365)  # always negative (convention)
    saving_rate  = saving_pct / 100.0
    debt_r       = (annuity + 200) / income_safe
    cr_ratio     = amt_credit / income_safe
    ann_ratio    = annuity / income_safe
    dti          = annuity / income_safe
    avg_ext      = (ext_1 + ext_2 + ext_3) / 3
    lgd_est      = 0.45

    input_dict = {
        'debt_ratio':         debt_r,
        'saving_rate':        saving_rate,
        'stability_points':   stability,
        'CREDIT_DAY_OVERDUE': overdue,
        'NAME_CONTRACT_STATUS': 1 if contract_type == "Cash loan" else 0,
        'EXT_SOURCE_1':       ext_1,
        'EXT_SOURCE_2':       ext_2,
        'EXT_SOURCE_3':       ext_3,
        'credit_income_ratio':  cr_ratio,
        'annuity_income_ratio': ann_ratio,
        'AMT_CREDIT':         float(amt_credit),
        'DAYS_EMPLOYED':      float(days_employed),
    }
    input_df = pd.DataFrame([input_dict])[FEATURE_COLUMNS]

    if model:
        risk_proba = float(model.predict_proba(input_df)[0, 1])
    else:
        # Demo: calibrated rule-based estimate (all clamped, no division by zero)
        risk_proba = (
            0.72
            - avg_ext * 0.55
            + max(debt_r - 0.35, 0) * 0.25
            + min(overdue, 365) * 0.004
            - saving_rate * 0.12
            - min(years_employed, 20) * 0.01
        )
        risk_proba = max(0.02, min(0.97, risk_proba))

    score  = round((1 - risk_proba) * 100, 1)
    el_val = risk_proba * amt_credit * lgd_est

    # Decision
    if score >= 80:
        banner_cls, verdict = "banner-approve", "Approve credit"
        verdict_color, label_color = "#15803d", "#15803d"
        guidance = "All risk indicators within acceptable thresholds. Proceed with standard documentation."
    elif score >= 60:
        banner_cls, verdict = "banner-review", "Manual review required"
        verdict_color, label_color = "#b45309", "#b45309"
        guidance = "Borderline profile. Escalate to senior credit officer before issuing a final decision."
    else:
        banner_cls, verdict = "banner-decline", "Decline application"
        verdict_color, label_color = "#b91c1c", "#b91c1c"
        guidance = "Risk threshold exceeded. Profile does not meet minimum creditworthiness criteria."

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Row 1: Decision · Gauge · KPIs
    col_d, col_g, col_k = st.columns([1.4, 1, 1.1])

    with col_d:
        st.markdown(f"""
        <div class="banner {banner_cls}">
            <div class="banner-label" style="color:{label_color}">Recommendation · {client_ref}</div>
            <div class="banner-verdict" style="color:{verdict_color}">{verdict}</div>
            <div class="banner-score">Creditability score: {score} / 100</div>
            <div class="banner-note">{guidance}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_g:
        gauge_color = "#16a34a" if score >= 80 else ("#d97706" if score >= 60 else "#dc2626")
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={'font': {'size': 30, 'color': gauge_color, 'family': 'Inter'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 0,
                         'tickfont': {'color': '#9ca3af', 'size': 9}},
                'bar': {'color': gauge_color, 'thickness': 0.22},
                'bgcolor': '#f3f4f6', 'borderwidth': 0,
                'steps': [
                    {'range': [0, 60],  'color': '#fee2e2'},
                    {'range': [60, 80], 'color': '#fef9c3'},
                    {'range': [80, 100],'color': '#dcfce7'},
                ],
                'threshold': {'line': {'color': gauge_color, 'width': 2},
                              'thickness': 0.7, 'value': score}
            }
        ))
        fig_g.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=185, margin=dict(t=20, b=5, l=15, r=15),
            font={'color': '#374151', 'family': 'Inter'}
        )
        st.plotly_chart(fig_g, use_container_width=True, config={'displayModeBar': False})
        st.markdown("<div style='text-align:center;font-size:0.65rem;color:#9ca3af;letter-spacing:1.5px;margin-top:-0.4rem'>CREDITABILITY INDEX</div>", unsafe_allow_html=True)

    with col_k:
        pd_color  = "#dc2626" if risk_proba > 0.4 else "#16a34a"
        dti_color = "#dc2626" if dti > 0.5 else "#16a34a"
        st.markdown(f"""
        <div class="kpi-chip">
            <div class="kpi-label">Probability of default</div>
            <div class="kpi-value" style="color:{pd_color}">{risk_proba:.1%}</div>
            <div class="kpi-sub">Likelihood of non-repayment</div>
        </div>
        <div class="kpi-chip">
            <div class="kpi-label">Expected loss</div>
            <div class="kpi-value" style="color:#d97706">{el_val:,.0f} TND</div>
            <div class="kpi-sub">PD × EAD × LGD (45%)</div>
        </div>
        <div class="kpi-chip">
            <div class="kpi-label">Debt-to-income ratio</div>
            <div class="kpi-value" style="color:{dti_color}">{dti:.1%}</div>
            <div class="kpi-sub">Monthly burden on income</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Row 2: Factor chart · Metrics table
    col_chart, col_table = st.columns([1.3, 1])

    with col_chart:
        st.markdown('<div class="section-title">Risk factor contributions</div>', unsafe_allow_html=True)

        # All impacts clamped to [-0.5, +0.5], no unbounded values
        f_bureau   = max(-0.5, min(0.5, avg_ext - 0.5))
        f_income   = max(-0.5, min(0.5, (income / credit_safe) - 0.15))
        f_employ   = max(-0.5, min(0.5, years_employed / 10 - 0.1))
        f_overdue  = max(-0.5, min(0.0, -(overdue / 60)))
        f_debt     = max(-0.5, min(0.5, 0.35 - debt_r))
        f_stability= max(-0.5, min(0.5, (stability - 50) / 100))

        df_factors = pd.DataFrame({
            'Factor': ['Bureau scores', 'Income/credit ratio', 'Employment duration',
                       'Overdue record', 'Debt burden', 'Stability score'],
            'Impact': [f_bureau, f_income, f_employ, f_overdue, f_debt, f_stability]
        }).sort_values('Impact')

        bar_colors = ['#16a34a' if v >= 0 else '#dc2626' for v in df_factors['Impact']]
        fig_b = go.Figure(go.Bar(
            x=df_factors['Impact'], y=df_factors['Factor'], orientation='h',
            marker=dict(color=bar_colors, opacity=0.8, line=dict(width=0)),
            text=[f"{'+' if v >= 0 else ''}{v:.2f}" for v in df_factors['Impact']],
            textposition='outside',
            textfont=dict(family='Inter', size=10, color='#6b7280')
        ))
        fig_b.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', zeroline=True,
                       zerolinecolor='#d1d5db', tickfont=dict(color='#9ca3af', size=9)),
            yaxis=dict(showgrid=False, tickfont=dict(family='Inter', color='#374151', size=11)),
            height=260, margin=dict(t=5, b=5, l=10, r=55), showlegend=False
        )
        st.plotly_chart(fig_b, use_container_width=True, config={'displayModeBar': False})

    with col_table:
        st.markdown('<div class="section-title">Detailed risk metrics</div>', unsafe_allow_html=True)
        rows = [
            ("Exposure at default (EAD)", f"{amt_credit:,} TND"),
            ("Loss given default (LGD)",  f"{lgd_est:.0%}"),
            ("Expected loss (EL)",         f"{el_val:,.0f} TND"),
            ("Credit / income ratio",      f"{cr_ratio:.2f}×"),
            ("Annuity / income ratio",     f"{ann_ratio:.1%}"),
            ("Employment duration",        f"{years_employed:.1f} yrs"),
            ("BCT overdue days",           f"{overdue} days"),
            ("Average bureau score",       f"{avg_ext:.3f}"),
            ("Savings rate",               f"{saving_pct}%"),
        ]
        tbl = '<table class="mtable"><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>'
        for lbl, val in rows:
            tbl += f'<tr><td>{lbl}</td><td>{val}</td></tr>'
        tbl += '</tbody></table>'
        st.markdown(tbl, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Analyst notes
    st.markdown('<div class="section-title">Analyst notes</div>', unsafe_allow_html=True)
    notes = []
    if avg_ext >= 0.65:
        notes.append(("Bureau profile — strong",
                       f"Average bureau score of {avg_ext:.3f} indicates solid repayment history across reporting agencies."))
    elif avg_ext >= 0.45:
        notes.append(("Bureau profile — moderate",
                       f"Bureau average of {avg_ext:.3f} is borderline. Obtain any missing scores before a final decision."))
    else:
        notes.append(("Bureau profile — weak",
                       f"Low bureau average ({avg_ext:.3f}) significantly elevates risk. Collateral or guarantor strongly recommended."))

    if dti > 0.5:
        notes.append(("High debt burden",
                       f"DTI of {dti:.1%} exceeds the 50% threshold. Monthly obligations may impair repayment capacity."))
    else:
        notes.append(("Manageable debt burden",
                       f"DTI of {dti:.1%} is within the acceptable range, indicating adequate disposable income."))

    if overdue > 0:
        notes.append(("BCT overdue flag",
                       f"{overdue} overdue days found in the central registry. Request a written explanation before proceeding."))

    if saving_pct < 5:
        notes.append(("Low savings rate",
                       f"Declared savings rate of {saving_pct}% is below the recommended minimum. Verify income stability independently."))

    note_cols = st.columns(max(len(notes), 1))
    for i, (title, body) in enumerate(notes):
        with note_cols[i]:
            st.markdown(f"""
            <div class="note-card">
                <div class="note-title">{title}</div>
                <div class="note-body">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-note">
        <strong>Model guidance:</strong> External bureau scores are the primary predictive drivers.
        When scores are absent or flagged, rely on manual review by a senior credit officer.
        Expected loss uses a standard LGD of 45% (Basel III). This tool supports — but does not replace — banker judgment.
    </div>""", unsafe_allow_html=True)
