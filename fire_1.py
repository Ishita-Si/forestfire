import maya.cmds as cmds

def create_fire_on_tree(tree_name):
    # --- 1. Create Particles ---
    # nParticle returns [transform, shape]. We need the shape.
    nparticle_nodes = cmds.nParticle(name="Fire_Particles")
    particle_shape = nparticle_nodes[1] 
    
    # --- 2. Create Emitter (FIXED) ---
    # We grab index [0] because Maya returns ['emitter1']
    emitter_nodes = cmds.emitter(pos=(0, 0, 0), type="omni", r=100, spd=2)
    emitter_name = emitter_nodes[0] 
    
    # Connect them
    cmds.connectDynamic(nparticle_nodes[0], em=emitter_name)
    
    # --- 3. Move Emitter to Tree ---
    pos = cmds.xform(tree_name, q=True, ws=True, t=True)
    # Move up (Y+3) so it's not in the dirt
    cmds.move(pos[0], pos[1] + 3, pos[2], emitter_name)
    cmds.parent(emitter_name, tree_name)

    # --- 4. MAKE IT LOOK LIKE FIRE ---
    # Size
    cmds.setAttr(particle_shape + ".radius", 2.0) 
    # Ignore Gravity (Go Up)
    cmds.setAttr(particle_shape + ".ignoreSolverGravity", 1) 
    # Lifespan
    cmds.setAttr(particle_shape + ".lifespanMode", 2) # Random
    cmds.setAttr(particle_shape + ".lifespan", 1.5)
    cmds.setAttr(particle_shape + ".lifespanRandom", 0.5)
    # Render Type (MultiStreak)
    cmds.setAttr(particle_shape + ".particleRenderType", 7) 
    # Color (Force Orange)
    cmds.setAttr(particle_shape + ".colorInput", 0) 
    cmds.setAttr(particle_shape + ".color[0].color_Color", 1, 0.4, 0, type="double3")

    print(f"SUCCESS: Fire created on {tree_name}!")

# --- RUN IT ---
if cmds.objExists('Tree_1'):
    create_fire_on_tree('Tree_1')
else:
    print("Error: Could not find Tree_1")
