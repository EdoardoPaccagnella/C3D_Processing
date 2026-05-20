import matplotlib.pyplot as plt
from docx import Document
import os

def create_knee_plots(angles_json):
    # Extract data series from the JSON structure
    data = angles_json.get("data", [])

    l = None
    r = None

    # Specifically locate the Left and Right Knee angle datasets by their labels
    for entry in data:
        if entry["label"] == "LKneeAngles":
            l = entry["values"]
        elif entry["label"] == "RKneeAngles":
            r = entry["values"]

    # Safety check to ensure both datasets exist before plotting
    if not l or not r:
        print("Knee angles not found")
        return []

    # Prepare time (X-axis) shared across all plots
    t = [frame["time"] for frame in l]

    # Prepare X-component angles (Y-axis values for X plot)
    lx = [frame["x"] for frame in l]
    rx = [frame["x"] for frame in r]

    # Prepare Y-component angles (Y-axis values for Y plot)
    ly = [frame["y"] for frame in l]
    ry = [frame["y"] for frame in r]

    # Prepare Z-component angles (Y-axis values for Z plot)
    lz = [frame["z"] for frame in l]
    rz = [frame["z"] for frame in r]

    # Ensure output directory exists before saving plots
    os.makedirs("output", exist_ok=True)

    paths = []

    # Helper function to generate a plot with consistent styling
    def make_plot(left, right, axis_name, filename):
        # Generate the Matplotlib figure with labels, legend, and a grid
        plt.figure()
        plt.plot(t, left, label=f"Left Knee {axis_name}")
        plt.plot(t, right, label=f"Right Knee {axis_name}")
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (deg)")
        plt.title(f"Knee Angles - {axis_name} Axis")
        plt.grid(True)

        # Set dynamic Y-axis limit to ensure the legend doesn't overlap the lines

        ymin = min(min(left), min(right))
        ymax = max(max(left), max(right))
        margin = (ymax - ymin) * 0.2
        plt.ylim(ymin - margin, ymax + margin)
        
        plt.legend(loc="upper right")

        # Export the plot as a PNG file
        path = f"output/{filename}"
        plt.savefig(path)
        plt.close()

        return path

    # Create one plot per axis (X, Y, Z), combining left and right knees
    paths.append(make_plot(lx, rx, "X", "knee_plot_x.png"))
    paths.append(make_plot(ly, ry, "Y", "knee_plot_y.png"))
    paths.append(make_plot(lz, rz, "Z", "knee_plot_z.png"))

    return paths


def create_report(image_paths):
    # Initialize a new Word document
    doc = Document()
    doc.add_heading('C3D Report', 0)
    doc.add_paragraph('Knee angles analysis')

    # Embed all generated plot images into the document
    for path in image_paths:
        if path:
            doc.add_picture(path)

    # Ensure output directory exists before saving the report
    os.makedirs("output", exist_ok=True)
    doc.save("output/report.docx")
