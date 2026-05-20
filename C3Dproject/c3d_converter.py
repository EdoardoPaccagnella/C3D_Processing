import ezc3d
import json
import os
import math

# Handles invalid numerical data (NaN/Inf) by converting them to None for JSON compatibility
def safe_float(val):
    if math.isnan(val) or math.isinf(val):
        return None
    return float(val)

def process_c3d(file_path, output_dir):
    # Load the C3D file and extract metadata (labels, frame rate) and point data
    c3d = ezc3d.c3d(file_path)
    labels = c3d['parameters']['POINT']['LABELS']['value']
    points = c3d['data']['points']
    point_rate = c3d['header']['points']['frame_rate']

    # Calculate the time vector based on the frame rate
    n_frames = points.shape[2]
    times = [i / point_rate for i in range(n_frames)]

    angles_json = {"data": []}
    moments_json = {"data": []}
    powers_json = {"data": []}

    # Helper function to structure X, Y, Z coordinates and time for each frame
    def build_entry(label, i, unit):
        values = []
        for f in range(n_frames):
            values.append({
                "x": safe_float(points[0, i, f]),
                "y": safe_float(points[1, i, f]),
                "z": safe_float(points[2, i, f]),
                "time": times[f]
            })
        return {
            "label": label,
            "description": "",
            "values": values,
            "unit": unit
        }

    # Sort data into categories (Angles, Moments, Powers) based on the point labels
    for i, label in enumerate(labels):
        if "Angle" in label:
            angles_json["data"].append(build_entry(label, i, "deg"))
        elif "Moment" in label:
            moments_json["data"].append(build_entry(label, i, "Nm"))
        elif "Power" in label:
            powers_json["data"].append(build_entry(label, i, "W"))

    os.makedirs(output_dir, exist_ok=True)

    # Save the processed data into three separate structured JSON files
    with open(os.path.join(output_dir, "angles.json"), "w") as f:
        json.dump(angles_json, f, indent=2)

    with open(os.path.join(output_dir, "moments.json"), "w") as f:
        json.dump(moments_json, f, indent=2)

    with open(os.path.join(output_dir, "powers.json"), "w") as f:
        json.dump(powers_json, f, indent=2)

    return angles_json, moments_json, powers_json
