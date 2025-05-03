import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

st.set_page_config(layout="wide")
st.title("Cone Detector 2.0: Predictive Structure Under Metabolic Constraint")

st.markdown("""
This tool simulates **theta–gamma nesting** and interprets it categorically.
When coherence and metabolic support align, a **cone structure** forms.
If either breaks, the cone **collapses**, modeling the failure of temporal integration.
""")

# ---- USER CONTROLS ----
col1, col2 = st.columns(2)

with col1:
    theta_freq = st.slider("Theta Frequency (Hz)", 3, 8, 6)
    gamma_freq = st.slider("Gamma Frequency (Hz)", 30, 80, 40)
    modulation_strength = st.slider("Modulation Strength", 0.0, 1.0, 0.5)

with col2:
    energy_budget = st.slider("Energy Budget (0 = exhausted, 1 = abundant)", 0.0, 1.0, 0.6)

# ---- SIMULATION ----
fs = 1000
t = np.linspace(0, 2, fs * 2)

theta = np.sin(2 * np.pi * theta_freq * t)
gamma = np.sin(2 * np.pi * gamma_freq * t)

modulated_gamma = gamma * (1 + modulation_strength * theta)
composite = theta + modulated_gamma

# ---- CONE STRUCTURE DETECTION ----
analytic_theta = hilbert(theta)
analytic_gamma = hilbert(modulated_gamma)
theta_phase = np.angle(analytic_theta)
gamma_envelope = np.abs(analytic_gamma)

# Compute gamma amplitude locked to theta phase > 0
cone_active = (theta_phase > 0)
coherence = np.mean(gamma_envelope[cone_active]) - np.mean(gamma_envelope[~cone_active])
coherence = max(0, coherence)  # avoid negatives

# Determine metabolic viability
viable = coherence * modulation_strength < energy_budget

# ---- PLOT ----
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(t, composite, label="Composite Signal", color='black', linewidth=1)
ax.plot(t, modulated_gamma, label="Gamma (nested)", alpha=0.5)
ax.plot(t, theta, label="Theta", alpha=0.3)
ax.set_title("Simulated Signal with Nested Dynamics")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()
st.pyplot(fig)

# ---- FEEDBACK ----
st.markdown("---")
if viable:
    st.success("**Cone structure detected** — nested gamma bursts align with theta phase *and* stay within metabolic bounds.")
    st.markdown("""
    > In category-theoretic terms, the system maintains a **commutative cone**: each signal factors coherently through the apex (theta phase), stabilized by metabolic feasibility.
    """)
else:
    st.error("**Cone collapsed** — coupling exceeds metabolic threshold.")
    st.markdown("""
    > This models a breakdown in **predictive integration**: signals no longer sustain a coherent limit. Subjective continuity may fragment under resource constraints.
    """)

st.markdown("---")
st.caption("Modeled coherence = {:.3f} | Energy threshold = {:.2f}".format(coherence * modulation_strength, energy_budget))
