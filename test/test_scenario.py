import pytest
from pathlib import Path
import networkx as nx

from gephipy import gephipy 

# Must be imported after gephipy
from org.gephi.layout.plugin.forceAtlas2 import ForceAtlas2Builder
from org.gephi.layout.plugin.random import Random
from org.gephi.layout.plugin.noverlap import NoverlapLayoutBuilder
from org.gephi.statistics.plugin import Modularity, GraphDistance
from org.openide.util import Lookup
from org.gephi.appearance.api import AppearanceController
from org.gephi.appearance.plugin import RankingNodeSizeTransformer, PartitionElementColorTransformer
from org.gephi.appearance.plugin.palette import PaletteManager
from org.gephi.statistics.plugin import GraphDistance, Modularity


def test_scenario(): 
  #
  # Create a workspace
  #
  workspace = gephipy.create_workspace()

  
  # Create a random graph with NetworkX
  graphX = nx.erdos_renyi_graph(500,0.01)
  gephipy.networkx_to_gephi(workspace, graphX)
  graphModel = gephipy.get_graph_model(workspace)

  #
  # Compute some metrics
  #

  # Louvain
  modularity = Modularity()
  modularity.execute(graphModel)

  # Betweeness centrality
  centrality = GraphDistance()
  centrality.setDirected(True)
  centrality.execute(graphModel)

  #
  # Apply appearance
  # Here it is really looks like java code
  #

  appearanceController = Lookup.getDefault().lookup(AppearanceController)
  appearanceModel = appearanceController.getModel()

  # Size Make node size based on centrality
  centralityColumn = graphModel.getNodeTable().getColumn(GraphDistance.BETWEENNESS)
  centralityRanking = appearanceModel.getNodeFunction(centralityColumn, RankingNodeSizeTransformer)
  centralityTransformer = centralityRanking.getTransformer()
  centralityTransformer.setMinSize(10)
  centralityTransformer.setMaxSize(100)
  appearanceController.transform(centralityRanking)


  # Color by community
  communityColumn = graphModel.getNodeTable().getColumn(Modularity.MODULARITY_CLASS)
  colorPartition = appearanceModel.getNodeFunction(communityColumn, PartitionElementColorTransformer)
  partition = colorPartition.getPartition()
  palette = PaletteManager.getInstance().generatePalette(partition.size(graphModel.getGraph()))
  partition.setColors(graphModel.getGraph(), palette.getColors())
  appearanceController.transform(colorPartition)

  #
  # Run Layouts
  #

  # Random layout
  random = Random().buildLayout()
  random.setGraphModel(gephipy.get_graph_model(workspace))
  random.initAlgo()
  random.goAlgo()
  random.endAlgo()

  # FA2 layout
  fa2 = ForceAtlas2Builder().buildLayout()
  fa2.setGraphModel(gephipy.get_graph_model(workspace))
  fa2.resetPropertiesValues()
  fa2.initAlgo()
  for x in range(1000):
    fa2.goAlgo()

  # Noverlap layout
  noverlap = NoverlapLayoutBuilder().buildLayout()
  noverlap.setGraphModel(gephipy.get_graph_model(workspace))
  noverlap.initAlgo()
  noverlap.endAlgo()

  #
  # Export your graph
  #
  gephipy.export_gexf(workspace, "test-export-graph.gexf")
  file = Path("./test-export-graph.gexf")
  assert file.is_file() == True
    
  gephipy.export_svg(workspace, "test-export-graph.svg")
  file = Path("./test-export-graph.svg")
  assert file.is_file() == True
    
  gephipy.export_pdf(workspace, "test-export-graph.pdf")
  file = Path("./test-export-graph.pdf")
  assert file.is_file() == True
    
  # PNG requires a display ?
  # gephipy.export_png(workspace, "test-export-graph.png")
  # file = Path("./test-export-graph.png")
  # assert file.is_file() == True