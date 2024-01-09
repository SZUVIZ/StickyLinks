from NodeStickyLinks import drawsticky


def run():
    """
    Run a program to interactively collect user inputs and draw a graph based on specified parameters.

    Returns:
    None
    """
    print("hello, run_drawsticky.py")
    ## Collect user input for the desired link style (stickiness or thickiness)
    while True:
        my_drawStyle = input('\033[1;34mPlease input your ideal link style including stickiness and thickiness:\033[0m')
        if my_drawStyle not in ['stickiness', 'thickiness']:
            print('Invalid input, please input again.')
        else:
            break

    path = input(' \033[1;93mPlease give me the data path:\033[0m')
    canvas_height = int(float(input(' \033[1;93mPlease set the height and width for canvas:\033[0m')))
    canvas_width = canvas_height
 
    nodes_radius = float(input(' \033[1;93mPlease input your expected nodes radius:\033[0m'))
    edge_width = drawsticky.get_user_edge_width()

    drawsticky.draw_graph(my_drawStyle, path, nodes_radius, edge_width, canvas_width, canvas_height)

if __name__ == '__main__':
    run()