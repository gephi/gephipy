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
def initialize():
    gtk_jar = Path("./gephi-toolkit-all.jar")
    if not gtk_jar.is_file():
      print("Download the Gephi toolkit jar")
      urllib.request.urlretrieve(GTK_URL, "gephi-toolkit-all.jar")
    # Starts the JVM with the GTK in the classpath
    try:
      jpype.startJVM(classpath=["./gephi-toolkit-all.jar"])
    except OSError as e: 
      print(f"Warning: {e}")

#
# Function to load a NetworkX instance in Gephi
# This function takes a networkX instance and returns a Gephi graphModel
#
def networkx_to_gephi(graphX):
  # Create a Gephi workspace
  pc = Lookup.getDefault().lookup(ProjectController)
  pc.newProject()
  workspace = pc.getCurrentWorkspace()

  # Get the Graph
  graphModel = Lookup.getDefault().lookup(GraphController).getGraphModel(workspace)
  directedGraph = graphModel.getDirectedGraph()

  # Cast NetworkX graph to Gephi
  for node in graphX.nodes:
    nodeAttributs = graphX.nodes[node]
    node = graphModel.factory().newNode(f"{node}")
    if "label" in nodeAttributs:
      node.setLabel(nodeAttributs["label"])
    directedGraph.addNode(node)

  for source, target in graphX.edges():
    edgeAttributs = graphX[source][target]
    edgeWeight = edgeAttributs["weight"] if "weight" in edgeAttributs else 0.0
    sourceNode = directedGraph.getNode(f"{source}")
    targetNode = directedGraph.getNode(f"{target}")
    edge = graphModel.factory().newEdge(sourceNode, targetNode, 0, edgeWeight, True)
    directedGraph.addEdge(edge)

  return graphModel

#
# gephi to networkX
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