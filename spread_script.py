import maya.cmds as cmds
import math

# --- SETTINGS (Roll No. 19 Customization) ---
spread_speed = 1.9        # Roll Number 19: Controls how fast fire moves
spread_radius = 15.0      # How far the fire can jump between trees
max_frames = 300          # Animation length

def setup_forest_fire():
    # 1. GET ALL TREES
    # We look for anything named "Tree_*"
    trees = cmds.ls("Tree_*", type="transform")
    
    if not trees:
        print("Error: No trees found! Make sure they are named Tree_1, Tree_2, etc.")
        return

    print(f"Found {len(trees)} trees. Setting up fire engines...")

    # Dictionary to store data: {tree_name: [emitter_node, x, z]}
    forest_data = {}
    
    # 2. ADD EMITTERS TO ALL TREES (But turn them OFF)
    for tree in trees:
        # Create Emitter & Particle
        nparticle_nodes = cmds.nParticle(name=f"Fire_{tree}")
        particle_shape = nparticle_nodes[1]
        emitter_nodes = cmds.emitter(pos=(0, 0, 0), type="omni", r=100, spd=2)
        emitter_name = emitter_nodes[0]
        
        # Connect
        cmds.connectDynamic(nparticle_nodes[0], em=emitter_name)
        
        # Position & Parent
        pos = cmds.xform(tree, q=True, ws=True, t=True)
        cmds.move(pos[0], pos[1] + 3, pos[2], emitter_name)
        cmds.parent(emitter_name, tree)
        
        # APPLY VISUALS (The settings you liked)
        cmds.setAttr(particle_shape + ".radius", 2.0)
        cmds.setAttr(particle_shape + ".ignoreSolverGravity", 1)
        cmds.setAttr(particle_shape + ".lifespanMode", 2)
        cmds.setAttr(particle_shape + ".lifespan", 1.2)
        cmds.setAttr(particle_shape + ".particleRenderType", 7) # MultiStreak
        cmds.setAttr(particle_shape + ".colorInput", 0)
        cmds.setAttr(particle_shape + ".color[0].color_Color", 1, 0.45, 0, type="double3") # Orange

        # TURN IT OFF INITIALLY (Rate = 0)
        cmds.setAttr(emitter_name + ".rate", 0)
        
        # Store for logic calculation
        forest_data[tree] = [emitter_name, pos[0], pos[2]]

    # 3. CALCULATE THE SPREAD (The Logic)
    print("Calculating spread path...")
    
    # Queue: [ (TreeName, StartFrame) ]
    # We start with Tree_1 burning at Frame 1
    process_queue = [("Tree_1", 1)]
    visited = {"Tree_1": 1} # Keep track so we don't burn a tree twice

    # Process the queue until empty
    while len(process_queue) > 0:
        current_tree, current_time = process_queue.pop(0)
        
        # Get Current Tree's Data
        if current_tree not in forest_data: continue
        c_emitter, c_x, c_z = forest_data[current_tree]
        
        # KEYFRAME: Turn ON the fire at this time
        # Set rate to 0 just before
        cmds.setKeyframe(c_emitter, attribute="rate", t=current_time-1, v=0)
        # Set rate to 100 (ON) at the ignition time
        cmds.setKeyframe(c_emitter, attribute="rate", t=current_time, v=150)
        
        # FIND NEIGHBORS
        for neighbor in trees:
            if neighbor in visited: continue # Skip if already burning
            
            # Calculate Distance
            n_emitter, n_x, n_z = forest_data[neighbor]
            dist = math.sqrt((c_x - n_x)**2 + (c_z - n_z)**2)
            
            # If close enough, ignite it!
            if dist < spread_radius:
                # Logic: Time = CurrentTime + (Distance * SpeedFactor)
                ignition_delay = dist * spread_speed
                ignition_time = current_time + ignition_delay
                
                if ignition_time < max_frames:
                    visited[neighbor] = ignition_time
                    process_queue.append((neighbor, ignition_time))
                    
                    # Sort queue so earlier fires process first (Breadth-First)
                    process_queue.sort(key=lambda x: x[1])

    print("DONE! Fire spread simulation baked. Press PLAY.")

# Run it
setup_forest_fire()
