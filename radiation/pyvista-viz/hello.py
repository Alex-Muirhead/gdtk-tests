import os
import pyvista as pv

print(f"Display backend: {os.environ.get('XDG_SESSION_TYPE', 'unknown')}")
print(f"Display: {os.environ.get('DISPLAY', 'not set')}")
print(f"Wayland display: {os.environ.get('WAYLAND_DISPLAY', 'not set')}")

try:
    # Test basic PyVista functionality
    sphere = pv.Sphere()
    print("PyVista sphere creation: SUCCESS")

    # Test plotting (this is where the error likely occurs)
    plotter = pv.Plotter()
    plotter.add_mesh(sphere)
    print("PyVista plotter setup: SUCCESS")

    # This is the critical test
    plotter.show()
    print("PyVista display: SUCCESS")

except Exception as e:
    print(f"PyVista error: {e}")
