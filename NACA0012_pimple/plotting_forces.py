import numpy as np
import matplotlib.pyplot as plt

def read_forces_file(filename):
    # Skip header lines starting with '#' and read columns
    data = []
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith('#') and line.strip():
                data.append([float(x) for x in line.strip().split()])
    return np.array(data)

def plot_forces(data, title='Forces over Time'):
    time = data[:, 0]
    fx = data[:, 1] + data[:, 4]  # pressure + viscous x
    fy = data[:, 2] + data[:, 5]  # pressure + viscous y
    fz = data[:, 3] + data[:, 6]  # pressure + viscous z

    plt.figure(figsize=(10, 6))
    plt.plot(time, fx, label='Force X')
    plt.plot(time, fy, label='Force Y')
    plt.plot(time, fz, label='Force Z')
    plt.xlabel('Time [s]')
    plt.ylabel('Force [N]')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Change this to your actual file path
filename = 'postProcessing/forces_cylinder/0/force.dat'

# Run
data = read_forces_file(filename)
plot_forces(data, title='Cylinder1 Forces')
