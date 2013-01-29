
def position_slides(tree):
    """Position the slides in the tree"""
    
    # For now, just put them side by side
    for count, step in enumerate(tree.findall('step')):
        step.attrib['data-y'] = str(0)
        step.attrib['data-x'] = str(1600*count)
    return tree
        
