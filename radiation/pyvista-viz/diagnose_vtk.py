import vtk
import pyvista as pv
import os

print("=== Environment ===")
print(f"XDG_SESSION_TYPE: {os.environ.get('XDG_SESSION_TYPE')}")
print(f"DISPLAY: {os.environ.get('DISPLAY')}")
print(f"WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY')}")

print("\n=== VTK Info ===")
print(f"VTK Version: {vtk.vtkVersion.GetVTKVersion()}")

# Check available render window types
print("\n=== Available Render Windows ===")
try:
    rw = vtk.vtkRenderWindow()
    print(f"Default render window: {type(rw).__name__}")
except Exception as e:
    print(f"Default render window error: {e}")

print("\n=== PyVista Backend ===")
try:
    print(f"PyVista backend: {pv.global_theme.backend}")
except:
    print("Could not determine PyVista backend")

# Test render window creation specifically
print("\n=== Render Window Test ===")
try:
    plotter = pv.Plotter()
    print("Plotter creation: SUCCESS")

    # This is where the GLX error typically occurs
    rw = plotter.ren_win
    print(f"Render window type: {type(rw).__name__}")

except Exception as e:
    print(f"Render window error: {e}")
