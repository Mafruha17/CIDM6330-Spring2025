import graphviz
import os
import shutil

# Create a folder for UML diagrams
output_folder = "UML_Diagrams"
os.makedirs(output_folder, exist_ok=True)

def save_diagram(diagram, filename):
    """Helper function to save diagrams"""
    path = os.path.join(output_folder, filename)
    diagram.render(path, format="png", cleanup=True)

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

# 3. Component Diagram
component_diagram = graphviz.Digraph(format='png')
component_diagram.attr(rankdir='TB')
components = ['PatientApp', 'ProviderPortal', 'AdminPortal', 'Database', 'API']
for c in components:
    shape = 'cylinder' if c == 'Database' else 'component'
    component_diagram.node(c, shape=shape)

component_diagram.edge('PatientApp', 'API', label='Sends Data')
component_diagram.edge('ProviderPortal', 'API', label='Retrieves Data')
component_diagram.edge('AdminPortal', 'API', label='Manages Users')
component_diagram.edge('API', 'Database', label='Stores Data')

save_diagram(component_diagram, "ComponentDiagram")

# 4. Class Diagram
class_diagram = graphviz.Digraph(format='png')
class_diagram.attr(rankdir='TB')

class_diagram.node('Patient', shape='record', label="{Patient|+Name: String\l+ID: Int\l+Devices: List\l}")
class_diagram.node('Device', shape='record', label="{Device|+Type: String\l+Data: String\l}")
class_diagram.node('Provider', shape='record', label="{Provider|+Name: String\l+Patients: List\l}")
class_diagram.node('Admin', shape='record', label="{Admin|+Role: String\l+Permissions: String\l}")

class_diagram.edge('Patient', 'Device', label='Owns')
class_diagram.edge('Provider', 'Patient', label='Monitors')
class_diagram.edge('Admin', 'Provider', label='Manages')

save_diagram(class_diagram, "ClassDiagram")

# Create a ZIP file with all UML diagrams
shutil.make_archive(output_folder, 'zip', output_folder)

print("✅ UML Diagrams successfully generated! Check the 'UML_Diagrams' folder.")
print("✅ ZIP file created: UML_Diagrams.zip")
