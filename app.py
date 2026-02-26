import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Smart Home Dialysis Simulator", layout="wide")
st.title("💉 Smart Home Dialysis Simulation Engine")

# -----------------------------
# Patient Profiles
patients = {
    "Elderly Patient": {"blood_pressure": 110, "flow_speed": 4, "uf_rate": 180},
    "Cardiac Patient": {"blood_pressure": 140, "flow_speed": 5, "uf_rate": 250},
    "Diabetic Patient": {"blood_pressure": 130, "flow_speed": 5, "uf_rate": 200},
    "High Fluid Overload": {"blood_pressure": 150, "flow_speed": 6, "uf_rate": 400}
}

# اختيار المريض
selected_patient = st.selectbox("Select Patient Profile", list(patients.keys()))
scenario = patients[selected_patient]

num_pipes = 4
num_points = 10
pipe_length = 100

# -----------------------------
# مؤقت الحركة
if 't' not in st.session_state:
    st.session_state.t = 0

# Placeholder للرسم
placeholder = st.empty()

# مؤقت ديناميكي
if 'running' not in st.session_state:
    st.session_state.running = True

col1, col2, col3 = st.columns(3)
if col1.button("▶️ Start"):
    st.session_state.running = True
if col2.button("⏸ Stop"):
    st.session_state.running = False
if col3.button("🔄 Reset"):
    st.session_state.t = 0

# -----------------------------
# تحليل حالة المريض وإظهار Alert
bp = scenario["blood_pressure"]
uf = scenario["uf_rate"]
flow = scenario["flow_speed"]

risk = "Stable 🟢"
if bp < 100:
    risk = "Low BP 🔴"
elif bp > 150:
    risk = "High BP 🔴"
elif uf > 350:
    risk = "High UF 🟡"

st.markdown(f"**Patient Risk Status:** {risk}")

# -----------------------------
# المحاكاة
if st.session_state.running:
    fig = go.Figure()

    for i in range(num_pipes):
        y = i * 5
        # رسم الأنبوب
        fig.add_trace(go.Scatter(
            x=[0, pipe_length], y=[y, y],
            mode='lines', line=dict(color='black', width=12),
            showlegend=False
        ))

        # حركة الدم (نقاط حمراء)
        positions = [(p + st.session_state.t * flow) % pipe_length for p in range(0, pipe_length, pipe_length // num_points)]
        fig.add_trace(go.Scatter(
            x=positions, y=[y]*len(positions),
            mode='markers', marker=dict(color='red', size=15),
            showlegend=False
        ))

        # المضخة على أول أنبوب
        if i == 0:
            fig.add_trace(go.Scatter(
                x=[5], y=[y],
                mode='markers+text',
                marker=dict(color='blue', size=25),
                text=["Pump"], textposition="top center",
                showlegend=False
            ))

    # -----------------------------
    vitals_text = f"BP: {bp} mmHg | UF rate: {uf} mL | Flow: {flow}"
    st.markdown(f"**Current Vitals:** {vitals_text}")

    fig.update_layout(
        xaxis=dict(range=[0, pipe_length], visible=False),
        yaxis=dict(range=[-5, num_pipes*5], visible=False),
        height=250
    )

    placeholder.plotly_chart(fig, use_container_width=True)
    st.session_state.t += 1