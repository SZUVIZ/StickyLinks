
# Sticky Links
implement of [Sticky Links：Encoding Quantitative Data of Graph Links]() [To revise]


## 🔗 [Paper]()|[Project](https://github.com/deardeer/Node-SpikeLink)|[video](https://www.liaoxuefeng.com/wiki/896043488029600/896827951938304)
![image](https://github.com/maymayuo/Spiky-Links/blob/main/NewOverview.png)
    we present __Sticky Links__, a novel visual encoding method that draws graph links with __stickiness__. Taking the metaphor of links with glues, sticky links represent connection strength using spiky shapes, ranging from two broken spikes for weak connections to connected lines for strong connections. 


## Dependencies
* python: we used Python3.9 and 3.11, the later one is recommended

* python third-Party libraries:
 ```bash
 -pycairo>=1.19.1(pycairo==1.22.0 is recommended)
 -numpy(numpy=1.24.3 is recommended)
```

## 💻Usage on Windows 
### Download / Install
```bash
pip install NodeSpikyLinks
```
Note that if you fail to install dependencies with  `pip install NodeSpikyLinks`, you can fix with`pip install pycairo==1.22.0 numpy==1.24.3`.
### Import
```bash
from NodesSpikyLinks import aa_drawing
```
use `from NodesSpikyLinks import aa_drawing` to import our stickiness drawing.

### Run
```bash
aa_drawing.run()
```
 after you run it, you are prompted to input your data path, here is the path exmaple:
 ```bash
 path=('C:\\NodeSpikyLinks\\drawingData\\miserables_layout.json')
```
 In the end, input drawing styles including convention, spike and straight. when you input "spike" or "straight", you are supposed to input the stickiness values in the form of numbers ranging from zero to one. Now, your expected works are generated!:100:


## 📊Example of  Data
our graph format supports two representations: 
### 1️⃣Edge List (Space-Delimited):
```
0 1 0.3
0 2 0.8
1 2 0.5

```
'0 1 3.0' means there is an edge from source node 0 to taget node 1 with 0.3 weight.The edge list is assumed to be undirected.The reader accepts only space delimited edge lists
### 2️⃣Json-Like Format:
Alternatively, you can use a JSON-like format for a more structured representation, as shown in the example above.

```js
{
  "type": "graph.layout",
  "nodes": [
    {
      "name": "0",
      "pos": {
        "x": -434.64355,
        "y": 959.1635
      }
    },
    {
      "name": "1",
      "pos": {
        "x": 422.963,
        "y": 1153.1467
      }
    },
    {
      "name": "2",
      "pos": {
        "x": 266.72882,
        "y": 524.0617
      }
    }
  ],
  "links": [
    {
      "key": "0",
      "source": "0",
      "target": "0",
      "weight": 1.0
    },
    {
      "key": "1",
      "source": "0",
      "target": "399",
      "weight": 0.3000
    },
    {
      "key": "2",
      "source": "0",
      "target": "1311",
      "weight": 0.8324
    }
  ]
}

```
  
## API Reference


#### 1️⃣readdata(data_path)


    changes the form of data from json to dictionary and creates global lists,which are "all_nodes"and"all_links" from converted dictionary of "nodes" and "links" respectively
 

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `data_path` | `string` | **Required**: Absolute path  where the JSON file resides in  local disk |


#### 2️⃣nodes_out()

    Creates global lists,which are "all_names"and "all_pos" from the key of "names" and "pos" in "all_nodes"and "all_links" respectively


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `all_nodes`      | list| a global variable and consists of dictionary.
      

#### 3️⃣links_out()

    Creates "source_target_allout",a global list of dictionary,like [{"source":"Walter","target":"myriel"}] 

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `all_links`      | list| a global variable and consists of dictionary.

#### 4️⃣ get_sourcetargetpos(HEIGHT_SURFACE)


    Creates global lists,which are "source_pos_new"and"target_pos_new" used for following drawing and calculation


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `all_nodes`      | list| see above description for details
| `all_links`      | list| be similar to "all_nodes"in structure
| ` HEIGHT_SURFACE `   |constant| refers to the height of surface where we draw graphic 

#### 5️⃣generate_stickyspike(drawStyle,encodeInfo,prop,source_pos_new,target_pos_new,SOURCE_RADIUS,TARGET_RADIUS)


    returns thirdpos and handlepoint that are used when drawing curves. 
  
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `drawstyle`      | string|  the edge style between source and target,including"convention"、"spike"and"straight"
| `encodeInfo`      | string | value is "constant"
| `prop`      | dictionary | key is "constant" and value is '0.4'

#### 6️⃣ getStickiness(encodeInfo,prop)

    Returns stickiness which control the shape of spike 

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `encodeInfo`      | string | see above
| `prop`      | dictionary | see above

####  7️⃣getAnchors(ball1_pos,ball2_pos,stickiness,drawStyle,SOURCE_RADIUS,TARGET_RADIUS)

    Returns two pairs of pa and pb on source and target circles when we draw "straight"and "spike" edges

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `ball1_pos`      | list |equal to "source_pos_new" generated by get_sourcetargetpos()
| `ball2_pos`      | list |equal to "target_pos_new"generated by get_sourcetargetpos()
| `stickiness`      | constant |generated by getStickiness(encodeInfo,prop)
| `drawStyle`      | string |see above

#### 8️⃣ drawStyle(pab,thirds,drawStyle,source_pos_new,target_pos_new,SOURCE_RADIUS,TARGET_RADIUS,WIDTH_SURFACE,HEIGHT_SURFACE)

    Draws different edges depending on the value of "drawStyle" and circles 

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pab`      |dictionary | one pair points of it shows symmetry of circle's center generated by getAnchors()
| `thirds`      | dictionary | it is calculated by pa、pb、source_pos_new and target_pos_new.Also,it helps draw "spike"and "straight"
| `WIDTH_SURFACEs`      |constant |refers to the width of surface where we draw graphic  

#### 9️⃣ relationMatrix()

   Returns a numpy.ndarray which map connection realtion,that is the source circles should link to the right aimed target circles based on data


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `all_nodes`      | dictionary |see above
| `source_target_allout`      | dictionary |generated by function links_out

#### 🔟⚫ drawCircles(context,center1,center2,radius1,radius2)

     Draws circle shapes in every positions on the given surface
 


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `context`      | dictory |to draw with cairo, you should create a "context" whatever names to set surface which is known as "canvas" in other libraries
| `center1`      | list |Here we can pass (x,y) coordinates for the center of the source circles
| `center2`      | list |Here we can pass (x,y) coordinates for the center of the target circles
| `radius1`      | constant | the radius of source circles
| `radius2`      | constant | the radius of target circles















## 📔Citation

If you find our work useful for your research, please consider citing the following papers :)

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
