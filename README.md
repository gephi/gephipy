 # Gephipy

This project is Python wrapper of [Gephi toolkit](https://gephi.org/toolkit/), thanks to [Jpype](https://www.jpype.org) which does the bindings between Java and Python.

It provides helpers to easy the use of Gephy toolkit for Pythonist, even if you still ned to know the Java API.

## How to use 

* Install the lib `pip install gephipy`

* Import gephipy

```python
from gephipy import gephipy

```

Then you can use the Gephi toolkit or the GephiPy features.

## Example 

```python
from gephipy import gephipy

# Java imports must be after the gephipy import
from org.gephi.layout.plugin.forceAtlas2 import ForceAtlas2Builder
from org.gephi.layout.plugin.random import Random
from org.gephi.layout.plugin.noverlap import NoverlapLayoutBuilder
from org.gephi.statistics.plugin import Modularity, GraphDistance
from org.openide.util import Lookup
from org.gephi.appearance.api import AppearanceController
from org.gephi.appearance.plugin import RankingNodeSizeTransformer, PartitionElementColorTransformer
from org.gephi.appearance.plugin.palette import PaletteManager
from org.gephi.statistics.plugin import GraphDistance, Modularity

#
# Create a workspace
#
workspace = gephipy.create_workspace()

#
# Import a GEXF file
#
gephipy.import_gexf(workspace, "./graph.gexf")
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
random.initAlgo();
random.goAlgo()
random.endAlgo();

# FA2 layout
fa2 = ForceAtlas2Builder().buildLayout()
fa2.setGraphModel(gephipy.get_graph_model(workspace))
fa2.resetPropertiesValues();
fa2.initAlgo();
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

gephipy.export_gexf(workspace, "my-gephi-graph.gexf")
```
