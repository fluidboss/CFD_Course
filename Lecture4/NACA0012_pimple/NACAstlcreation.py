#
# git clone https://github.com/mikedh/trimesh.git
# cd trimesh
# python3 setup.py install
#


import pandas as pd
import numpy as np
import trimesh
import math

def load_airfoil_coords(csv_path):
    """
    Load and sanitize 2D airfoil coordinates from CSV file.

    Assumes file has headers: x, y.
    Handles possible whitespace, duplicate points, and non-numeric values.
    """
    df = pd.read_csv(csv_path)

    # Clean whitespace from column headers if necessary
    df.columns = df.columns.str.strip().str.lower()

    # Drop duplicates at leading edge
    df = df.round(7)
    df = df.drop_duplicates(subset=['x', 'y'], keep='first').reset_index(drop=True)

    # Ensure valid numeric types
    df['x'] = pd.to_numeric(df['x'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    df = df.dropna(subset=['x', 'y'])

    return df[['x', 'y']].values


def extrude_airfoil(coords, span=1.0):
    """Extrude airfoil profile along z-axis (2 layers: front and back)"""
    front = np.hstack([coords, np.zeros((coords.shape[0], 1))])
    back = np.hstack([coords, span * np.ones((coords.shape[0], 1))])
    return front, back

def triangulate_surface(front, back):
    """Generate triangle faces between front and back profiles"""
    faces = []
    n = front.shape[0]

    for i in range(n - 1):
        # Vertices of quad: front[i] -> back[i] -> back[i+1] -> front[i+1]
        faces.append([front[i], back[i], back[i + 1]])
        faces.append([front[i], back[i + 1], front[i + 1]])

    # Optionally close the shape
    return np.array(faces)

def save_as_stl(triangles, output_path="naca0012_fixed.stl", angle_degrees=0):
    """Save triangles as STL using trimesh"""
    vertices = triangles.reshape(-1, 3)
    faces = np.arange(len(vertices)).reshape(-1, 3)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    angle_rad = math.radians(angle_degrees)
    print( angle_degrees)
    rot_axis = [0, 0, 1]
    rot_matrix = trimesh.transformations.rotation_matrix(
        -angle_rad,           # rotation angle in radians
        direction=rot_axis,  # axis to rotate around
        point=mesh.centroid  # rotate about center of the mesh
    )
    print(rot_matrix)
    mesh=mesh.apply_transform(rot_matrix)
    mesh.export(output_path)
    print(f"✅ STL file saved to: {output_path}")

def main():
    csv_path = "naca0012.csv"  # Must contain headers: x,y
    span = 1.0
    angle_degrees = 10
    coords_2d = load_airfoil_coords(csv_path)
    print('Read in the coordinates\n')
    front, back = extrude_airfoil(coords_2d, span)
    faces = triangulate_surface(front, back)
    save_as_stl(faces, "constant/triSurface/naca0012_fixed.stl", angle_degrees)

if __name__ == "__main__":
    main()
