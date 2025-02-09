import graphviz

test_diagram = graphviz.Digraph(format='png')
test_diagram.node('A', label="Test Node A")
test_diagram.node('B', label="Test Node B")
test_diagram.edge('A', 'B', label="Test Edge")
test_diagram.render("Test_UML_Diagrams/Test_Graphviz")

print("✅ Test Graphviz Diagram Created!")
