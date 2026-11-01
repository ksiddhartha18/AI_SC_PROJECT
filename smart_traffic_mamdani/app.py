import streamlit as st
import pandas as pd
from mamdani import calculate_green_duration
from visualizations import membership_figure, output_figure, response_surface_figure

st.set_page_config(page_title="Smart Traffic Light Controller", page_icon="🚦", layout="wide")
st.title("🚦 Smart Traffic Light Control System")
st.caption("Adaptive green-light duration using a Mamdani Fuzzy Inference System")

with st.sidebar:
    st.header("Traffic conditions")
    scenario = st.selectbox("Sample scenario", [
        "Custom", "Light traffic · short wait", "Moderate traffic · medium wait",
        "Heavy traffic · long wait", "Heavy traffic · short wait", "Light traffic · long wait"
    ])
    samples = {
        "Custom": (10,30), "Light traffic · short wait": (3,10),
        "Moderate traffic · medium wait": (15,60), "Heavy traffic · long wait": (28,110),
        "Heavy traffic · short wait": (27,15), "Light traffic · long wait": (4,110)
    }
    d_traffic, d_wait = samples[scenario]
    traffic_count = st.slider("Vehicles waiting",0,30,d_traffic)
    waiting_time = st.slider("Waiting time (seconds)",0,120,d_wait)

result = calculate_green_duration(traffic_count,waiting_time)
a,b,c = st.columns(3)
a.metric("Green-light duration",f"{result['green_duration']:.2f} sec")
b.metric("Duration category",result["category"])
c.metric("Rules fired",str(len(result["fired_rules"])))
st.success(f"The model recommends a green phase of {result['green_duration']:.2f} seconds for these simulated conditions.")

left,right = st.columns(2)
with left:
    st.subheader("Input membership degrees")
    rows = [{"Input":"Traffic density","Fuzzy set":k,"Membership degree":round(v,3)} for k,v in result["traffic_memberships"].items()]
    rows += [{"Input":"Waiting time","Fuzzy set":k,"Membership degree":round(v,3)} for k,v in result["waiting_memberships"].items()]
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
with right:
    st.subheader("Signal decision")
    st.write(f"**Vehicles waiting:** {traffic_count}")
    st.write(f"**Waiting time:** {waiting_time} seconds")
    st.write(f"**Suggested green phase:** {result['green_duration']:.2f} seconds")
    st.caption("Only the simulated green phase is modeled. Yellow/all-red intervals are outside this project's scope.")

st.subheader("Fired fuzzy rules")
st.dataframe(pd.DataFrame(result["fired_rules"]),use_container_width=True,hide_index=True)
st.subheader("Membership functions")
st.pyplot(membership_figure(),use_container_width=True)
st.subheader("Aggregated output and centroid")
st.pyplot(output_figure(result),use_container_width=True)
with st.expander("View response surface"):
    st.pyplot(response_surface_figure(),use_container_width=True)
with st.expander("Assumptions and safety limitations"):
    st.markdown("""
    - Educational simulation only; no live sensors or physical traffic lights.
    - Inputs and membership functions are illustrative.
    - Models one traffic approach and does not coordinate an intersection.
    - Pedestrian phases, emergency priority, yellow/all-red interlocks and fail-safe controls are not implemented.
    - Real-world use requires traffic-engineering validation and regulatory approval.
    """)
st.caption("Academic mini-project · Mamdani FIS · Python + Streamlit")
