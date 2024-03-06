import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

G = 6.674e-11  # Gravitational constant
simulation_dt = 0.0003  # Smaller time step for accurate calculations
plotting_dt = 0.1 # Time interval for plotting (1 second)

# Larger dimensions for the plot
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# New initial conditions for three bodies for an amazing visualization with motion
masses = np.array([1e12, 1e12, 1e12])
positions = np.array([[0.0, 0.0, 0.0], [-4.0, 3.0, 2.0], [6.0, -2.0, -1.0]])
velocities = np.array([[0.0, 0.0, 0.0], [0.1, -0.2, 0.3], [-0.1, 0.2, -0.3]])

# Arrays to store data for plotting
trajectory = np.zeros((0, 3, 3))  # Time steps, Bodies, Coordinates (x, y, z)

colors = ['g', 'b', 'r']
labels = ['Body 1', 'Body 2', 'Body 3']


# Function to update the plot
def update_plot(num):
    global positions, velocities, trajectory

    # Simulate for 1 second and accumulate data
    accumulated_positions = []
    simulation_steps = int(plotting_dt / simulation_dt)

    for _ in range(simulation_steps):
        # Compute pairwise gravitational forces and update velocities
        forces = np.zeros_like(velocities)

        for i in range(3):
            for j in range(3):
                if i != j:
                    r = positions[i] - positions[j]
                    r_norm = np.linalg.norm(r)
                    force = G * masses[i] * masses[j] / r_norm ** 3 * r
                    forces[i] -= force
                    forces[j] += force

        velocities += forces * (simulation_dt / (2.0 * masses[:, np.newaxis]))

        # Update positions
        positions += velocities * simulation_dt
        accumulated_positions.append(positions.copy())

    # Append the accumulated positions to the trajectory
    trajectory = np.vstack((trajectory, accumulated_positions))

    # Clear the previous frame
    ax.clear()


    for i in range(3):
        # Plot the trajectory as a line with antialiasing
        ax.plot(trajectory[:, i, 0], trajectory[:, i, 1], trajectory[:, i, 2], label=labels[i], color=colors[i],
                linewidth=0.5, antialiased=True)

        # Plot the present location of the particles as thicker spheres with antialiasing
        ax.scatter(positions[i, 0], positions[i, 1], positions[i, 2], s=50, c=colors[i], marker='o', antialiased=True)

    # Set larger axis limits
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    ax.legend()
    plt.title('Amazing Triple Body Gravitational Movement in 3D Space')



# Create an animation with an explicit number of frames
# Adjust the value of frames as needed
ani = FuncAnimation(fig, update_plot, frames=1000, interval=0.0001, repeat=False)
plt.show()
