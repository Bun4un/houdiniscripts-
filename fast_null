import hou

selected_node = hou.selectedNodes() 
if not selected_node:
        print('Not found selected nodes')
else: 
        for current_node in selected_node:
                null = current_node.createOutputNode('null')
                null.setName(f"OUT_{current_node.name()}")
