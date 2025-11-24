# Visualizing a Forest Fire Spread with Dynamic Particle Effects in Maya

**Course:** Graphics and Visual Computing (GVC)
**Submission Type:** Individual
**Roll Number:** 19
**Tools Used:** Autodesk Maya 2024/2025, Python (`maya.cmds`), nParticles

---

## 1. Project Objective
The primary objective of this project is to create a realistic, dynamic simulation of a forest fire spreading across a terrain. The project demonstrates proficiency in the GVC modeling pipeline, procedural scripting, viewing transformations, and particle dynamics. The simulation visualizes how fire propagates from a single ignition point to neighboring trees based on proximity logic.

## 2. Methodology

The project was implemented in three distinct phases:

### Phase 1: Modeling & Scene Setup
* **Terrain:** Created a `pPlane` with $100 \times 100$ dimensions. Applied a **Sine Deformer** (Wave) to create organic hills and valleys, simulating a natural forest floor.
* **Vegetation (Trees):** Modeled a low-poly tree using a Cylinder (trunk) and Cone (canopy).
* **Procedural Generation:** Instead of manual placement, a **Python script** was written to generate **300 trees**. The script utilized a `closestPointOnMesh` node to mathematically calculate the terrain height at random $X, Z$ coordinates, ensuring every tree snapped perfectly to the undulating ground surface. Size variation ($0.5x$ to $2.5x$) was applied for realism.

### Phase 2: Particle Simulation (The Visuals)
* **Fire System:** Utilized Maya **nParticles** emitting from the tree geometry.
* **Attributes:**
    * **Render Type:** `MultiStreak` to simulate flames.
    * **Color:** Ramp from bright yellow to red/orange.
    * **Physics:** `IgnoreSolverGravity` enabled to allow fire to rise naturally; `Lifespan` set to random range ($1.5s$) for flickering effects.
* **Optimization:** Emitters were parented to individual trees but kept inactive (Rate = 0) until triggered by the logic script.

### Phase 3: Dynamic Spread Logic (The Script)
* A custom Python algorithm was implemented to handle the spread logic.
* **Ignition:** The simulation begins at `Tree_1`.
* **Propagation:** The script calculates the Euclidean distance between the burning tree and all other trees.
* **Timeline:** If a neighbor is within the **Spread Radius**, the script calculates a specific frame number for ignition based on distance and a **Spread Speed** factor.
* **Animation:** `setKeyframe` commands were used to automate the Emitter Rate from 0 to 150 at the calculated specific frames.

---

## 3. Roll Number Customization
As per **Guideline 2**, my Roll Number (**19**) was used to customize the simulation parameters:

* **Spread Speed Factor:** Set to **1.9** (derived from 19). This value controls the delay calculation, dictating how fast the fire "jumps" from one tree to another.
* **Initial Conditions:** The simulation is initialized focusing on the 1st and 9th quadrants of the logic check (Ignition starts at `Tree_1`).

---

## 4. How to Run the Project
1.  Open the Maya Scene file (`.mb`).
2.  Open the **Script Editor** (Windows > General Editors > Script Editor).
3.  Load the attached Python script (see below) into the Python tab.
4.  Ensure the Timeline is set to **300 frames**.
5.  Press **Play** on the script to bake the simulation keyframes.
6.  Press **Play** on the Maya timeline to view the result.

---

## 5. Code Snapshot
*Below is the core logic used to calculate distances and bake the spread animation.*

```python
import maya.cmds as cmds
import math

# Custom Parameters (Roll No: 19)
spread_speed = 1.9        
spread_radius = 15.0     

def setup_forest_fire():
    # Identify all trees
    trees = cmds.ls("Tree_*", type="transform")
    forest_data = {}

    # Initialize Emitters
    for tree in trees:
        # (Emitter creation code omitted for brevity...)
        # Store emitter and position data
        pos = cmds.xform(tree, q=True, ws=True, t=True)
        forest_data[tree] = [emitter_name, pos[0], pos[2]]

    # Spread Logic (Breadth-First Search approach)
    process_queue = [("Tree_1", 1)]
    visited = {"Tree_1": 1}

    while len(process_queue) > 0:
        current_tree, current_time = process_queue.pop(0)
        c_emitter, c_x, c_z = forest_data[current_tree]
        
        # Keyframe Ignition
        cmds.setKeyframe(c_emitter, attribute="rate", t=current_time-1, v=0)
        cmds.setKeyframe(c_emitter, attribute="rate", t=current_time, v=150)
        
        # Check Neighbors
        for neighbor in trees:
            if neighbor in visited: continue
            
            n_emitter, n_x, n_z = forest_data[neighbor]
            dist = math.sqrt((c_x - n_x)**2 + (c_z - n_z)**2)
            
            if dist < spread_radius:
                ignition_delay = dist * spread_speed
                ignition_time = current_time + ignition_delay
                visited[neighbor] = ignition_time
                process_queue.append((neighbor, ignition_time))

setup_forest_fire()
