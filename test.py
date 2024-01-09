
# NodeStickyLinks Package Usage Examples
# ---------------------------------------
# This script demonstrates two ways to use the NodeStickyLinks package:
# 1. Running an interactive user interface for graph visualization.
# 2. Programmatically drawing a graph with specific parameters.
# Follow the instructions in each section to see how each method works.
# Uncomment the necessary lines to execute the examples.
# ----------------------------------------------------

from NodeStickyLinks import run_drawsticky
from NodeStickyLinks import drawsticky

# ----------------------------------------------------
# Example 1: Run StickyLinks Interactive User Interface
# ----------------------------------------------------

# To use the interactive user interface of NodeStickyLinks, 
# simply call the run() function from the run_drawsticky module.
# This will launch the interface where you can interactively 
# draw and visualize graphs.

run_drawsticky.run()


# ----------------------------------------------------
# Example 2: Programmatically Draw a Graph with Specified Parameters
# ----------------------------------------------------

# If you prefer to programmatically draw a graph with specific parameters,
# you can use the draw_graph function from the drawsticky module.
# First, define the parameters for the graph drawing:

# edge_style: Choose between 'thickness' or 'stickiness' for edge style
# file_path: Path to your JSON or CSV data file
# nodes_radius: Radius of the nodes in the graph
# edge_width: Width of the edges in the graph
# canvas_width, canvas_height: Dimensions of the canvas for the drawing

edge_style = 'stickiness'  # Example: 'stickiness'
file_path = "path/to/your/datafile.json"  # Replace with the path to your data file
nodes_radius = 5.0  # Example: 5.0
edge_width = 2  # Example: 2
canvas_width = 700  # Example: 700
canvas_height = 700  # Example: 700

# Now, draw the graph with the specified parameters.
# This will create 'graph.svg' and 'graph.png' files,
# containing the visual representation of the graph.

drawsticky.draw_graph(edge_style, file_path, nodes_radius, edge_width, canvas_width, canvas_height)

# Note: Uncomment the lines in this section to execute the example.
