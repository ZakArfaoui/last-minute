# import streamlit as st
# import pandas as pd
# import joblib
# from datetime import datetime

# # ── Page config ──────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Credit Eligibility Check",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # ── CSS ──────────────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

# html, body, [class*="css"] {
#     font-family: 'Inter', sans-serif !important;
#     background: #f8f9fb !important;
#     color: #111827 !important;
# }
# .stApp { background: #f8f9fb !important; }
# #MainMenu, footer, header { visibility: hidden; }
# [data-testid="stSidebar"] { display: none; }
# .block-container { padding: 2.5rem 1rem; max-width: 700px; margin: 0 auto; }

# /* Hero */
# .hero {
#     text-align: center;
#     background: #fff;
#     border: 1px solid #e5e7eb;
#     border-radius: 12px;
#     padding: 2.5rem 2rem 2rem;
#     margin-bottom: 1.5rem;
# }
# .hero-badge {
#     display: inline-block;
#     font-size: 0.72rem; font-weight: 600;
#     background: #f0fdf4; color: #15803d;
#     border: 1px solid #86efac; border-radius: 20px;
#     padding: 4px 14px; margin-bottom: 1rem; letter-spacing: 0.4px;
# }
# .hero-title { font-size: 1.75rem; font-weight: 700; color: #111827; line-height: 1.25; margin-bottom: 0.6rem; }
# .hero-sub { font-size: 0.9rem; color: #6b7280; line-height: 1.65; max-width: 420px; margin: 0 auto; }

# /* Trust row */
# .trust-row {
#     display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;
#     background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
#     padding: 0.85rem 1rem; margin-bottom: 1.5rem;
# }
# .trust-item { font-size: 0.78rem; color: #6b7280; font-weight: 500; }

# /* Section card */
# .section-card {
#     background: #fff; border: 1px solid #e5e7eb;
#     border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1.2rem;
# }
# .section-title {
#     font-size: 0.68rem; font-weight: 600;
#     text-transform: uppercase; letter-spacing: 1.5px; color: #6b7280;
#     margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e5e7eb;
# }

# /* Inputs */
# .stNumberInput input, .stTextInput input {
#     background: #f9fafb !important; border: 1px solid #d1d5db !important;
#     border-radius: 6px !important; color: #111827 !important; font-size: 0.875rem !important;
# }
# .stSelectbox > div > div {
#     background: #f9fafb !important; border: 1px solid #d1d5db !important;
#     border-radius: 6px !important; color: #111827 !important;
# }
# label { color: #374151 !important; font-size: 0.82rem !important; font-weight: 500 !important; }
# .stSlider > div > div > div { background: #e5e7eb !important; }
# .stSlider > div > div > div > div { background: #16a34a !important; }

# /* Button */
# .stButton > button {
#     background: #16a34a !important; color: #fff !important; border: none !important;
#     border-radius: 8px !important; font-weight: 600 !important;
#     font-size: 0.95rem !important; padding: 0.75rem 1rem !important;
# }
# .stButton > button:hover { background: #15803d !important; }

# /* Result cards */
# .result-card { border-radius: 10px; padding: 1.5rem; text-align: center; margin-bottom: 1.25rem; }
# .result-eligible { background: #f0fdf4; border: 1px solid #86efac; border-top: 4px solid #16a34a; }
# .result-maybe    { background: #fffbeb; border: 1px solid #fcd34d; border-top: 4px solid #d97706; }
# .result-unlikely { background: #fef2f2; border: 1px solid #fca5a5; border-top: 4px solid #dc2626; }

# .result-icon  { font-size: 2.5rem; margin-bottom: 0.5rem; }
# .result-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem; }
# .result-body  { font-size: 0.85rem; color: #4b5563; line-height: 1.6; max-width: 380px; margin: 0 auto; }

# /* Score bar */
# .score-bar-wrap { margin: 1.25rem 0; }
# .score-bar-top {
#     display: flex; justify-content: space-between;
#     font-size: 0.78rem; color: #6b7280; margin-bottom: 6px;
# }
# .score-bar-track {
#     background: #e5e7eb; border-radius: 6px; height: 10px; overflow: hidden;
# }
# .score-bar-fill { height: 100%; border-radius: 6px; transition: width 0.6s ease; }
# .score-bar-labels {
#     display: flex; justify-content: space-between;
#     font-size: 0.65rem; color: #9ca3af; margin-top: 5px;
# }

# /* Breakdown table */
# .btable { width: 100%; border-collapse: collapse; font-size: 0.82rem; background: #fff; border-radius: 10px; overflow: hidden; border: 1px solid #e5e7eb; }
# .btable th {
#     background: #f3f4f6; color: #6b7280; font-size: 0.68rem; font-weight: 600;
#     letter-spacing: 1px; text-transform: uppercase; padding: 0.6rem 1rem;
#     text-align: left; border-bottom: 1px solid #e5e7eb;
# }
# .btable td { padding: 0.65rem 1rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
# .btable tr:last-child td { border-bottom: none; }

# .pill {
#     display: inline-block; font-size: 0.7rem; font-weight: 600;
#     padding: 2px 10px; border-radius: 20px;
# }
# .pill-good { background: #f0fdf4; color: #15803d; border: 1px solid #86efac; }
# .pill-mid  { background: #fffbeb; color: #b45309; border: 1px solid #fcd34d; }
# .pill-bad  { background: #fef2f2; color: #b91c1c; border: 1px solid #fca5a5; }

# /* Tip card */
# .tip-card {
#     background: #fff; border: 1px solid #e5e7eb; border-left: 3px solid #2563eb;
#     border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.7rem;
# }
# .tip-title { font-size: 0.82rem; font-weight: 600; color: #1e40af; margin-bottom: 4px; }
# .tip-body  { font-size: 0.8rem; color: #4b5563; line-height: 1.55; }

# /* CTA */
# .cta-box {
#     background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px;
#     padding: 1.25rem 1.5rem; text-align: center; margin-top: 1.25rem;
# }
# .cta-title { font-size: 0.95rem; font-weight: 600; color: #15803d; margin-bottom: 0.4rem; }
# .cta-body  { font-size: 0.8rem; color: #4b5563; line-height: 1.6; margin-bottom: 0.75rem; }
# .cta-contacts { font-size: 0.78rem; color: #6b7280; }

# /* Footer */
# .portal-footer {
#     text-align: center; margin-top: 2rem;
#     font-size: 0.72rem; color: #9ca3af; line-height: 1.8;
# }
# </style>
# """, unsafe_allow_html=True)

# # ── Model ────────────────────────────────────────────────────────────────────────
# FEATURE_COLUMNS = [
#     'debt_ratio', 'saving_rate', 'stability_points', 'CREDIT_DAY_OVERDUE',
#     'NAME_CONTRACT_STATUS', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
#     'credit_income_ratio', 'annuity_income_ratio', 'AMT_CREDIT', 'DAYS_EMPLOYED'
# ]

# @st.cache_resource
# def load_model():
#     try:
#         return joblib.load('tunisian_credit_model.pkl')
#     except Exception:
#         return None

# model = load_model()

# # ── Hero ─────────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="hero">
#     <div class="hero-badge">Banque Nationale · Digital Services</div>
#     <div class="hero-title">Can you get a credit?</div>
#     <div class="hero-sub">
#         Answer a few simple questions to instantly check your eligibility.
#         Takes less than 2 minutes. No impact on your credit score.
#     </div>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div class="trust-row">
#     <span class="trust-item">🔒 100% Confidential</span>
#     <span class="trust-item">⚡ Instant result</span>
#     <span class="trust-item">📊 No credit check</span>
#     <span class="trust-item">🆓 Free & no obligation</span>
# </div>
# """, unsafe_allow_html=True)

# # ── Form ─────────────────────────────────────────────────────────────────────────
# st.markdown('<div class="section-card"><div class="section-title">Your finances</div>', unsafe_allow_html=True)
# fc1, fc2 = st.columns(2)
# with fc1:
#     income = st.number_input("Monthly income after tax (TND)", min_value=1, value=2500, step=100)
# with fc2:
#     amt_credit = st.number_input("How much credit do you need? (TND)", min_value=1000, value=20000, step=1000)
# fc3, fc4 = st.columns(2)
# with fc3:
#     annuity = st.number_input("Monthly payment you can afford (TND)", min_value=50, value=450, step=50)
# with fc4:
#     years_employed = st.number_input("Years at your current job", min_value=0.0, value=3.0, step=0.5)
# st.markdown('</div>', unsafe_allow_html=True)

# st.markdown('<div class="section-card"><div class="section-title">Credit history</div>', unsafe_allow_html=True)
# fh1, fh2 = st.columns(2)
# with fh1:
#     overdue = st.number_input("Overdue days on any loan (BCT)", min_value=0, value=0,
#                                help="Enter 0 if you have no overdue payments")
# with fh2:
#     credit_history = st.selectbox("Credit history", [
#         "Good — always paid on time",
#         "Mixed — some late payments",
#         "None — first credit"
#     ])
# st.markdown('</div>', unsafe_allow_html=True)

# st.markdown('<div class="section-card"><div class="section-title">About you</div>', unsafe_allow_html=True)
# fa1, fa2 = st.columns(2)
# with fa1:
#     savings_habit = st.selectbox("Do you save money regularly?", [
#         "Yes — every month",
#         "Sometimes",
#         "Rarely or never"
#     ])
# with fa2:
#     employment_type = st.selectbox("Employment type", [
#         "Permanent contract (CDI)",
#         "Fixed-term contract (CDD)",
#         "Self-employed",
#         "Civil servant"
#     ])
# st.markdown('</div>', unsafe_allow_html=True)

# check_btn = st.button("Check my eligibility", use_container_width=True)

# # ── Results ──────────────────────────────────────────────────────────────────────
# if check_btn:
#     # ── Map plain answers to model inputs (all clamped, no division by zero)
#     income_safe  = max(income, 1)
#     credit_safe  = max(amt_credit, 1)
#     days_employed = -int(years_employed * 365)  # always negative

#     # Bureau score proxy from credit history
#     ext_base_map = {
#         "Good — always paid on time": 0.73,
#         "Mixed — some late payments": 0.46,
#         "None — first credit":        0.50,
#     }
#     ext_base = ext_base_map[credit_history]

#     # Small adjustments — clamped to [0, 1]
#     stability_bonus = min(years_employed / 40, 0.15)
#     ext_1 = max(0.0, min(1.0, ext_base + stability_bonus))
#     ext_2 = ext_base                                        # BCT — no adjustment
#     ext_3 = max(0.0, min(1.0, ext_base + stability_bonus * 0.5))
#     avg_ext = (ext_1 + ext_2 + ext_3) / 3

#     # Savings rate
#     saving_rate_map = {
#         "Yes — every month":  0.18,
#         "Sometimes":          0.08,
#         "Rarely or never":    0.02,
#     }
#     saving_rate = saving_rate_map[savings_habit]

#     # Stability score (0–100)
#     stability = 50
#     if employment_type in ("Permanent contract (CDI)", "Civil servant"):
#         stability = min(100, stability + 20)
#     elif employment_type == "Fixed-term contract (CDD)":
#         stability = min(100, stability + 5)
#     stability = min(100, stability + int(min(years_employed, 20) * 1.5))

#     debt_r    = (annuity + 200) / income_safe
#     cr_ratio  = amt_credit / income_safe
#     ann_ratio = annuity / income_safe
#     dti       = annuity / income_safe
#     lgd_est   = 0.45

#     input_dict = {
#         'debt_ratio':           debt_r,
#         'saving_rate':          saving_rate,
#         'stability_points':     stability,
#         'CREDIT_DAY_OVERDUE':   overdue,
#         'NAME_CONTRACT_STATUS': 1,
#         'EXT_SOURCE_1':         ext_1,
#         'EXT_SOURCE_2':         ext_2,
#         'EXT_SOURCE_3':         ext_3,
#         'credit_income_ratio':  cr_ratio,
#         'annuity_income_ratio': ann_ratio,
#         'AMT_CREDIT':           float(amt_credit),
#         'DAYS_EMPLOYED':        float(days_employed),
#     }
#     input_df = pd.DataFrame([input_dict])[FEATURE_COLUMNS]

#     if model:
#         risk_proba = float(model.predict_proba(input_df)[0, 1])
#     else:
#         # Demo: calibrated, fully clamped
#         risk_proba = (
#             0.72
#             - avg_ext * 0.55
#             + max(debt_r - 0.35, 0) * 0.25
#             + min(overdue, 365) * 0.004
#             - saving_rate * 0.12
#             - min(years_employed, 20) * 0.01
#         )
#         risk_proba = max(0.02, min(0.97, risk_proba))

#     score = round((1 - risk_proba) * 100, 1)

#     # ── Result card
#     if score >= 80:
#         r_cls, r_icon, r_title = "result-eligible", "✅", "You're likely eligible!"
#         r_title_color = "#15803d"
#         r_body = "Your profile looks strong. You have a good chance of getting approved. We recommend visiting your nearest branch to start the official application."
#         bar_color = "#16a34a"
#     elif score >= 58:
#         r_cls, r_icon, r_title = "result-maybe", "🤔", "You might be eligible — let's talk."
#         r_title_color = "#b45309"
#         r_body = "Your profile has some positive signals but also some areas that could be improved. A banker can review your full file and suggest options."
#         bar_color = "#d97706"
#     else:
#         r_cls, r_icon, r_title = "result-unlikely", "😔", "Not eligible right now — but that can change."
#         r_title_color = "#b91c1c"
#         r_body = "Your current profile doesn't meet the standard criteria. The tips below can help you improve your score over the next few months."
#         bar_color = "#dc2626"

#     st.markdown(f"""
#     <div class="result-card {r_cls}">
#         <div class="result-icon">{r_icon}</div>
#         <div class="result-title" style="color:{r_title_color}">{r_title}</div>
#         <div class="result-body">{r_body}</div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Score bar
#     st.markdown(f"""
#     <div class="score-bar-wrap">
#         <div class="score-bar-top">
#             <span>Eligibility score</span>
#             <span style="font-weight:600;color:{bar_color}">{score:.0f} / 100</span>
#         </div>
#         <div class="score-bar-track">
#             <div class="score-bar-fill" style="width:{score}%;background:{bar_color}"></div>
#         </div>
#         <div class="score-bar-labels">
#             <span>0</span><span>Not eligible · 60 · May qualify</span><span>80 · Likely · 100</span>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # ── Breakdown table
#     st.markdown('<div class="section-card"><div class="section-title">What affects your score</div>', unsafe_allow_html=True)

#     def make_pill(good, bad, good_txt="Good", mid_txt="OK", bad_txt="Risk"):
#         if good:
#             return f'<span class="pill pill-good">{good_txt}</span>'
#         elif bad:
#             return f'<span class="pill pill-bad">{bad_txt}</span>'
#         else:
#             return f'<span class="pill pill-mid">{mid_txt}</span>'

#     breakdown = [
#         ("Monthly income",        f"{income:,} TND",
#          make_pill(income >= 2000, income < 800)),
#         ("Credit requested",      f"{amt_credit:,} TND",
#          make_pill(cr_ratio <= 8, cr_ratio > 20, "Reasonable", "High", "Very high")),
#         ("Monthly payment / income", f"{dti:.0%}",
#          make_pill(dti <= 0.35, dti > 0.55, "Healthy", "Moderate", "Too high")),
#         ("Years at current job",  f"{years_employed:.1f} yrs",
#          make_pill(years_employed >= 2, years_employed < 0.5, "Stable", "Recent", "Too short")),
#         ("Overdue days (BCT)",    f"{overdue} days",
#          make_pill(overdue == 0, overdue > 30, "Clear", "Minor", "Flagged")),
#         ("Credit history",        credit_history.split("—")[0].strip(),
#          make_pill("Good" in credit_history, "Mixed" in credit_history, "Positive", "Neutral", "Negative")),
#         ("Savings habit",         savings_habit.split("—")[0].strip(),
#          make_pill("Yes" in savings_habit, "Rarely" in savings_habit, "Good", "Moderate", "Poor")),
#     ]

#     tbl = '<table class="btable"><thead><tr><th>Factor</th><th>Your value</th><th>Status</th></tr></thead><tbody>'
#     for label, val, pill in breakdown:
#         tbl += f'<tr><td>{label}</td><td>{val}</td><td>{pill}</td></tr>'
#     tbl += '</tbody></table>'
#     st.markdown(tbl, unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # ── Tips (only when score < 80)
#     if score < 80:
#         tips = []
#         if dti > 0.4:
#             tips.append(("Reduce your monthly payment",
#                           f"Your payment-to-income ratio is {dti:.0%}. Try requesting a smaller credit amount or a longer repayment period to bring this under 35%."))
#         if overdue > 0:
#             tips.append(("Clear overdue payments",
#                           "Any overdue amount in the BCT registry significantly lowers your score. Settling these before applying makes a big difference."))
#         if "Rarely" in savings_habit:
#             tips.append(("Start saving regularly",
#                           "Even saving 5–10% of your income each month signals financial discipline to lenders and strengthens your application."))
#         if cr_ratio > 12:
#             tips.append(("Consider a smaller credit amount",
#                           f"You're requesting {cr_ratio:.1f}× your monthly income. Lenders prefer ratios below 10×. A smaller first credit is easier to approve."))
#         if years_employed < 1:
#             tips.append(("Build employment stability",
#                           "Less than 1 year at your current job is often seen as a risk factor. Waiting until you have 12+ months in your role can help."))

#         if tips:
#             st.markdown('<div class="section-card"><div class="section-title">How to improve your chances</div>', unsafe_allow_html=True)
#             for t_title, t_body in tips:
#                 st.markdown(f"""
#                 <div class="tip-card">
#                     <div class="tip-title">{t_title}</div>
#                     <div class="tip-body">{t_body}</div>
#                 </div>""", unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#     # ── CTA
#     st.markdown("""
#     <div class="cta-box">
#         <div class="cta-title">Ready to apply in person?</div>
#         <div class="cta-body">
#             Our credit advisors are available Monday to Friday, 9:00 – 17:00.<br>
#             Please bring: last 3 salary slips · National ID (CIN) · Employment contract
#         </div>
#         <div class="cta-contacts">📍 Find your nearest branch &nbsp;·&nbsp; 📞 71 000 000 &nbsp;·&nbsp; 🌐 banque.tn</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ── Footer ───────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="portal-footer">
#     This tool provides an indicative estimate only and does not constitute an offer of credit.<br>
#     Final decisions are made by a qualified banking officer based on your full financial file.<br>
#     © 2024 Banque Nationale · Regulated by the Banque Centrale de Tunisie
# </div>
# """, unsafe_allow_html=True)



import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Eligibility Check",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #f8f9fb !important;
    color: #111827 !important;
}
.stApp { background: #f8f9fb !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 1rem; max-width: 700px; margin: 0 auto; }

/* Hero */
.hero {
    text-align: center;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 2.5rem 2rem 2rem;
    margin-bottom: 1.5rem;
}
.hero-badge {
    display: inline-block;
    font-size: 0.72rem; font-weight: 600;
    background: #f0fdf4; color: #15803d;
    border: 1px solid #86efac; border-radius: 20px;
    padding: 4px 14px; margin-bottom: 1rem; letter-spacing: 0.4px;
}
.hero-title { font-size: 1.75rem; font-weight: 700; color: #111827; line-height: 1.25; margin-bottom: 0.6rem; }
.hero-sub { font-size: 0.9rem; color: #6b7280; line-height: 1.65; max-width: 420px; margin: 0 auto; }

/* Trust row */
.trust-row {
    display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;
    background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 0.85rem 1rem; margin-bottom: 1.5rem;
}
.trust-item { font-size: 0.78rem; color: #6b7280; font-weight: 500; }

/* Section card */
.section-card {
    background: #fff; border: 1px solid #e5e7eb;
    border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1.2rem;
}
.section-title {
    font-size: 0.68rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px; color: #6b7280;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e5e7eb;
}

/* Inputs */
.stNumberInput input, .stTextInput input {
    background: #f9fafb !important; border: 1px solid #d1d5db !important;
    border-radius: 6px !important; color: #111827 !important; font-size: 0.875rem !important;
}
.stSelectbox > div > div {
    background: #f9fafb !important; border: 1px solid #d1d5db !important;
    border-radius: 6px !important; color: #111827 !important;
}
label { color: #374151 !important; font-size: 0.82rem !important; font-weight: 500 !important; }
.stSlider > div > div > div { background: #e5e7eb !important; }
.stSlider > div > div > div > div { background: #16a34a !important; }

/* Button */
.stButton > button {
    background: #16a34a !important; color: #fff !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.95rem !important; padding: 0.75rem 1rem !important;
}
.stButton > button:hover { background: #15803d !important; }

/* Result cards */
.result-card { border-radius: 10px; padding: 1.5rem; text-align: center; margin-bottom: 1.25rem; }
.result-eligible { background: #f0fdf4; border: 1px solid #86efac; border-top: 4px solid #16a34a; }
.result-maybe    { background: #fffbeb; border: 1px solid #fcd34d; border-top: 4px solid #d97706; }
.result-unlikely { background: #fef2f2; border: 1px solid #fca5a5; border-top: 4px solid #dc2626; }

.result-icon  { font-size: 2.5rem; margin-bottom: 0.5rem; }
.result-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem; }
.result-body  { font-size: 0.85rem; color: #4b5563; line-height: 1.6; max-width: 380px; margin: 0 auto; }

/* Score bar */
.score-bar-wrap { margin: 1.25rem 0; }
.score-bar-top {
    display: flex; justify-content: space-between;
    font-size: 0.78rem; color: #6b7280; margin-bottom: 6px;
}
.score-bar-track {
    background: #e5e7eb; border-radius: 6px; height: 10px; overflow: hidden;
}
.score-bar-fill { height: 100%; border-radius: 6px; transition: width 0.6s ease; }
.score-bar-labels {
    display: flex; justify-content: space-between;
    font-size: 0.65rem; color: #9ca3af; margin-top: 5px;
}

/* Debug banner */
.debug-banner {
    background: #fef3c7; border: 1px solid #f59e0b; border-radius: 6px;
    padding: 0.5rem 1rem; margin-bottom: 1rem; font-size: 0.75rem;
}

/* Breakdown table */
.btable { width: 100%; border-collapse: collapse; font-size: 0.82rem; background: #fff; border-radius: 10px; overflow: hidden; border: 1px solid #e5e7eb; }
.btable th {
    background: #f3f4f6; color: #6b7280; font-size: 0.68rem; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase; padding: 0.6rem 1rem;
    text-align: left; border-bottom: 1px solid #e5e7eb;
}
.btable td { padding: 0.65rem 1rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
.btable tr:last-child td { border-bottom: none; }

.pill {
    display: inline-block; font-size: 0.7rem; font-weight: 600;
    padding: 2px 10px; border-radius: 20px;
}
.pill-good { background: #f0fdf4; color: #15803d; border: 1px solid #86efac; }
.pill-mid  { background: #fffbeb; color: #b45309; border: 1px solid #fcd34d; }
.pill-bad  { background: #fef2f2; color: #b91c1c; border: 1px solid #fca5a5; }

/* Tip card */
.tip-card {
    background: #fff; border: 1px solid #e5e7eb; border-left: 3px solid #2563eb;
    border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.7rem;
}
.tip-title { font-size: 0.82rem; font-weight: 600; color: #1e40af; margin-bottom: 4px; }
.tip-body  { font-size: 0.8rem; color: #4b5563; line-height: 1.55; }

/* CTA */
.cta-box {
    background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px;
    padding: 1.25rem 1.5rem; text-align: center; margin-top: 1.25rem;
}
.cta-title { font-size: 0.95rem; font-weight: 600; color: #15803d; margin-bottom: 0.4rem; }
.cta-body  { font-size: 0.8rem; color: #4b5563; line-height: 1.6; margin-bottom: 0.75rem; }
.cta-contacts { font-size: 0.78rem; color: #6b7280; }

/* Footer */
.portal-footer {
    text-align: center; margin-top: 2rem;
    font-size: 0.72rem; color: #9ca3af; line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# ── FEATURE COLUMNS ──────────────────────────────────────────────────────────────
FEATURE_COLUMNS = [
    'debt_ratio', 'saving_rate', 'stability_points', 'CREDIT_DAY_OVERDUE',
    'NAME_CONTRACT_STATUS', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
    'credit_income_ratio', 'annuity_income_ratio', 'AMT_CREDIT', 'DAYS_EMPLOYED'
]

# ── LOAD MODEL (for info only, not used) ────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return joblib.load('tunisian_credit_model.pkl')
    except Exception:
        return None

model = load_model()

# ── SIDEBAR DIAGNOSTICS ─────────────────────────────────────────────────────────
st.sidebar.header("🔍 System Info")
if model:
    st.sidebar.write("ML Model: Loaded (not used)")
    st.sidebar.write(f"Type: {type(model).__name__}")
else:
    st.sidebar.write("ML Model: Not found")
st.sidebar.markdown("---")
st.sidebar.write("**Using:** Rule-based estimator")
st.sidebar.write("**Status:** ✅ Active")

# ── MAIN UI ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Banque Nationale · Digital Services</div>
    <div class="hero-title">Can you get a credit?</div>
    <div class="hero-sub">
        Answer a few simple questions to instantly check your eligibility.
        Takes less than 2 minutes. No impact on your credit score.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="trust-row">
    <span class="trust-item">🔒 100% Confidential</span>
    <span class="trust-item">⚡ Instant result</span>
    <span class="trust-item">📊 No credit check</span>
    <span class="trust-item">🆓 Free & no obligation</span>
</div>
""", unsafe_allow_html=True)

# ── FORM ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">Your finances</div>', unsafe_allow_html=True)
fc1, fc2 = st.columns(2)
with fc1:
    income = st.number_input("Monthly income after tax (TND)", min_value=1, value=2500, step=100)
with fc2:
    amt_credit = st.number_input("How much credit do you need? (TND)", min_value=1000, value=20000, step=1000)
fc3, fc4 = st.columns(2)
with fc3:
    annuity = st.number_input("Monthly payment you can afford (TND)", min_value=50, value=450, step=50)
with fc4:
    years_employed = st.number_input("Years at your current job", min_value=0.0, value=3.0, step=0.5)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card"><div class="section-title">Credit history</div>', unsafe_allow_html=True)
fh1, fh2 = st.columns(2)
with fh1:
    overdue = st.number_input("Overdue days on any loan (BCT)", min_value=0, value=0,
                               help="Enter 0 if you have no overdue payments")
with fh2:
    credit_history = st.selectbox("Credit history", [
        "Good — always paid on time",
        "Mixed — some late payments",
        "None — first credit"
    ])
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card"><div class="section-title">About you</div>', unsafe_allow_html=True)
fa1, fa2 = st.columns(2)
with fa1:
    savings_habit = st.selectbox("Do you save money regularly?", [
        "Yes — every month",
        "Sometimes",
        "Rarely or never"
    ])
with fa2:
    employment_type = st.selectbox("Employment type", [
        "Permanent contract (CDI)",
        "Fixed-term contract (CDD)",
        "Self-employed",
        "Civil servant"
    ])
st.markdown('</div>', unsafe_allow_html=True)

check_btn = st.button("Check my eligibility", use_container_width=True)

# ── RESULTS ─────────────────────────────────────────────────────────────────────
if check_btn:
    # Calculate all features
    income_safe = max(income, 1)
    credit_safe = max(amt_credit, 1)
    days_employed = -int(years_employed * 365)
    
    # Bureau scores from credit history
    ext_base_map = {
        "Good — always paid on time": 0.73,
        "Mixed — some late payments": 0.46,
        "None — first credit": 0.50,
    }
    ext_base = ext_base_map[credit_history]
    
    stability_bonus = min(years_employed / 40, 0.15)
    ext_1 = max(0.0, min(1.0, ext_base + stability_bonus))
    ext_2 = ext_base
    ext_3 = max(0.0, min(1.0, ext_base + stability_bonus * 0.5))
    bureau_avg = (ext_1 + ext_2 + ext_3) / 3
    
    # Savings rate
    saving_rate_map = {
        "Yes — every month": 0.18,
        "Sometimes": 0.08,
        "Rarely or never": 0.02,
    }
    saving_rate = saving_rate_map[savings_habit]
    
    # Stability score
    stability = 50
    if employment_type in ("Permanent contract (CDI)", "Civil servant"):
        stability = min(100, stability + 20)
    elif employment_type == "Fixed-term contract (CDD)":
        stability = min(100, stability + 5)
    stability = min(100, stability + int(min(years_employed, 20) * 1.5))
    
    # Financial ratios
    debt_r = (annuity + 200) / income_safe
    cr_ratio = amt_credit / income_safe
    ann_ratio = annuity / income_safe
    dti = annuity / income_safe
    
    # ── RULE-BASED RISK CALCULATION (ML MODEL BYPASSED) ────────────────────────
    
    # 1. Credit/Income ratio (35% weight) - MOST IMPORTANT
    # 285x income = 0.95 risk, 10x = 0.35 risk, 5x = 0.10 risk
    if cr_ratio <= 5:
        credit_risk = cr_ratio / 5 * 0.10  # 0 to 0.10
    elif cr_ratio <= 10:
        credit_risk = 0.10 + (cr_ratio - 5) / 5 * 0.25  # 0.10 to 0.35
    elif cr_ratio <= 20:
        credit_risk = 0.35 + (cr_ratio - 10) / 10 * 0.30  # 0.35 to 0.65
    elif cr_ratio <= 50:
        credit_risk = 0.65 + (cr_ratio - 20) / 30 * 0.25  # 0.65 to 0.90
    else:
        credit_risk = 0.90 + min((cr_ratio - 50) / 100, 0.05)  # 0.90 to 0.95
    
    # 2. Income level (25% weight) - ABSOLUTE MINIMUM
    # 700 TND = 0.50 risk, 1500 TND = 0 risk
    if income >= 1500:
        income_risk = 0.0
    elif income >= 1000:
        income_risk = (1500 - income) / 500 * 0.25  # 0 to 0.25
    else:
        income_risk = 0.25 + (1000 - income) / 1000 * 0.25  # 0.25 to 0.50
    
    # 3. DTI - Debt to Income ratio (15% weight)
    if dti <= 0.30:
        dti_risk = 0.0
    elif dti <= 0.50:
        dti_risk = (dti - 0.30) / 0.20 * 0.15  # 0 to 0.15
    else:
        dti_risk = 0.15 + min((dti - 0.50) / 0.50, 0.35)  # 0.15 to 0.50
    
    # 4. Bureau/Credit history (10% weight)
    bureau_risk = max(0, 0.60 - bureau_avg) * 0.5  # 0.46 avg = 0.07 risk
    
    # 5. Employment stability (10% weight)
    if years_employed >= 2:
        employ_risk = 0.0
    elif years_employed >= 1:
        employ_risk = (2 - years_employed) / 1 * 0.10  # 0 to 0.10
    else:
        employ_risk = 0.10 + (1 - years_employed) / 1 * 0.15  # 0.10 to 0.25
    
    # 6. Overdue days (5% weight)
    overdue_risk = min(overdue / 100, 0.30) * 0.5  # Max 0.15 at 100 days
    
    # Combine all risks
    risk_proba = (
        credit_risk * 0.35 +
        income_risk * 0.25 +
        dti_risk * 0.15 +
        bureau_risk * 0.10 +
        employ_risk * 0.10 +
        overdue_risk * 0.05
    )
    
    # Clamp to valid range
    risk_proba = max(0.02, min(0.98, risk_proba))
    
    # Calculate final score
    score = round((1 - risk_proba) * 100, 1)
    
    # ── DEBUG INFO IN SIDEBAR ──────────────────────────────────────────────────
    st.sidebar.subheader("📊 Calculation Details")
    st.sidebar.write(f"**Credit/Income:** {cr_ratio:.1f}x → risk {credit_risk:.2f}")
    st.sidebar.write(f"**Income:** {income} TND → risk {income_risk:.2f}")
    st.sidebar.write(f"**DTI:** {dti:.1%} → risk {dti_risk:.2f}")
    st.sidebar.write(f"**Bureau:** {bureau_avg:.2f} → risk {bureau_risk:.2f}")
    st.sidebar.write(f"**Employment:** {years_employed}y → risk {employ_risk:.2f}")
    st.sidebar.write(f"**Overdue:** {overdue}d → risk {overdue_risk:.2f}")
    st.sidebar.write("---")
    st.sidebar.write(f"**Total Risk:** {risk_proba:.3f}")
    st.sidebar.write(f"**Final Score:** {score:.1f}")
    
    # ── RESULT DISPLAY ──────────────────────────────────────────────────────────
    
    # Debug banner
    st.markdown(f"<div class='debug-banner'>Risk: {risk_proba:.3f} | Score: {score:.1f}/100 | Using: Rule-based estimator</div>", unsafe_allow_html=True)
    
    # Result card
    if score >= 80:
        r_cls, r_icon, r_title = "result-eligible", "✅", "You're likely eligible!"
        r_title_color = "#15803d"
        r_body = "Your profile looks strong. You have a good chance of getting approved. We recommend visiting your nearest branch to start the official application."
        bar_color = "#16a34a"
    elif score >= 58:
        r_cls, r_icon, r_title = "result-maybe", "🤔", "You might be eligible — let's talk."
        r_title_color = "#b45309"
        r_body = "Your profile has some positive signals but also some areas that could be improved. A banker can review your full file and suggest options."
        bar_color = "#d97706"
    else:
        r_cls, r_icon, r_title = "result-unlikely", "😔", "Not eligible right now — but that can change."
        r_title_color = "#b91c1c"
        r_body = "Your current profile doesn't meet the standard criteria. The tips below can help you improve your score over the next few months."
        bar_color = "#dc2626"

    st.markdown(f"""
    <div class="result-card {r_cls}">
        <div class="result-icon">{r_icon}</div>
        <div class="result-title" style="color:{r_title_color}">{r_title}</div>
        <div class="result-body">{r_body}</div>
    </div>
    """, unsafe_allow_html=True)

    # Score bar
    st.markdown(f"""
    <div class="score-bar-wrap">
        <div class="score-bar-top">
            <span>Eligibility score</span>
            <span style="font-weight:600;color:{bar_color}">{score:.0f} / 100</span>
        </div>
        <div class="score-bar-track">
            <div class="score-bar-fill" style="width:{score}%;background:{bar_color}"></div>
        </div>
        <div class="score-bar-labels">
            <span>0</span><span>Not eligible · 60 · May qualify</span><span>80 · Likely · 100</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Breakdown table
    st.markdown('<div class="section-card"><div class="section-title">What affects your score</div>', unsafe_allow_html=True)
    
    def make_pill(good, bad, good_txt="Good", mid_txt="OK", bad_txt="Risk"):
        if good: return f'<span class="pill pill-good">{good_txt}</span>'
        elif bad: return f'<span class="pill pill-bad">{bad_txt}</span>'
        else: return f'<span class="pill pill-mid">{mid_txt}</span>'
    
    breakdown = [
        ("Monthly income", f"{income:,} TND", make_pill(income >= 2000, income < 1000)),
        ("Credit requested", f"{amt_credit:,} TND", make_pill(cr_ratio <= 8, cr_ratio > 20, "Reasonable", "High", "Very high")),
        ("Credit/Income ratio", f"{cr_ratio:.1f}×", make_pill(cr_ratio <= 10, cr_ratio > 20, "Good", "Moderate", "Dangerous")),
        ("Monthly payment / income", f"{dti:.0%}", make_pill(dti <= 0.35, dti > 0.55, "Healthy", "Moderate", "Too high")),
        ("Years at current job", f"{years_employed:.1f} yrs", make_pill(years_employed >= 2, years_employed < 0.5, "Stable", "Recent", "Too short")),
        ("Overdue days (BCT)", f"{overdue} days", make_pill(overdue == 0, overdue > 30, "Clear", "Minor", "Flagged")),
        ("Credit history", credit_history.split("—")[0].strip(), make_pill("Good" in credit_history, "Mixed" in credit_history, "Positive", "Neutral", "Negative")),
        ("Savings habit", savings_habit.split("—")[0].strip(), make_pill("Yes" in savings_habit, "Rarely" in savings_habit, "Good", "Moderate", "Poor")),
    ]
    
    tbl = '<table class="btable"><thead><tr><th>Factor</th><th>Your value</th><th>Status</th></tr></thead><tbody>'
    for label, val, pill in breakdown:
        tbl += f'<tr><td>{label}</td><td>{val}</td><td>{pill}</td></tr>'
    tbl += '</tbody></table>'
    st.markdown(tbl, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Tips
    if score < 80:
        tips = []
        if cr_ratio > 10:
            tips.append(("Reduce credit amount", f"You're requesting {cr_ratio:.1f}× your monthly income. Maximum recommended is 10×. Try a smaller amount."))
        if income < 1000:
            tips.append(("Income below minimum", f"Your income of {income} TND is below the 1000 TND minimum threshold for credit approval."))
        if dti > 0.4:
            tips.append(("Reduce monthly payment", f"Your payment-to-income ratio is {dti:.0%}. Try a longer repayment term to reduce monthly burden."))
        if overdue > 0:
            tips.append(("Clear overdue payments", "Any overdue amount in BCT significantly lowers your score. Settle before applying."))
        if "Rarely" in savings_habit:
            tips.append(("Start saving regularly", "Even 5-10% monthly savings signals financial discipline to lenders."))
        if years_employed < 1:
            tips.append(("Build employment stability", "Less than 1 year at current job is seen as high risk. Wait for 12+ months."))
        
        if tips:
            st.markdown('<div class="section-card"><div class="section-title">How to improve your chances</div>', unsafe_allow_html=True)
            for t_title, t_body in tips:
                st.markdown(f'<div class="tip-card"><div class="tip-title">{t_title}</div><div class="tip-body">{t_body}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # CTA
    st.markdown("""
    <div class="cta-box">
        <div class="cta-title">Ready to apply in person?</div>
        <div class="cta-body">
            Our credit advisors are available Monday to Friday, 9:00 – 17:00.<br>
            Please bring: last 3 salary slips · National ID (CIN) · Employment contract
        </div>
        <div class="cta-contacts">📍 Find your nearest branch &nbsp;·&nbsp; 📞 71 000 000 &nbsp;·&nbsp; 🌐 banque.tn</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="portal-footer">
    This tool provides an indicative estimate only and does not constitute an offer of credit.<br>
    Final decisions are made by a qualified banking officer based on your full financial file.<br>
    © 2024 Banque Nationale · Regulated by the Banque Centrale de Tunisie
</div>
""", unsafe_allow_html=True)