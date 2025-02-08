import graphviz
import os
import shutil

# Create a folder for UML diagrams
output_folder = "UML_Diagrams"
os.makedirs(output_folder, exist_ok=True)

def save_diagram(diagram, filename):
    """Helper function to save diagrams"""
    path = os.path.join(output_folder, filename)
    diagram.render(path, format="png")

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

# Save the diagram
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

# Save the sequence diagram
sequence_diagram.render("UML_Diagrams/Enhanced_SequenceDiagram", format="png")

print("✅ Enhanced Sequence Diagram Generated with Lifelines and Activation Bars")

# 3. Component Diagram
component_diagram = graphviz.Digraph(format='png')
component_diagram.attr(rankdir='TB')
component_diagram.node('PatientApp', shape='component')
component_diagram.node('ProviderPortal', shape='component')
component_diagram.node('AdminPortal', shape='component')
component_diagram.node('Database', shape='cylinder')
component_diagram.node('API', shape='component')

component_diagram.edge('PatientApp', 'API', label='Sends Data')
component_diagram.edge('ProviderPortal', 'API', label='Retrieves Data')
component_diagram.edge('AdminPortal', 'API', label='Manages Users')
component_diagram.edge('API', 'Database', label='Stores Data')

save_diagram(component_diagram, "ComponentDiagram")

# 4. Class Diagram
class_diagram = graphviz.Digraph(format='png')
class_diagram.attr(rankdir='TB')

class_diagram.node('Patient', shape='rectangle', label='{Patient|+Name: String\\l+ID: Int\\l+Devices: List\\l}')
class_diagram.node('Device', shape='rectangle', label='{Device|+Type: String\\l+Data: String\\l}')
class_diagram.node('Provider', shape='rectangle', label='{Provider|+Name: String\\l+Patients: List\\l}')
class_diagram.node('Admin', shape='rectangle', label='{Admin|+Role: String\\l+Permissions: String\\l}')

class_diagram.edge('Patient', 'Device', label='Owns')
class_diagram.edge('Provider', 'Patient', label='Monitors')
class_diagram.edge('Admin', 'Provider', label='Manages')

save_diagram(class_diagram, "ClassDiagram")

# 5. State Diagram
state_diagram = graphviz.Digraph(format='png')
state_diagram.attr(rankdir='TB')

state_diagram.node('Idle', shape='ellipse')
state_diagram.node('Connected', shape='ellipse')
state_diagram.node('Transmitting Data', shape='ellipse')
state_diagram.node('Error', shape='ellipse')

state_diagram.edge('Idle', 'Connected', label='Pairing Successful')
state_diagram.edge('Connected', 'Transmitting Data', label='Sends Health Data')
state_diagram.edge('Transmitting Data', 'Idle', label='Data Sent')
state_diagram.edge('Connected', 'Error', label='Failure')

save_diagram(state_diagram, "StateDiagram")

# 6. Deployment Diagram
deployment_diagram = graphviz.Digraph(format='png')
deployment_diagram.attr(rankdir='TB')

deployment_diagram.node('Patient Device', shape='box')
deployment_diagram.node('Cloud Server', shape='box')
deployment_diagram.node('Database Server', shape='cylinder')
deployment_diagram.node('Provider System', shape='box')

deployment_diagram.edge('Patient Device', 'Cloud Server', label='Sends Data')
deployment_diagram.edge('Cloud Server', 'Database Server', label='Stores Data')
deployment_diagram.edge('Provider System', 'Cloud Server', label='Retrieves Data')

save_diagram(deployment_diagram, "DeploymentDiagram")

# Create a ZIP file with all UML diagrams
shutil.make_archive(output_folder, 'zip', output_folder)

print("✅ UML Diagrams successfully generated! Check the 'UML_Diagrams' folder.")
print("✅ ZIP file created: UML_Diagrams.zip")
