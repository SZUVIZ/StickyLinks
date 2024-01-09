
import json
import pandas as pd
import networkx as nx
import cairo
import math
import copy
def determine_file_type(file_path):
    """
    Determine the type of a file based on its content and structure.

    This function checks if the file is a JSON or CSV and further classifies 
    it into one of four categories: json1, json2, csv1, or csv2.

    Parameters:
    file_path (str): Path to the file that needs to be classified.

    Returns:
    str: Type of the file ('json1', 'json2', 'csv1', 'csv2').
    """
    try:
        with open(file_path,'r',encoding='utf-8') as file:

            content = json.load(file)
            graph_data = determine_json_type(content)
        return graph_data
    
    except json.JSONDecodeError:
        df = pd.read_csv(file_path,header=None,encoding='utf-8')
        graph_data = determine_csv_type(df,file_path)
        print("graph_data",graph_data)
        return graph_data
    
    except UnicodeDecodeError:
        return "Encoding error: The file could not be read with UTF-8 encoding."

def determine_json_type(json_content):
    if 'links' in json_content  and all('weight' in link for link in json_content['links']):  #all()用于检查给定的迭代器中的元素是否都为True。这种情况下，它检查links中的每个元素是否都包含'weight'键
       json_type = 'json1'

    else:
        user_difined_weight = get_user_input('json2')
        for link in json_content['links']:
            link['weight']=user_difined_weight
        json_type = "json2"
        

    layout_choice = get_user_input(json_type, tag_json_layout=True)
    updated_json = apply_layout_to_json(json_content,layout_choice)

    return updated_json

def determine_csv_type(df,csv_path):
    if df[2].nunique() == 1:
        return get_user_input('csv1',csv_path)
    else:
        return get_user_input('csv2',csv_path)

def get_user_input(file_type,csv_path=None,tag_json_layout=False):
    layout_option = {
            0:"no layout", 
            1:'circular_layout',
            2:'random_layout',
            3:'shell_layout',
            4:'spring_layout',
            5:'spectral_layout',
        }
    
    if file_type =='json2' and tag_json_layout == False:
        while True:
            try:
                value = float(input("please enter a weight value between 0 and 1:"))
                if 0 <= value <=1:
                    return value   #需要对json2中添加字段weight,写个函数！
                else:
                    print('The value must be between 0 and 1.')
            except ValueError:
                print('Invalid input. Please enter a numeric value')
    
    elif file_type in('json1','json2') and tag_json_layout == True:
        print("Please choose a layout option for  graph:")
        for key, value in layout_option.items():
                print(f"Enter {key} for {value}")
        try:
            choice=int(input('Your choice: '))
            if choice in layout_option:
                return layout_option[choice]
            else:
                print('Invalid choice. Please choose a valid option.')
        except ValueError:
            print('Invalid input. Please enter a numeric value.')

    elif file_type in('csv1','csv2') and csv_path is not None:
        
        while True:
            print("Please choose a layout option:")
            for key, value in layout_option.items():
                print(f"Enter {key} for {value}")
            try:
                choice = int(input('Your choice: '))
                if choice in layout_option:
                    return convert_csv_to_json_graph(csv_path,layout_option[choice])
                else:
                    print('Invalid choice. Please choose a valid option.')
            except ValueError:
                print('Invalid input. Please enter a numeric value.')
def get_user_edge_width():
    while True:
        try:
            #prmpt the user for input
            line_width = float(input("Please enter the desired line width (e.g., 0.5, 1, 1.5):"))

            #check if the line width is within an acceptable range
            if 0< line_width <=10:
                return line_width
            else:
                print("Line width should be between 0 and 10.")

        except ValueError:
            print("Invalid input. Please enter a numeraical value.")

def convert_csv_to_json_graph(csv_file_path,layout_option):
    df = pd.read_csv(csv_file_path,encoding = 'utf-8',header = None)

    df.columns = ['source','target','weight']
    G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')
     

    layout_func=getattr(nx, layout_option, nx.spring_layout)  
    nodesPos=layout_func(G)

    nodes=[{"name":str(n), "pos":{"x":float(pos[0]), 'y':float(pos[1])}} for n, pos in nodesPos.items()]
    edges=[{"source":str(int(row['source'])), "target":str(int(row['target'])), 'weight':float(row['weight'])} for index, row in df.iterrows()]
    graph_json={"nodes":nodes, 'links':edges}

    return graph_json

def apply_layout_to_json(json_content,layout_option):
    """
    Apply a specified layout algorithm to the JSON graph and update node positions.

    Parameters:
    json_content (dict): The graph in JSON format.
    layout_option (str): The name of the layout algorithm to apply.

    Returns:
    dict: Updated JSON content with new node positions.
    """
    if layout_option == 'no layout':
        return json_content

    G = nx.Graph()
    for node in json_content['nodes']:
        G.add_node(node["name"])
    for link in json_content['links']:
        G.add_edge(link['source'], link['target'])
    layout_func = getattr(nx, layout_option, nx.spring_layout)

    nodes_position = layout_func(G)

    for node in json_content["nodes"]:
        node['pos']['x'], node['pos']['y'] = nodes_position[node["name"]]
    return json_content


def readdata(graph_path,canvas_height, canvas_width):
    layout_graph_json = determine_file_type(graph_path)
    links_weight = [link['weight'] for link in layout_graph_json['links']]  

    scaled_layout_graph_data = scale_positions_with_padding(layout_graph_json,canvas_height,canvas_width,40,30)


    all_nodes = scaled_layout_graph_data['nodes']
    all_links = scaled_layout_graph_data['links']

    source_pos_new, target_pos_new = get_source_target_positions(all_links,all_nodes)

    nodes_scaled_position = extract_node_positions(all_nodes)
    
    return {
        "source":source_pos_new,
        "target":target_pos_new,
        "links_weight":links_weight,
        "nodes_scaled_position":nodes_scaled_position
    }

#extract_node_positions暂时并未使用，aa_drawspike.py中是用来绘制Thckiness的
def extract_node_positions(nodes):
    nodes_position = []

    for node in nodes:
        nodes_position.append(node['pos'])
    
    return nodes_position

def get_source_target_positions(links,nodes):
    source_positions = []
    target_positions = []

    for link in links:

        source_name = link['source']
        target_name = link['target']
        source_node = next(node for node in nodes if node['name'] == source_name)
        target_node = next(node for node in nodes if node['name'] == target_name)
        source_positions.append(source_node['pos'])
        target_positions.append(target_node['pos'])

    return source_positions, target_positions

def scale_positions_with_padding(layout_graph_json,canvas_width,canvas_height,x_padding, y_padding):
    """
    Scale positions of points to fit within a canvas while maintainning aspect ratio and padding

    Parameters:
    all_pos(list): List of dictionaries, each containing 'x' and 'y' coordinates of a point.
    canvas_width(int): Width of the canvas.
    canvas_height(int): Height of the canvas.
    x_padding(int): Padding on the left and right sides of the canvas.

    Returns:
    list: List of scaled positions with padding applied.
    """
    #calculate the actual plot area considering padding
    plot_width = canvas_width- 2 * x_padding
    plot_height = canvas_height- 2 * y_padding

    #Find the range of existing positions
    node_list=layout_graph_json['nodes']
    min_x = min(node['pos']['x'] for node in node_list)
    max_x = max(node['pos']['x'] for node in node_list)
    min_y = min(node['pos']['y'] for node in node_list)
    max_y = max(node['pos']['y'] for node in node_list)

    #Calculate scaling factors
    x_scale = plot_width/(max_x-min_x)
    y_scale = plot_height/(max_y-min_y)
    scale=min(x_scale, y_scale)

    #Applying scaling and translation to fit within the canvas
    for node in layout_graph_json['nodes']:
        node['pos']['x'] = (node['pos']['x'] - min_x) * scale + x_padding
        node['pos']['y'] = (node['pos']['y'] - min_y) * scale + y_padding
    
    return layout_graph_json
def  gen_sticky(drawStyle,ss,source_pos_new,target_pos_new,SOURCE_RADIUS,TARGET_RADIUS):
    """
    Generate sticky link visualization parameters based on input parameters.

    This function calculates and returns visualization parameters for sticky links
    based on the given drawing style, weight (ss), source and target node positions,
    and other parameters.

    Parameters:
    drawStyle (str): The drawing style, e.g., 'stickiness'.
    ss (float): weight value.
    source_pos_new (dict): Dictionary containing the position of the source node.
    target_pos_new (dict): Dictionary containing the position of the target node.
    SOURCE_RADIUS (float): Radius of the source node.
    TARGET_RADIUS (float): Radius of the target node.

    Returns:
    dict: Dictionary containing the visualization parameters, including positions and handles.
    """
     
    distance_st = []
    angle1s_radian = []

    dy = target_pos_new['y'] - source_pos_new['y']
    dx = target_pos_new['x'] - source_pos_new['x']

    dxy = math.sqrt(pow(dx, 2) + pow(dy, 2))
    distance_st.append(dxy)
    if dx == 0:
        angle1_some = math.pi
    else:
        angle1_some = math.atan2(dy, dx)
            
    angle1s_radian.append(angle1_some)

    anchors = get_control_point(source_pos_new, target_pos_new, ss, SOURCE_RADIUS, TARGET_RADIUS, angle1s_radian)

    p1a = anchors['p1a']
    p1b = anchors['p1b']
    p2a = anchors['p2a']
    p2b = anchors['p2b']
   
    p1c = copy.deepcopy(source_pos_new)
    L1 = SOURCE_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * ss
    p1c['x'] = L1 * math.cos(angle1s_radian[0]) + p1c["x"]
    p1c['y'] = L1 * math.sin(angle1s_radian[0]) + p1c['y']

    p2c = copy.deepcopy(target_pos_new)
    L2 = TARGET_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * ss
    p2c['x'] = L2 * math.cos(angle1s_radian[0] + math.pi) + p2c["x"]
    p2c['y'] = L2 * math.sin(angle1s_radian[0] + math.pi) + p2c['y']
    delta = 0.8

    #stickeness<0.5，two spikes
    if ss <= 0.5:
        #spike for source
         if drawStyle == 'stickiness':

            thirdpos_source = copy.deepcopy(p1c)

            handlepos1 = copy.deepcopy(source_pos_new)
            L3 = SOURCE_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * ss * 0.1
            handlepos1['x'] = L3 * math.cos(angle1s_radian[0]) + handlepos1["x"]
            handlepos1['y'] = L3 * math.sin(angle1s_radian[0]) + handlepos1['y']


            p1a_handleIn = copy.deepcopy(p1a)
            p1a_handleIn[0]['x'] = p1a_handleIn[0]['x'] + (handlepos1['x'] - p1a[0]['x']) * delta
            p1a_handleIn[0]['y'] = p1a_handleIn[0]['y'] + (handlepos1['y'] - p1a[0]['y']) * delta

            p1b_handleOut = copy.deepcopy(p1b)
            p1b_handleOut[0]['x'] = p1b_handleOut[0]['x'] + (handlepos1['x'] - p1b[0]['x']) * delta
            p1b_handleOut[0]['y'] = p1b_handleOut[0]['y'] + (handlepos1['y'] - p1b[0]['y']) * delta

            #spikes_target

            thirdpos_target=copy.deepcopy(p2c)

            handlepos2=copy.deepcopy(target_pos_new)
            L4 = TARGET_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * ss * 0.1
            handlepos2['x'] = handlepos2['x'] + L4 * math.cos(angle1s_radian[0] + math.pi)
            handlepos2['y'] = handlepos2['y'] + L4 * math.sin(angle1s_radian[0] + math.pi)


            p2a_handleIn = copy.deepcopy(p2a)
            p2a_handleIn[0]['x'] = p2a_handleIn[0]['x'] + (handlepos2['x'] - p2a[0]['x']) * delta
            p2a_handleIn[0]['y'] = p2a_handleIn[0]['y'] + (handlepos2['y'] - p2a[0]['y']) * delta

            p2b_handleOut = copy.deepcopy(p2b)
            p2b_handleOut[0]['x'] = p2b_handleOut[0]['x'] + (handlepos2['x'] - p2b[0]['x']) * delta
            p2b_handleOut[0]['y'] = p2b_handleOut[0]['y'] + (handlepos2['y'] - p2b[0]['y']) * delta

            
            return{
                'thirdpos_source': thirdpos_source,
                'thirdpos_target': thirdpos_target,
                'p1a_handleIn': p1a_handleIn,
                'p1b_handleOut': p1b_handleOut,
                'p2a_handleIn': p2a_handleIn,
                'p2b_handleOut': p2b_handleOut,
                'angle1s_radian': angle1s_radian
            }
    else:

        thirdpos1_max = copy.deepcopy(p1a)
        thirdpos1_max = thirdpos1_max[0]
        thirdpos1_max['x'] = (thirdpos1_max['x'] + p2a[0]['x']) * 0.5
        thirdpos1_max['y'] = (thirdpos1_max['y'] + p2a[0]['y']) * 0.5

        thirdpos1_min = copy.deepcopy(source_pos_new)
        L5 = SOURCE_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * 0.5
        thirdpos1_min['x'] = thirdpos1_min['x'] + L5 * math.cos(angle1s_radian[0])
        thirdpos1_min['y'] = thirdpos1_min['y'] + L5 * math.sin(angle1s_radian[0])

        thirdpos1 = [interpolate_vector(thirdpos1_min, thirdpos1_max, (ss - 0.5) / 0.5)]


        thirdpos2_max = copy.deepcopy(p1b)
        thirdpos2_max = thirdpos2_max[0]

        thirdpos2_max['x'] = (thirdpos2_max['x'] + p2b[0]['x']) * 0.5
        thirdpos2_max['y'] = (thirdpos2_max['y'] + p2b[0]['y']) * 0.5


        thirdpos2_min = copy.deepcopy(target_pos_new)
        L6 = TARGET_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * 0.5
        thirdpos2_min['x'] = L6 * math.cos(angle1s_radian[0] + math.pi) + thirdpos2_min['x']
        thirdpos2_min['y'] = L6 * math.sin(angle1s_radian[0] + math.pi) + thirdpos2_min['y']

        thirdpos2 = [interpolate_vector(thirdpos2_min, thirdpos2_max, (ss - 0.5) / 0.5)]

        interR=math.pow((ss - 0.5)/0.5, 3)
        midpos1_base, midpos2_base=[], []
        midpos1_base = copy.deepcopy(source_pos_new)
        midpos2_base = copy.deepcopy(target_pos_new)
        v_length1, v_length2, v_length3, v_length4 = [], [], [], []

        L7 = SOURCE_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * 0.5 * 0.1
        midpos1_base['x'] = midpos1_base['x'] + L7 * math.cos(angle1s_radian[0])
        midpos1_base['y'] = midpos1_base['y'] + L7 * math.sin(angle1s_radian[0])    

        dist1 = get_vector_length(midpos1_base, p1a[0])
        v_length1.append(dist1)
        dist2 = get_vector_length(midpos1_base, p1b[0])
        v_length2.append(dist2)


        L8 = TARGET_RADIUS + (distance_st[0] - (SOURCE_RADIUS + TARGET_RADIUS)) * 0.5 * 0.1
        midpos2_base['x'] += L8 * math.cos(angle1s_radian[0] - math.pi)
        midpos2_base['y'] += L8 * math.sin(angle1s_radian[0] - math.pi)

        dist3 = get_vector_length(midpos2_base, p2a[0])
        v_length3.append(dist3)
        dist4 = get_vector_length(midpos2_base, p2b[0])
        v_length4.append(dist4)

        # Interpolate positions
        h0 = interpolate_vector_scale(p1a[0], midpos1_base, p2a[0], interR, v_length1)
        h3 = interpolate_vector_scale(p1b[0], midpos1_base, p2b[0], interR, v_length2)
        h1 = interpolate_vector_scale(p2a[0], midpos2_base, p1a[0], interR, v_length3)
        h2 = interpolate_vector_scale(p2b[0], midpos2_base, p1b[0], interR, v_length4)

        # Handle positions adjustments
        p1a_handleOut = copy.deepcopy(h0)
        p1a_handleOut[0]['x'] = p1a_handleOut[0]['x'] * delta
        p1a_handleOut[0]['y'] = p1a_handleOut[0]['y'] * delta

        p2a_handleIn=copy.deepcopy(h1)
        p2a_handleIn[0]['x'] = p2a_handleIn[0]['x']*delta
        p2a_handleIn[0]['y'] = p2a_handleIn[0]['y']*delta
   
        p2b_handleOut=copy.deepcopy(h2)
        p2b_handleOut[0]['x'] = p2b_handleOut[0]['x']*delta
        p2b_handleOut[0]['y'] = p2b_handleOut[0]['y']*delta


        p1b_handleIn=copy.deepcopy(h3)
        p1b_handleIn[0]['x'] = p1b_handleIn[0]['x']*delta
        p1b_handleIn[0]['y'] = p1b_handleIn[0]['y']*delta

        return {
            'thirdpos_source': thirdpos1,
            'thirdpos_target': thirdpos2,
            'p1a_handleIn': p1a_handleOut,
            'p2a_handleIn': p2a_handleIn,
            'p2b_handleOut': p2b_handleOut,
            'p1b_handleOut': p1b_handleIn,
            'angle1s_radian': angle1s_radian
        }


def get_control_point(ball1_pos,ball2_pos,stickiness,SOURCE_RADIUS,TARGET_RADIUS,angle1s_radian):
    """
    Calculate anchor points for sticky link visualization based on input parameters.

    This function computes anchor points for a sticky link visualization, taking into account
    various factors such as stickiness, node radii, and interpolation.

    Parameters:
    ball1_pos (dict): Dictionary containing the position of the source node.
    ball2_pos (dict): Dictionary containing the position of the target node.
    stickiness (float): Stickiness factor influencing the angle difference.
    SOURCE_RADIUS (float): Radius of the source node.
    TARGET_RADIUS (float): Radius of the target node.
    angle1s_

    Returns:
    dict: Dictionary containing anchor points for the sticky link visualization.
    """
    max_ang_dif = math.pi*0.35
    min_ang_dif = math.pi*0.05
    angle_dif= min_ang_dif+(max_ang_dif - min_ang_dif)*stickiness

    angle1a = [angle1s_radian[0] + angle_dif]

    angle1b = [angle1s_radian[0] - angle_dif]

    angle2a = [angle1s_radian[0] + math.pi - angle_dif]

    angle2b = [angle1s_radian[0] - math.pi + angle_dif]



    p1a = [{'x': SOURCE_RADIUS * math.cos(angle1a[0]) + ball1_pos['x'],
            'y': SOURCE_RADIUS * math.sin(angle1a[0]) + ball1_pos['y']}]


    p1b = [{'x': SOURCE_RADIUS * math.cos(angle1b[0]) + ball1_pos['x'],
        'y': SOURCE_RADIUS * math.sin(angle1b[0]) + ball1_pos['y']}]


    p2a = [{'x': TARGET_RADIUS * math.cos(angle2a[0]) + ball2_pos['x'],
        'y': TARGET_RADIUS * math.sin(angle2a[0]) + ball2_pos['y']}]

    p2b = [{'x': TARGET_RADIUS * math.cos(angle2b[0]) + ball2_pos['x'],
        'y': TARGET_RADIUS * math.sin(angle2b[0]) + ball2_pos['y']}]
        

    return {
		'p1a': p1a,
		'p1b': p1b,
		'p2a': p2a,
		'p2b': p2b
	}


def interpolate_vector(v1,v2,ratio):
    """
    Interpolate a vector between two vectors based on a given ratio.

    Parameters:
    - v1 (dict): Dictionary representing the first vector.
    - v2 (dict): Dictionary representing the second vector.
    - ratio (float): Interpolation ratio between the two vectors.

    Returns:
    dict: A dictionary representing the interpolated vector.
    """

    return {'x': v1['x'] + ratio * (v2['x'] - v1['x']), 'y': v1['y'] + ratio * (v2['y'] - v1['y'])}
    
def get_vector_length(point1, point2):
    return math.sqrt((point1['x'] - point2['x']) ** 2+(point1['y'] - point2['y']) ** 2)
def interpolate_vector_scale(center_point, from_point, to_point, ratio, radius):
    """
    Interpolate and scale a vector between two points based on a given ratio and radius.

    Parameters:
    - center_point (dict): Dictionary containing the coordinates of the center point.
    - from_point (dict): Dictionary containing the coordinates of the starting point.
    - to_point (dict): Dictionary containing the coordinates of the ending point.
    - ratio (float): Interpolation ratio between the two vectors.
    - radius (list): List containing the radius information.

    Returns:
    list: A list containing a dictionary representing the scaled interpolated vector.
    """
    result = []

    v1 = {'x': from_point['x'] - center_point['x'], 'y': from_point['y'] - center_point['y']}
    v2 = {'x': to_point['x'] - center_point['x'], 'y': to_point['y'] - center_point['y']}
    interpolated_vector = interpolate_vector(v1, v2, ratio)
    r_t = radius[0] / math.sqrt(interpolated_vector['x'] ** 2 + interpolated_vector['y'] ** 2)

    scaled_vector = {'x': interpolated_vector['x'] * r_t, 'y': interpolated_vector['y'] * r_t}
    result.append(scaled_vector)
    return result

def set_line_width(ss, edge_width):
    # Check if edge_width is less than 1
    if edge_width < 1:
        return max(edge_width, 0.1)  # Set to the minimum positive width (or edge_width if it's already positive)

    if 0 < ss <= 0.1:
        width = edge_width - 0.9
    elif 0.1 < ss <= 0.2:
        width = edge_width - 0.8
    elif 0.2 < ss <= 0.3:
        width = edge_width - 0.7
    elif 0.3 < ss <= 0.4:
        width = edge_width - 0.6
    elif 0.4 < ss <= 0.5:
        width = edge_width - 0.5
    elif 0.5 < ss <= 0.6:
        width = edge_width - 0.4
    elif 0.6 < ss <= 0.7:
        width = edge_width - 0.3
    elif 0.7 < ss <= 0.8:
        width = edge_width - 0.2
    elif 0.8 < ss <= 0.9:
        width = edge_width - 0.1
    else:
        width = edge_width

    return width


def draw_stickiness_edge(stickiness, pab, thirds,line_width,context):
    """
    Draw stickiness curves on the given Cairo context.

    Parameters:
    - stickiness (float): weight value.
    - pab (dict): Dictionary containing anchor points for drawing.
    - thirds (dict): Dictionary containing third positions and handles for drawing.
    - context (cairo.Context): Cairo canvas for drawing.

    Returns:
    None
    """
    p1a_x,p1a_y=[],[]
    p1b_x,p1b_y=[],[]
    p2a_x,p2a_y=[],[]
    p2b_x,p2b_y=[],[]

    for item in pab:
        if item == 'p1a':
            p1a_x.append(pab[item][0]['x'])
            p1a_y.append(pab[item][0]['y'])
        elif item=='p1b':
            p1b_x.append(pab[item][0]['x'])
            p1b_y.append(pab[item][0]['y'])
        elif item=='p2a' :
            p2a_x.append(pab[item][0]['x'])
            p2a_y.append(pab[item][0]['y'])
        elif item=='p2b':
            p2b_x.append(pab[item][0]['x'])
            p2b_y.append(pab[item][0]['y'])

    if stickiness<=0.5:

        for item in thirds:
            for i in thirds[item]:
                if(item =='thirdpos_source'):
                    thirdpos_source=copy.deepcopy(thirds[item])
                elif(item =='thirdpos_target'):
                    thirdpos_target=copy.deepcopy(thirds[item])
                elif(item=='p1a_handleIn'):
                    p1a_handle=copy.deepcopy(thirds[item])
                elif(item=='p1b_handleOut'):
                    p1b_handle=copy.deepcopy(thirds[item])
                elif(item=='p2a_handleIn'):
                    p2a_handle=copy.deepcopy(thirds[item])
                else:
                    p2b_handle=copy.deepcopy(thirds[item])


        #draw curve
        context.set_line_width(line_width)
        context.set_source_rgb(0.5, 0.5, 0.5)

        context.curve_to(p1a_x[0],p1a_y[0],p1a_handle[0]['x'],p1a_handle[0]['y'],thirdpos_source['x'],thirdpos_source['y'])
        context.curve_to(thirdpos_source['x'],thirdpos_source['y'],p1b_handle[0]['x'],p1b_handle[0]['y'],p1b_x[0],p1b_y[0])
        context.set_line_cap(cairo.LINE_CAP_BUTT)
        context.fill()

        context.curve_to(p2a_x[0],p2a_y[0],p2a_handle[0]['x'],p2a_handle[0]['y'],thirdpos_target['x'],thirdpos_target['y'])
        context.curve_to(thirdpos_target['x'],thirdpos_target['y'],p2b_handle[0]['x'],p2b_handle[0]['y'],p2b_x[0],p2b_y[0])
        context.set_line_cap(cairo.LINE_CAP_BUTT)

        context.fill()

    else:

        p1a_handle=[]
        p1b_handle=[]
        thirdpos_source=[]
        thirdpos_target=[]
        p2a_handle=[]
        p2b_handle=[]

        for item in thirds:
            if item=='thirdpos1':
                thirdpos_source=thirds[item]
            if item=='thirdpos2':
                thirdpos_target=thirds[item]
            if item=='p1a_handleIn':
                p1a_handle=thirds[item]
            if item=='p2a_handleIn':
                p2a_handle=thirds[item]
            if item=='p2b_handleOut':
                p2b_handle=thirds[item]
            if item=='p1b_handleOut':
                p1b_handle=thirds[item]

        # Drawing Curve
        context.set_line_width(line_width)
        context.set_source_rgb(0.5, 0.5, 0.5)
 
        context.move_to(p1a_x[0],p1a_y[0])
        context.curve_to(p1a_x[0] + p1a_handle[0]['x'], p1a_y[0] + p1a_handle[0]['y'],
                                p2a_x[0]+p2a_handle[0]['x'],p2a_y[0]+p2a_handle[0]['y'],
                            p2a_x[0],p2a_y[0])
        context.line_to(p2b_x[0],p2b_y[0])
            
        context.curve_to(p2b_x[0] + p2b_handle[0]['x'], p2b_y[0] + p2b_handle[0]['y'],
                            p1b_x[0]+p1b_handle[0]['x'],p1b_y[0]+p1b_handle[0]['y'],
                            p1b_x[0],p1b_y[0])
        context.line_to(p1a_x[0],p1a_y[0])
        context.fill()

def draw_thickiness_edge(source_pos_new,target_pos_new,weight,edge_width, context):
    """
    Draw edges with varying thickness based on the provided weight.

    Parameters:
    - source_pos_new (list): List of dictionaries containing source node positions.
    - target_pos_new (list): List of dictionaries containing target node positions.
    - weight (float): Weight of the edges, influencing the thickness of edge.
    - context (cairo.Context): Cairo context(canvas) for drawing.

    Returns:
    None
    """

    context.set_source_rgb(0.5,0.5,0.5)

    width = set_line_width(weight,edge_width)
    context.set_line_width(width)
    #draw edges
    for source, target in zip(source_pos_new, target_pos_new):
        context.move_to(source['x'],source['y'])
        context.line_to(target['x'],target['y'])
        context.stroke()
    
def draw_nodes(context,all_pos_new,radius):

    for pos in all_pos_new:
        context.arc(pos['x'],pos['y'],radius,0,2 * math.pi)
        context.set_source_rgb(0,0,0)
        context.fill()

def gen_sticky_edge_properties(edge_style, weight, source_pos, target_pos, source_radius, target_radius):
    result_gen_sticky = gen_sticky(edge_style, weight, source_pos, target_pos,
                                           source_radius, target_radius)
    angle_st_radian = result_gen_sticky['angle1s_radian']
    thirds_handles = {
        'thirdpos_source': result_gen_sticky['thirdpos_source'],
        'thirdpos_target': result_gen_sticky['thirdpos_target'],
        'p1a_handleIn': result_gen_sticky['p1a_handleIn'],
        'p1b_handleOut': result_gen_sticky['p1b_handleOut'],
        'p2a_handleIn': result_gen_sticky['p2a_handleIn'],
        'p2b_handleOut': result_gen_sticky['p2b_handleOut']
        }

 
    pab = get_control_point(source_pos, target_pos, weight, source_radius, target_radius,
                              angle_st_radian)
    return  thirds_handles, pab
                    
    
def draw_graph(edge_style,file_path,nodes_radius,edge_width,canvas_width,canvas_height):
    """
    Draw a graph with specified edge style, file path, nodes radius, canvas size, and spike style.

    Parameters:
    - edge_style (str): Style of the edges ('thickiness' or 'stickiness').
    - file_path (str): Path to the data file.
    - nodes_radius (float): Expected radius of nodes.
    - canvas_width (int): Width of the canvas.
    - canvas_height (int): Height of the canvas.
  
    Returns:
    None
    """

    st_positions=readdata(file_path, canvas_height, canvas_width)
    source_pos_new = st_positions['source']
    target_pos_new = st_positions["target"]
    stickiness_lst = st_positions['links_weight']
    nodes_pos_scaled=st_positions['nodes_scaled_position']
    source_radius=nodes_radius
    target_radius=nodes_radius

    #draw result save as svg
    #draw edges
    with cairo.SVGSurface('graph.svg',canvas_height,canvas_width) as surface:
            context = cairo.Context(surface)

            #draw edges: stickiness or thickiness
            for i, weight in enumerate(stickiness_lst):

                if edge_style == 'thickiness':
                    draw_thickiness_edge(source_pos_new, target_pos_new, weight,edge_width, context)

                else:
                    thirds_handles, pab=gen_sticky_edge_properties( 
                    edge_style, weight, source_pos_new[i], target_pos_new[i],
                    source_radius, target_radius)
 
                    draw_stickiness_edge(weight, pab, thirds_handles, edge_width, context)


            #draw nodes
            draw_nodes(context, nodes_pos_scaled, nodes_radius)
    
    #draw result save as png
    with cairo.ImageSurface(cairo.FORMAT_ARGB32,canvas_height,canvas_width) as surface:
            context = cairo.Context(surface)

            #draw edges: stickiness or thickiness
            for i, weight in enumerate(stickiness_lst):

                if edge_style == 'thickiness':
                    draw_thickiness_edge(source_pos_new, target_pos_new, weight,edge_width, context)

                else:
                    thirds_handles, pab=gen_sticky_edge_properties( 
                    edge_style, weight, source_pos_new[i], target_pos_new[i],
                    source_radius, target_radius)
 
                    draw_stickiness_edge(weight, pab, thirds_handles, edge_width, context)


            #draw nodes
            draw_nodes(context, nodes_pos_scaled, nodes_radius)     
            surface.write_to_png("graph.png")
