import graphviz
import os
import shutil

# Ensure Graphviz is installed
try:
    graphviz.version()
except graphviz.ExecutableNotFound:
    raise RuntimeError("Graphviz is not installed or not in the system PATH. Please install Graphviz.")

# Create a folder for UML diagrams
output_folder = "UML_Diagrams"
os.makedirs(output_folder, exist_ok=True)

def save_diagram(diagram, filename):
    """Helper function to save diagrams"""
    path = os.path.join(output_folder, filename)
    try:
        diagram.render(path, format="png", engine="dot", cleanup=True, quiet=False)
    except graphviz.ExecutableNotFound:
        raise RuntimeError("Graphviz executable not found. Ensure it is installed and accessible.")

# 1. Use Case Diagram
use_case = graphviz.Digraph(format='png')
use_case.attr(rankdir='TB')
use_case.node('Patient', shape='ellipse')
use_case.node('Provider', shape='ellipse')
use_case.node('Admin', shape='ellipse')
use_case.node('Device', shape='ellipse')
use_case.node('System', shape='rectangle')

use_case.edge('Patient', 'Device', label='Connects & Sends Data')
use_case.edge('Device', 'System', label='Sends Data To')
use_case.edge('System', 'Provider', label='Provides Data To')
use_case.edge('Provider', 'System', label='Monitors Patient Data')
use_case.edge('Admin', 'System', label='Manages Users & Logs')

save_diagram(use_case, "UseCaseDiagram")

# 2. Sequence Diagram - Device Data Integration with Lifelines
sequence_diagram = graphviz.Digraph(format='png')
sequence_diagram.attr(rankdir='TB')

# Define participants (lifelines)
sequence_diagram.node('Patient', shape='rect', label="────────────\nPatient\n────────────", style="dotted")
sequence_diagram.node('Device', shape='rect', label="────────────\nDevice\n────────────", style="dotted")
sequence_diagram.node('System', shape='rect', label="────────────\nSystem\n────────────", style="dotted")
sequence_diagram.node('Provider', shape='rect', label="────────────\nProvider\n────────────", style="dotted")

# Define interactions with activation bars
sequence_diagram.edge('Patient', 'Device', label='Pair Device')
sequence_diagram.node('Device_Active', shape="box", label="<< Activation >>", style="filled", fillcolor="lightgray")
sequence_diagram.edge('Device', 'Device_Active', style="dotted")

sequence_diagram.edge('Device', 'System', label='Send Health Data')
sequence_diagram.node('System_Active', shape="box", label="<< Activation >>", style="filled", fillcolor="lightgray")
sequence_diagram.edge('System', 'System_Active', style="dotted")

sequence_diagram.edge('System', 'Provider', label='Notify Provider')
sequence_diagram.node('Provider_Active', shape="box", label="<< Activation >>", style="filled", fillcolor="lightgray")
sequence_diagram.edge('Provider', 'Provider_Active', style="dotted")

sequence_diagram.edge('Provider', 'System', label='Retrieve Patient Data')
sequence_diagram.edge('System', 'Device', label='Acknowledge Data Received')
sequence_diagram.edge('Device', 'Patient', label='Display Status')

# End activations (Deactivations are shown as dotted edges to mimic UML)
sequence_diagram.edge('Device_Active', 'Device', style="dotted")
sequence_diagram.edge('System_Active', 'System', style="dotted")
sequence_diagram.edge('Provider_Active', 'Provider', style="dotted")

save_diagram(sequence_diagram, "SequenceDiagram")

print("✅ Enhanced Sequence Diagram Generated with Lifelines and Activation Bars")

# Create a ZIP file with all UML diagrams
try:
    shutil.make_archive(output_folder, 'zip', output_folder)
    print("✅ ZIP file created: UML_Diagrams.zip")
except Exception as e:
    print(f"❌ Error creating ZIP file: {e}")

print("✅ UML Diagrams successfully generated! Check the 'UML_Diagrams' folder.")
