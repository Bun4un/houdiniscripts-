import hou 
selected_nodes = hou.selectedNodes() 
root_dir = hou.node('/obj/')
if not selected_nodes:
        print('Not found selected nodes')
else: 
        for current_node in selected_nodes:
                node = root_dir.createNode('geo')
                merger = node.createNode('object_merge')
                merger.parm('objpath1').set(current_node.path())      
                
