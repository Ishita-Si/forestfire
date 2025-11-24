# Visualizing a Forest Fire Spread with Dynamic Particle Effects in Maya

* **Project Title:** Dynamic Forest Fire Simulation 
* **Course:** Graphics and Visual Computing (GVC)
* **Roll Number:** 24cs2019
* **Submission Date:** November 2025

---

## 🛠 Toolchain & Technologies
* **Primary Software:** Autodesk Maya 2026
* **Scripting Language:** Python (using `maya.cmds` library)
* **Simulation Engine:** Maya nParticles (Nucleus Solver)
* **Rendering:** Viewport 2.0 / Hardware Renderer
* **OS:** Windows

---

## 🎯 Project Objective
The primary objective of this project is to simulate a natural disaster scenario—specifically a forest fire spread—to demonstrate proficiency in core Graphics and Visual Computing (GVC) concepts.

The project highlights the following technical competencies:
1.  **Modeling Pipeline:** creating organic terrain and low-poly vegetation assets.
2.  **Procedural Generation:** using Python scripting to scatter vegetation mathematically across an uneven surface.
3.  **Particle Dynamics:** implementing physics-based fire simulation using nParticles.
4.  **Event-Driven Animation:** programming a logic system where the visual state of an object changes based on proximity triggers (fire spreading logic).

---

## ⚙️ Methodology

The project was executed in three distinct technical phases:

### Phase 1: Environment Modeling & Procedural Scattering
* **Terrain:** A $100 \times 100$ unit `pPlane` was deformed using a **Non-linear Sine Deformer** to create undulating hills and valleys, simulating a natural forest floor.
* **Assets:** A low-poly tree was modeled using primitive shapes (Cylinder for trunk, Cone for canopy) to optimize performance for a scene with 200+ objects.
* **Scattering Logic:** A custom Python script was written to duplicate the tree 200 times. A `closestPointOnMesh` node was utilized to calculate the exact $Y$-height of the terrain at random $X/Z$ coordinates, ensuring trees adhered perfectly to the geometry. Scale variation ($0.5x$ - $2.5x$) was applied using `random.uniform`.

### Phase 2: Particle Simulation Setup
* **Visual Style:** Maya **nParticles** were used with the **MultiStreak** render type to simulate the volume and chaos of flames.
* **Shading:** A color ramp transitioning from **Incandescent Yellow** to **Orange/Red** was applied.
* **Physics:** Gravity was ignored (`ignoreSolverGravity = 1`) to allow the flames to rise naturally. A random lifespan ($1.2s - 1.5s$) was set to create a flickering effect.

### Phase 3: Dynamic Spread Algorithm (Roll No. 19 Customization)
* **Spread Logic:** A Breadth-First Search (BFS) style algorithm was implemented in Python.
* **Distance Check:** The script calculates the Euclidean distance between the currently burning tree and all neighbors.
* **Roll Number Integration:** * **Spread Speed:** The fire propagation delay was calculated using a factor of **1.9** (derived from Roll No 19).
    * **Ignition:** The simulation initiates at `Tree_1`.
* **Animation Baking:** The script automatically sets keyframes on the Emitter Rate (0 to 150) at the precise moment the "fire front" reaches a specific tree.

---

## 📸 Screenshots

*(Student to insert images here)*

1.  **Scene Setup:** <img src='https://github.com/Ishita-Si/forestfire/blob/main/imgs/Screenshot%202025-11-22%20143747.png'>
2.  **Ignition:** <img src='https://github.com/Ishita-Si/forestfire/blob/main/imgs/Screenshot%202025-11-24%20193951.png'>
3.  **Spread:** [Insert Screenshot of the fire spreading to multiple trees]

---

## 💻 Code Snapshot

**Core Logic for Distance-Based Fire Spread:**

```python
# Spread Calculation Snippet
# Logic: Time = CurrentTime + (Distance * SpeedFactor)

spread_speed = 1.9  # Roll No 19 Customization
spread_radius = 15.0

# Loop through neighbors
dist = math.sqrt((c_x - n_x)**2 + (c_z - n_z)**2)

if dist < spread_radius:
    ignition_delay = dist * spread_speed
    ignition_time = current_time + ignition_delay
    
    # Check if this is within the animation timeline
    if ignition_time < max_frames:
        visited[neighbor] = ignition_time
        # Add to queue for next iteration
        process_queue.append((neighbor, ignition_time))
