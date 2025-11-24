import maya.cmds as cmds
import random

# --- SETTINGS ---
terrain_name = 'pPlane2'      
tree_template = 'Tree_Template'
number_of_trees = 300
terrain_size = 100            

# check if objects exist
if not cmds.objExists(terrain_name):
    print(f"Error: Terrain '{terrain_name}' not found!")
elif not cmds.objExists(tree_template):
    print(f"Error: Template '{tree_template}' not found!")
else:
    # Clean up old trees if you ran this before (Optional safety)
    # cmds.delete(cmds.ls("Tree_*")) 
    
    for i in range(number_of_trees):
        # 1. Duplicate
        new_tree = cmds.duplicate(tree_template, name=f"Tree_{i+1}")[0]
        
        # 2. Random X and Z
        rand_x = random.uniform(-terrain_size/2.0, terrain_size/2.0)
        rand_z = random.uniform(-terrain_size/2.0, terrain_size/2.0)
        
        # 3. Move HIGH UP first (Sky Drop Technique)
        # We place it at Y=50 so it is definitely above the hills
        cmds.move(rand_x, 50, rand_z, new_tree)
        
        # 4. Snap to Ground (Geometry Constraint)
        # This forces the tree down until it hits the terrain geometry
        try:
            constraint = cmds.geometryConstraint(terrain_name, new_tree)[0]
            cmds.delete(constraint) # Remove the constraint immediately
        except:
            print(f"Warning: Tree {i} missed the terrain.")

        # 5. Random Rotation
        rand_rot = random.uniform(0, 360)
        cmds.rotate(0, rand_rot, 0, new_tree)
        
        # 6. BIG AND SMALL VARIATION
        # 0.5 is half size, 2.5 is double-and-a-half size
        rand_scale = random.uniform(0.5, 2.5) 
        cmds.scale(rand_scale, rand_scale, rand_scale, new_tree)

    # Hide template
    cmds.hide(tree_template)
    print("Forest planted! Big and small trees created.")
