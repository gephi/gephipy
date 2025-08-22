import jpype
import jpype.imports
import networkx as nx

# Starting the JVM
from gephipy import jvm
jvm.start()

# Java import
from java.io import File
from org.openide.util import Lookup
from org.gephi.graph.api import GraphController
from org.gephi.project.api import ProjectController
from org.gephi.io.processor.plugin import DefaultProcessor
from org.gephi.io.exporter.api import ExportController
from org.gephi.io.importer.api import ImportController, EdgeDirectionDefault

#
# Create a new Gephi workspace
#
def create_workspace(): 
  # Create a Gephi workspace
  pc = Lookup.getDefault().lookup(ProjectController)
  pc.newProject()
  return pc.getCurrentWorkspace()

#
# Get the graph model of
#
def get_graph_model(workspace): 
  return Lookup.getDefault().lookup(GraphController).getGraphModel(workspace)

#
# Function to load a NetworkX instance in Gephi
# This function takes a networkX instance and returns a Gephi graphModel
#
def networkx_to_gephi(workspace, graphX):
  # Get the Graph
  graphModel = Lookup.getDefault().lookup(GraphController).getGraphModel(workspace)
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


#
# Gephi to NetworkX
#
def gephi_to_networkx(workspace):
  graphModel = Lookup.getDefault().lookup(GraphController).getGraphModel(workspace)
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
# Import a GEXF
#
def import_gexf(workspace, file_path=""):
  importController = Lookup.getDefault().lookup(ImportController)
  file = File(file_path)
  container = importController.importFile(file)
  container.getLoader().setEdgeDefault(EdgeDirectionDefault.DIRECTED)
  importController.process(container, DefaultProcessor(), workspace);
#
# Export the current Gephi graph to an GEXF file
#
def export_gexf(workspace, file_path="./graph.gexf"):
  export = Lookup.getDefault().lookup(ExportController)
  gexf = export.getExporter("gexf")
  gexf.setWorkspace(workspace)
  export.exportFile(File(file_path))
  

#
# Export the current Gephi graph to an PDF file
#
def export_pdf(workspace, file_path="./graph.pdf"):
  export = Lookup.getDefault().lookup(ExportController)
  pdf = export.getExporter("pdf")
  pdf.setWorkspace(workspace)
  export.exportFile(File(file_path),pdf)
  
#
# Export the current Gephi graph to an SVG file
#
def export_svg(workspace, file_path="./graph.svg"):
  export = Lookup.getDefault().lookup(ExportController)
  svg = export.getExporter("svg")
  svg.setWorkspace(workspace)
  export.exportFile(File(file_path), svg)
  
#
# Export the current Gephi graph to an PNG file
#
def export_png(workspace, file_path="./graph.png"):
  export = Lookup.getDefault().lookup(ExportController)
  png = export.getExporter("png")
  png.setWorkspace(workspace)
  export.exportFile(File(file_path), png)