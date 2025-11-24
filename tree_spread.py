import maya.cmds as cmds
import random

# Settings
number_of_trees = 300
terrain_size = 100

# 1. Find the template tree
# We check if it exists to avoid errors
if not cmds.objExists('Tree_Template'):
    print("Error: Could not find 'Tree_Template'. Please rename your tree.")
else:
    # 2. Loop 300 times
    for i in range(number_of_trees):
        # Duplicate the template. returns a list, so we take [0]
        new_tree = cmds.duplicate('Tree_Template', name=f"Tree_{i+1}")[0]
        
        # Random Position
        rand_x = random.uniform(-terrain_size/2, terrain_size/2)
        rand_z = random.uniform(-terrain_size/2, terrain_size/2)
        
        # Move
        cmds.move(rand_x, 0, rand_z, new_tree)
        
        # Random Rotation (Y-axis)
        rand_rot = random.uniform(0, 360)
        cmds.rotate(0, rand_rot, 0, new_tree)
        
        # Random Scale
        rand_scale = random.uniform(0.8, 1.2)
        cmds.scale(rand_scale, rand_scale, rand_scale, new_tree)

    # 3. Hide the original template
    cmds.hide('Tree_Template')
    print("Forest Created Successfully with maya.cmds!")
