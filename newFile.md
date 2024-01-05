# StickyLinks: A Novel Visual Encoding of Edges in Node-link Diagram

A Python implementation of paper 🔗 [Sticky Links: Encoding Quantitative Data of Graph Edges](https://deardeer.github.io/)

![image](https://github.com/maymayuo/Spiky-Links/blob/main/NewOverview.png)
    __Sticky Links__ is introduced as a novel visual encoding method that draws graph links with __stickiness__, as shown in the right of the above figure. The conventional graph links use their thickness to encode quantitative attributes (shown on the left). Taking the metaphor of links with glues, sticky links represent numerical link attribute using spiky shapes, ranging from two broken spikes for weak connections to connected lines for strong connections.

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

   data_path ="path/to/your/datafile.json"  # Replace with your graph data file path

   graph_data = drawsticky.readdata(data_path) 

   node_positions = drawsticky.extract_node_positions(graph_data)

   # ... continue with other function calls as needed

   ```

   Replace the function calls in the example with the actual functions you need from the `drawsticky` module, based on your graph drawing requirements.

### 2. Run StickyLinks Interactive User Interface

We developed a mini UI for interactive usage of StickyLinks, where you can type in parameters and see results without writing any code.

1. **Run the Interactive Script**:

Firstly, use Python to run the `run_drawsticky` module, which contains the interactive `run` function:

```python

  from nodespikylink import run_drawsticky

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
- **Default Setting**: By default, the canvas is set to a rectangular shape.

##### Node Radius

- **Prompt**: Determine the radius size for nodes in your graph.
- **Input**: Enter a numerical value in pixels, preferably between 2 and 6.
- **Recommendation**: Based on our tests, a radius within this range should provide a balanced visual representation depending on your graph's scale.

##### Line Width

- **Prompt**: Set the width for the lines (edges) in your graph.
- **Input**: Enter a numerical value in pixels, ideally between 1 and 3.
- **Suggestion**: This value should be chosen according to your graph's scale; our testing suggests that values in this range are generally effective.

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

StickyLinks also supports CSV formatted graphs. The CSV files should adhere to the following structure:

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

**CSV2 Example**:

```

0,1,0.6
0,2,0.4
0,3,1



```

Ensure that your data files conform to these formats for optimal compatibility with StickyLinks.

## API Reference📚

The `drawsticky` module provides a variety of functions for graph visualization. Below are descriptions of key functions:

### Core Functions🔑

#### `read_data(data_path)`

Reads and parses graph data.

- `data_path` (string): Path to the data file.

#### `draw_graph(context, nodes, edges, params)`

Renders the entire graph.

- `context`: Drawing context.
- `nodes`: Node data.
- `edges`: Edge data.
- `params`: Graph drawing parameters.

### Layout and Style Functions

#### `apply_layout_to_json(json_data, layout_type)`

Applies a specified layout to JSON graph data.

- `json_data`: The graph data in JSON format.
- `layout_type`: Type of layout to apply.

#### `set_line_width(width)`

Sets the line width for drawing.

- `width`: Width of the lines.

### Node and Edge Drawing Functions

#### `draw_nodes(context, nodes, radius)`

Draws graph nodes.

- `context`: Drawing context.
- `nodes`: Node data.
- `radius`: Radius of nodes.

#### `draw_stickiness_edge(...)`, `draw_thickness_edge(...)`

Functions to draw different types of edges.

#### `gen_sticky(...)`

Generates stickiness edges based on parameters.

#### `get_control_point(...)`

Calculate four control points for stickiness edge.

(Note: This is a condensed overview. Please refer to the source code in `drawsticky.py` for detailed comments and more functions.)

## Visualization Examples

StickyLinks can be applied to various datasets to produce insightful visualizations. Below are examples using two different datasets: 'Miserables' and 'StarWars'. Each dataset is visualized using two different layouts to showcase the flexibility of StickyLinks.

### Miserables Dataset(JSON2 Example)

The 'Miserables' dataset visualizations demonstrate how different layouts can impact the presentation of the same data.

#### Original Layout

![Miserables Original Layout](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/Pic/mis_700_5_1.8_0.4_nolayout%402x.png)

#### Spring Layout

![Miserables Spring Layout](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/Pic/mis_700_5_1.8_0.4_spring%402x.png)

### StarWars Dataset(JSON1 Example)

#### Original Layout

![StarWars Original Layout](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/Pic/starwars_700_5_1.8_nolayout%402x.png)

#### Spring Layout

![StarWars Spring Layout](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/Pic/starwar_700_5_1.8_0.4_spring%402x.png)
Similar to the 'Miserables' dataset, the 'StarWars' dataset is shown here with both its original layout and a spring layout.

### Dataset Availability

Developers interested in exploring these visualizations further can access the JSON data for these datasets:

- [Miserables Dataset JSON](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/datasets/miserables_layout.json)
- [StarWars Dataset JSON](https://github.com/SZUVIZ/StickyLinks/blob/main/visualizationExample/datasets/starwars_layout_new.json)

These examples illustrate the adaptability of StickyLinks in representing complex relationships in graphical data.

## Citation

If you find our work useful for your research, please consider citing our paper :)

```bibtex

@article{Winglets19,

title = {Winglets: Visualizing Association with Uncertainty in Multi-class Scatterplots},

author = {Min Lu, Shuaiqi Wang, Joel Lanir, Noa Fish, Yang Yue, Daniel Cohen-Or, Hui Huang},

journal = {IEEE Transactions on Visualization and Computer Graphics (Proceedings of InfoVis 2019)},

volume = {26},

number = {1}, 


pages = {770--779}, 


year = {2020},

}

```
