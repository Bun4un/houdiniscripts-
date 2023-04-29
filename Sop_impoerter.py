import hou 

selected_nodes = hou.selectedNodes() 
root_dir = hou.node('/stage/')
once_create = False

if not selected_nodes:
    print('Not found selected nodes')
else:
    x, y = 0, 0  
    for current_node in selected_nodes:
        if current_node.type().name() == 'geo':
            sopimport_node = root_dir.createNode('sopimport')
            sopimport_node.parm('soppath').set(current_node.path())
            sopimport_node.setName(current_node.name())
            sopimport_node.setPosition((x, y))
            
            y -= 1.5

            matlib_node = root_dir.createNode('materiallibrary')
            matlib_node.parm('assign1').set(True)
            matlib_node.setName(f"{current_node.name()}_material")
            matlib_node.setPosition((x, y - 1.5))
            matlib_node.setInput(0, sopimport_node)
            
            y += 1.5
            x -= 1.5

        elif current_node.type().name() == 'cam' and not once_create:
            sceneimport_node = root_dir.createNode('sceneimport::2.0')
            sceneimport_node.setName('cameras')
            sceneimport_node.setPosition((x, y))  
            x -= 1.5
            once_create = True
