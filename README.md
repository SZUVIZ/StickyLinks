# StickyLinks: A Novel Edge Drawing in Node-link Diagram

A Python implementation of paper 🔗 [Sticky Links: Encoding Quantitative Data of Graph Edges](https://deardeer.github.io/)

![image](https://github.com/SZUVIZ/StickyLinks/blob/main/overview.png)
    __Sticky Links__ is introduced as a novel visual encoding method that draws graph links with __stickiness__, as shown in the right of the above figure. The conventional graph links use their thickness to encode quantitative attributes (shown on the left). Taking the metaphor of links with glues, sticky links represent numerical link attributes using spiky shapes, ranging from two broken spikes for weak connections to connected lines for strong connections.

[check out an online demo](http://175.178.152.10:8890/)

## Dependencies & Installation

StickyLinks requires the following Python packages:

- **Python**: Version 3.9 or later (3.11 recommended).
- **Third-Party Libraries**:

  - `pandas`: For data manipulation and analysis.
  - `networkx`: To create and work with a common graph layout algorithm.
  - `pycairo`: A set of Python bindings for the Cairo graphics library.

Install these packages using the following command:

```bash

pip install pandas networkx pycairo

```

- **Install our library NodeStickyLinks**:

To install StickyLinks, open your command prompt and run:

```bash

pip install NodeStickyLinks

```

## Usage on Windows

There are two kinds of ways you might use our NodeStickyLinks library to draw graphs with sticky links.
One is to envoke the functions in your python source code. The other is to use our interactive UI interface to draw the graph.

### 1. Envoke StickyLinks in Python Source Codes

If you're coding on a Python project and want to use StickyLinks for graph visualization, you can import and envode its functions as part of your code.

1. **Import the Package**:
   First, import the `drawsticky` module in your Python script:

   ```python

   from NodeStickyLinks import drawsticky

   ```
2. **Utilize Drawing Functions**:
   Second, use the function `drawsticky` to draw graphs and edges. Here's an example of how you can use this function:

   ```python

   # Example usage
   #Define parameters for the graph drawing()
   from NodeStickyLinks import drawsticky
   edge_style = 'stickiness' # Choose 'thickiness' or 'stickiness'
   file_path =  'path/to/your/datafile.json'  # Path to the JSON or CSV data file
   nodes_radius = 5.0 # Radius of the nodes
   edge_width = 2 # Width of the canvas for the drawing
   canvas_width = 700 # Width of the canvas for the drawing
   canvas_height = 700 # Height of the canvas for the drawing

   # Draw the graph
   draw_graph(edge_style, file_path, nodes_radius, edge_width, canvas_width, canvas_height)

   # After running the above function, two files will be created:
   # 'graph.svg' and 'graph.png', containing the visual representation of the graph.


   ```

   Replace the function calls in the example with the actual functions you need from the `drawsticky` module, based on your graph drawing requirements.

### 2. Run StickyLinks Interactive User Interface

We developed a mini UI for interactive usage of StickyLinks, where you can type in parameters and see results without writing any code.

1. **Run the Interactive Script**:

Firstly, use Python to run the `run_drawsticky` module, which contains the interactive `run` function:

```python

  from NodeStickyLinks import run_drawsticky

  run_drawsticky.run()

```

2. **Follow the Prompts**

The script will prompt you for inputs, including the path to your data file, and other parameters required for drawing your graph. Enter these details as prompted to generate the graph visualization.

##### Link Style

- **Prompt**: Choose the style for graph links.
- **Input**: Type `stickiness` or `thickiness`. Please use lowercase letters.
- **Note**: This selection will define the visual appearance of the links in your graph.

##### Canvas Dimensions

- **Prompt**: Set the canvas size for your graph.
- **Input**: Provide width and height in pixels (e.g., 600, 800, 1200).
- **Note**: By default, the canvas is set to a rectangular shape.

##### Node Radius

- **Prompt**: Determine the radius size for nodes in your graph.
- **Input**: Enter a numerical value in pixels, preferably between 2 and 6.
- **Note**: Based on our tests, a radius within this range should provide a balanced visual representation depending on your graph's scale.

##### Line Width

- **Prompt**: Set the width for the lines (edges) in your graph.
- **Input**: Enter a numerical value in pixels, ideally between 1 and 3.
- **Note**: This value should be chosen according to your graph's scale; our testing suggests that values in this range are generally effective.

##### Graph Layout Selection

- **Prompt**: Choose a layout for organizing the graph.
- **Input Options**:

  - `0` for no specific layout.
  - `1` for `circular_layout`.
  - `2` for `random_layout`.
  - `3` for `shell_layout`.
  - `4` for `spring_layout`.
  - `5` for `spectral_layout`.
- **Note**: Each layout option offers a unique arrangement and perspective for your graph nodes.

After completing these inputs, StickyLinks will draw a graph visualization based on your specified preferences.

3. **Output Formats**

After completing the input prompts and processing your data, StickyLinks will generate the graph visualization. The results will be available in two formats:

- **SVG Format**: A scalable vector graphic file, ideal for high-quality, scalable visualizations and for further editing in vector graphic tools such as online editor boxy SVG.
- **PNG Format**: A portable network graphics file.

These files will be saved in the specified output directory or a default location if not specified. You can use these files for presentations, reports, or further analysis.

## 📊 Example of  Data

StickyLinks supports two graph data formats: JSON and CSV. Both formats are intended for undirected graphs. **Most importantly, the values under the 'weight' field must range between 0 and 1.**

### 1️⃣ JSON Graph Format

In the JSON format, your data must include 'nodes' and 'links' fields:

- **Nodes**: Each node should have a 'name' and 'pos' (position) field. The 'pos' field must include 'x' and 'y' coordinates.
- **Links**: Links between nodes. If your graph includes weights, each link can or not have a 'weight' key.
  If the 'weight' key is specified, the graph will be drawn with the specified weights for edges (the first example).
  If no 'weight' key is specified, the graph will be draw with constant weight for edges (the second exmaple).

**JSON1 Example**:

```json

{

    "nodes": [

        {"name": "Node1", "pos": {"x": 0, "y": 0}},

        {"name": "Node2", "pos": {"x": 1, "y": 1}},

        {"name": "Node3", "pos": {"x": 0, "y": 1}}

    ],

    "links": [

        {"source": "Node1", "target": "Node2", "weight": 1},

        {"source": "Node1", "target": "Node3", "weight": 0.2}

    ]

}

```

**JSON2 Example**:

```json

{

    "nodes": [

        {"name": "1", "pos": {"x": 0, "y": 0}},

        {"name": "2", "pos": {"x": 1, "y": 1}},

        {"name": "3", "pos": {"x": 0, "y": 1}}

    ],

    "links": [

        {"source": "1", "target": "2"},

        {"source": "1", "target": "3"}

    ]

}

```

### 2️⃣ CSV Graph Format

StickyLinks also supports CSV-formatted graphs. The CSV files should adhere to the following structure:

- **Delimiter**: we now support comma delimiter.
- **No Headers**: The CSV files should not contain headers.
- **Columns**: The first column is the first node id, the second column is the second node id, and the last column is the edge weight.
- **Encoding**: Files must be UTF-8 encoded.

**CSV1 Example**:

```
0,1,0.6
0,2,0.6
0,3,0.6
```

Ensure that your data files conform to these formats for optimal compatibility with StickyLinks.

## API Reference📚


The `drawsticky` module provides a variety of functions for graph visualization. Below are descriptions of key functions:

#### `draw_graph(edge_style, file_path, nodes_radius, edge_width, canvas_width, canvas_height)`

Renders the entire graph with customizable edge styles, node sizes, and canvas dimensions.

- `edge_style` (str): Style of the edges ('thickness' or 'stickiness').
- `file_path` (str): Path to the data file.
- `nodes_radius` (int): Expected radius of nodes.
- `canvas_width` (int): Width of the canvas.
- `canvas_height` (int): Height of the canvas.

#### `draw_nodes(context, nodes, radius)`

- `context`: Drawing context.
- `nodes` (list): Node data in the form of a list consisting of dictionaries {"x": x1, "y": y1}.
- `radius` (int): Radius of nodes.

#### `draw_stickiness_edge(stickiness, pab, thirds, line_width, context)`

Draw stickiness curves on the given Cairo context.

- `stickiness` (float): Weight value of edge.
- `pab` (dict): Dictionary containing anchor point for drawing.
- `thirds` (dict): Dictionary containing third positions and handles for drawing.
- `context` (cairo.Context): Cairo canvas for drawing.

#### `draw_thickness_edge(source_pos_new, target_pos_new, weight, edge_width, context)`

Draw edges with varying thickness based on the provided weight.

- `source_pos_new` (list): List of dictionaries containing source node positions.
- `target_pos_new` (list): List of dictionaries containing target node positions.
- `weight` (float): Weight of the edges, influencing the thickness of the edge.
- `context` (cairo.Context): Cairo context (canvas) for drawing.

#### `gen_sticky(drawStyle, ss, source_pos_new, target_pos_new, SOURCE_RADIUS, TARGET_RADIUS)`

Generate sticky link visualization parameters based on input parameters.

- `drawStyle` (str): The drawing style, e.g., 'stickiness'.
- `ss` (float): Weight value.
- `source_pos_new` (dict): Dictionary containing the position of the source node.
- `target_pos_new` (dict): Dictionary containing the position of the target node.
- `SOURCE_RADIUS` (float): Radius of the source node.
- `TARGET_RADIUS` (float): Radius of the target node.

#### `get_control_point(ball1_pos, ball2_pos, stickiness, SOURCE_RADIUS, TARGET_RADIUS, angle)`

This function computes anchor points for a sticky link visualization, taking into account various factors such as stickiness, node radius, and interpolation.

- `ball1_pos` (dict): Dictionary containing the position of the source node.
- `ball2_pos` (dict): Dictionary containing the position of the target node.
- `stickiness` (float): Stickiness factor influencing the angle difference.
- `SOURCE_RADIUS` (float): Radius of the source node.
- `TARGET_RADIUS` (float): Radius of the target node.
- `angle`: Radian angle between source and target nodes.

(Note: This is a condensed overview. Please refer to the source code in `drawsticky.py` for detailed comments and more functions.)

## Examples

The visualization presented below showcases the stickiness style applied to the [Miserables Dataset JSON](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/datasets/miserables_layout.json) and [Star War Dataset JSON](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/datasets/starwars_layout_new.json).

![image](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/Pic/Visualization%20Example.png)

## Citation

If you find our work useful for your research, please consider citing our paper :)

```bibtex

@article{Stickylinks2023_lu,

title = {Sticky Links: Encoding Quantitative Data of Graph Edges},

author = {Min Lu, Xiangfang Zeng, Joel Lanir, Xiaoqin Sun, Guozheng Li, Daniel Cohen-Or, and Hui Huang},

journal = {IEEE Transactions on Visualization and Computer Graphics (to appear)},

volume = {},

number = {}, 


pages = {--}, 


year = {2023},

}

```
