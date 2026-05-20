# C3D Processing & Analysis Pipeline

A comprehensive Python-based workflow designed to process biomechanical `.c3d` files and generate visual reports.

##  Project Structure & File Descriptions

*   **`app.py` (Streamlit Interface)**: The entry point of the application. It provides a web-based UI for uploading C3D files, monitoring the extraction process, and triggering the reporting pipeline.
*   **`c3d_converter.py` (Core Logic)**: Handles the parsing of binary C3D data using `ezc3d`. it converts raw point data into structured dictionaries, manages `NaN` values for data integrity, and exports categorized results (Angles, Moments, Powers) into JSON format.
*   **`report.py` (Visualization & DOCX)**: Contains logic to filter specific biomechanical markers (e.g., Knee Angles) and generate time-series plots via `matplotlib`. It also automates the creation of a professional `.docx` report containing the generated visuals.

## Data Outputs

The processing engine generates three specialized JSON files in the `output/` directory:

1.  **`angles.json`**: Joint kinematics measured in degrees (**deg**).
2.  **`moments.json`**: Joint kinetics measured in Newton-meters (**Nm**).
3.  **`powers.json`**: Joint mechanics measured in Watts (**W**).

Each file is structured to include:
*   **Labels**: The specific anatomical marker name.
*   **Time Vector**: Synchronized time for every frame.
*   **XYZ Components**: Safe-float values for each axis, compatible with web-based viewers.

## Workflow

1.  **Upload**: Provide a `.c3d` file through the Streamlit web interface.
2.  **Process**: The system extracts kinematics and kinetics, saving them locally as JSON.
3.  **Visualize**: A plot of Left vs. Right Knee angles is automatically generated.
4.  **Report**: A Word document is compiled with the analysis summary.
