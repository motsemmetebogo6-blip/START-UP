"""run_all.py: rebuild everything (CAD, views, thermal model, cross-check). Edit params.py first to use SolidWorks dimensions."""
import subprocess, sys
steps = ["build_cad.py", "render_iso.py", "drawings.py", "thermal_run.py"]
for s in steps:
    print("==", s); subprocess.run([sys.executable, s], check=True)
print("== octave cross-check")
subprocess.run(["octave-cli", "--eval", "octave_check()"], check=False)
