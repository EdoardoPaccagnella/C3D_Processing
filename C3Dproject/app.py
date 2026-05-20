import streamlit as st
from c3d_converter import process_c3d
from report import create_report, create_knee_plots

st.title("C3D Processor")

# Upload the binary C3D file via the web interface
file = st.file_uploader("Upload C3D", type=["c3d"])

if file:
    with open("temp.c3d", "wb") as f:
        f.write(file.read())

    if st.button("Process"):
        # Extract biomechanical data (angles, moments, powers) from the C3D file
        angles, moments, powers = process_c3d("temp.c3d", "output/")

        # Display data labels (e.g., "KneeAngle") to verify successful extraction
        st.write("Angles labels:", [d["label"] for d in angles["data"]])

        # Generate a specific visualization for knee kinematics
        img = create_knee_plots(angles)

        # Compile the generated plot into a final report document
        create_report(img)

        st.success("Processing complete!")
