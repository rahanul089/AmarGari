"""
AmarGari - Reusable UI components (thin wrappers over styled HTML blocks).
"""
import streamlit as st


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="margin-bottom: 0.5rem;">
        <h2 style="margin-bottom:0.15rem;">{title}</h2>
        <p style="opacity:0.75; margin-top:0;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def badge(text: str):
    st.markdown(f'<span class="db-badge">● {text}</span>', unsafe_allow_html=True)


def metric_card(label: str, value: str):
    st.markdown(f"""
    <div class="db-metric">
        <div class="db-metric-label">{label}</div>
        <div class="db-metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def stat(value: str, label: str):
    st.markdown(f"""
    <div>
        <div class="db-stat-value">{value}</div>
        <div class="db-stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def vehicle_card(reg_number: str, owner_name: str, vehicle_type: str, valid_till: str):
    st.markdown(f"""
    <div class="vehicle-card">
        <div class="vc-label">Digital Vehicle Card</div>
        <div class="vc-reg">{reg_number}</div>
        <div class="vc-row"><span>Owner</span><span>{owner_name}</span></div>
        <div class="vc-row"><span>Type</span><span>{vehicle_type}</span></div>
        <div class="vc-row"><span>Valid till</span><span>{valid_till}</span></div>
    </div>
    """, unsafe_allow_html=True)
