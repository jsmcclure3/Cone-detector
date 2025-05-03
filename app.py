import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Cone Detector: Theta–Gamma Coupling Visualizer")

st.write("""
This app simulates a theta (6 Hz) wave and a gamma (40 Hz) burst that is nested in the positive phase of the theta cycle. 
This is used as a proxy for categorical 'cone' structures in neural data.
""")

# Parameters
theta_freq = st.slider("Theta Frequency (Hz)", 4, 8, 6)
gamma_freq = st.slider("Gamma Frequency (Hz)", 30, 80, 40)
modulation_strength = st.slider("Modulation Strength", 0.0, 1.0, 0.5)

# Simulate signals
fs = 1000
t = np.arange(0, 2.0, 1/fs)
theta = np.sin(2 * np.pi * theta_freq * t)
gamma = (np.sin(2 * np.pi * gamma_freq * t) * (theta > 0)) * (1 + modulation_strength * theta)
signal = theta + gamma

# Plot
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(t, signal, label="Composite Signal", color='black')
ax.plot(t, theta, label="Theta", alpha=0.5)
ax.plot(t, gamma, label="Gamma (nested)", alpha=0.5)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()
st.pyplot(fig)

st.write("Use the sliders to explore how frequency and modulation affect coupling.")
