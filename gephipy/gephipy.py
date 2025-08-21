import jpype
from pathlib import Path
import urllib.request
import networkx as nx

from org.openide.util import Lookup
from org.gephi.graph.api import GraphController
from org.gephi.project.api import ProjectController

GTK_URL="https://repo1.maven.org/maven2/org/gephi/gephi-toolkit/0.10.1/gephi-toolkit-0.10.1-all.jar"

#
# Initialize the context
#
def initialize(gephi_jar_path="./gephi-toolkit-all.jar"):
    gtk_jar = Path(gephi_jar_path)
    if not gtk_jar.is_file():
      print("Download the Gephi toolkit jar")
      urllib.request.urlretrieve(GTK_URL, gephi_jar_path)
    # Starts the JVM with the GTK in the classpath
    try:
      jpype.startJVM(classpath=[gephi_jar_path])
    except OSError as e: 
      print(f"Warning: {e}")

#
# Create a new Gephi project in a fresh workspace and returns it associated graph model instance
#
def gephi_create_graph(): 
  # Create a Gephi workspace
  pc = Lookup.getDefault().lookup(ProjectController)
  pc.newProject()
  workspace = pc.getCurrentWorkspace()
  # returns the graph model
  return Lookup.getDefault().lookup(GraphController).getGraphModel(workspace)

#
# Function to load a NetworkX instance in Gephi
# This function takes a networkX instance and returns a Gephi graphModel
#
def networkx_to_gephi(graphX):
  # Get the Graph
  graphModel = gephi_create_graph()
  directedGraph = graphModel.getDirectedGraph()

  # Cast NetworkX graph to Gephi
  for node in graphX.nodes:
    nodeAttributs = graphX.nodes[node]
    node = graphModel.factory().newNode(f"{node}")
    if "label" in nodeAttributs:
      node.setLabel(nodeAttributs["label"])
    # TODO: add node attributes
    directedGraph.addNode(node)

  for source, target in graphX.edges():
    edgeAttributs = graphX[source][target]
    edgeWeight = edgeAttributs["weight"] if "weight" in edgeAttributs else 0.0
    sourceNode = directedGraph.getNode(f"{source}")
    targetNode = directedGraph.getNode(f"{target}")
    edge = graphModel.factory().newEdge(sourceNode, targetNode, 0, edgeWeight, True)
    # TODO: add edge attributes
    directedGraph.addEdge(edge)

  return graphModel

#
# Gephi to NetworkX
#
def gephi_to_networkx(graphModel):
  directedGraph = graphModel.getDirectedGraph()
  graphX = nx.Graph()
    
  nodeIter = directedGraph.getNodes().iterator()
  while nodeIter.hasNext():
    node = nodeIter.next()
    graphX.add_node(node.getId())
    edgeIter = directedGraph.getEdges().iterator()
  
  while edgeIter.hasNext():
    edge = edgeIter.next()
    graphX.add_edge(edge.getSource().getId(), edge.getTarget().getId())

  return graphX

#
# Export the current Gephi graph to an GEXF file
#
def export_gexf(file_path="./graph.gexf"):
  export = Lookup.getDefault().lookup(ExportController)
  export.exportFile(File(file_path))
  

#
# Export the current Gephi graph to an PDF file
#
def export_pdf(file_path="./graph.pdf"):
  export = Lookup.getDefault().lookup(ExportController)
  pdf = export.getExporter("pdf")
  export.exportFile(File(file_path),pdf)
  
#
# Export the current Gephi graph to an SVG file
#
def export_svg(file_path="./graph.svg"):
  export = Lookup.getDefault().lookup(ExportController)
  svg = export.getExporter("svg")
  export.exportFile(File(file_path), svg)
  
#
# Export the current Gephi graph to an PNG file
#
def export_png(file_path="./graph.png"):
  export = Lookup.getDefault().lookup(ExportController)
  png = export.getExporter("png")
  export.exportFile(File(file_path), png)