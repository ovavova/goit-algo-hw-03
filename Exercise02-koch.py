import matplotlib.pyplot as plt
import numpy as np

# The Koch Curve Logic
def get_koch_points(start, end, order):
    """
    Returns a list of (x, y) points representing a Koch curve 
    connecting 'start' and 'end'.
    """
    if order == 0:
        return [start, end]

    # Convert to complex numbers for easy 2D vector math
    p1 = complex(start[0], start[1])
    p2 = complex(end[0], end[1])
    
    # Vector representing the full line segment
    vector = p2 - p1
    
    # Calculate the 3 intermediate points
    # Point A: 1/3 of the way
    a = p1 + vector / 3
    # Point C: 2/3 of the way
    c = p1 + 2 * vector / 3
    # Point B: The "peak" of the triangle (rotated 60 degrees from A)
    # We rotate the segment (C-A) by 60 degrees (pi/3 radians)
    rotation = complex(np.cos(np.pi/3), np.sin(np.pi/3))
    b = a + (c - a) * rotation

    # Recursive calls for the 4 new segments
    # We convert back to (x, y) tuples for the recursive inputs
    seg1 = get_koch_points((p1.real, p1.imag), (a.real, a.imag), order - 1)
    seg2 = get_koch_points((a.real, a.imag), (b.real, b.imag), order - 1)
    seg3 = get_koch_points((b.real, b.imag), (c.real, c.imag), order - 1)
    seg4 = get_koch_points((c.real, c.imag), (p2.real, p2.imag), order - 1)

    # Combine points (exclude duplicates where segments join)
    return seg1[:-1] + seg2[:-1] + seg3[:-1] + seg4

# --- 2. The Sierpinski Logic (Structure) ---
def midpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

def draw_koch_triangle(vertices, ax, koch_order):
    """
    Draws a triangle where every side is a Koch curve.
    """
    # Define the pairs of vertices that make up the triangle sides
    # Side 1: Vertex 0 -> Vertex 1
    # Side 2: Vertex 1 -> Vertex 2
    # Side 3: Vertex 2 -> Vertex 0 (Closing the loop)
    sides = [
        (vertices[0], vertices[1]),
        (vertices[1], vertices[2]),
        (vertices[2], vertices[0])
    ]
    
    for start, end in sides:
        # Generate the fractal points for this side
        points = get_koch_points(start, end, koch_order)
        # Unzip points into X and Y lists for plotting
        x_vals, y_vals = zip(*points)
        ax.plot(x_vals, y_vals, 'k-', linewidth=0.5) # 'k-' means black line

def sierpinski_with_koch(vertices, sierpinski_level, koch_order, ax):
    # Base Case: When we reach the smallest triangle
    if sierpinski_level == 0:
        # Instead of a straight triangle, we draw the "Koch Triangle"
        draw_koch_triangle(vertices, ax, koch_order)
    else:
        # Recursive Step: Split into 3 smaller triangles (standard Sierpinski)
        mid01 = midpoint(vertices[0], vertices[1])
        mid12 = midpoint(vertices[1], vertices[2])
        mid20 = midpoint(vertices[2], vertices[0])
        
        # Top Triangle
        sierpinski_with_koch([vertices[0], mid01, mid20], sierpinski_level - 1, koch_order, ax)
        # Right Triangle
        sierpinski_with_koch([mid01, vertices[1], mid12], sierpinski_level - 1, koch_order, ax)
        # Left Triangle
        sierpinski_with_koch([mid20, mid12, vertices[2]], sierpinski_level - 1, koch_order, ax)

# --- 3. Main Execution ---
def main():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Define initial triangle vertices
    vertices = [[0, 0], [0.5, np.sqrt(3)/2], [1, 0]]

    # Add how deep to go
    while True:
        try:
            sierpinski_level = int(input("Please eneter how many triangles to draw (0-5) 0 for snowflake: "))
            if sierpinski_level < 0 or sierpinski_level > 5:
                raise ValueError("Number must be 1-5")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
        
    while True:
        try:
            koch_order = int(input("Please enter the recursion level in koch (0-10): "))
            if koch_order < 0 or koch_order > 10:
                raise ValueError("Number must be 0-10")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
    
    # sierpinski_level: How many triangles to generate (holes)
    # koch_order: How "rough" the edges of the triangles are
    sierpinski_with_koch(vertices, sierpinski_level=sierpinski_level, koch_order=koch_order, ax=ax)
    
    plt.show()

if __name__ == "__main__":
    main()