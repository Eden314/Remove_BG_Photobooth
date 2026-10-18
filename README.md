# Photobooth Background Removal

Photobooth worker for Windows x64. It keeps BiRefNet General loaded for a photo
session and processes only supported images added to the watched folder after
the worker starts. Images already present at startup are skipped.

## Run the portable package

Copy the complete `dist\Photobooth` folder to the target computer. Keep
`Photobooth.exe`, `_internal`, the model, the launcher, and the readme together.
Python and the project dependencies do not need to be installed on the target
computer.

Run:

```powershell
.\RUN_PHOTOBOOTH_WATCH.bat "D:\Photobooth\Input"
```

Save new photos into the input folder after the worker starts. Transparent PNG
results are written to `Input\output_no_bg`. Press Ctrl+C to stop the session.
DirectML is used when available; otherwise processing falls back to CPU.

## Run from source with Python

On a computer with Python 3.12 x64, run `INSTALL.bat` once. It creates an
isolated `.photobooth-env` and installs the Photobooth dependencies without
changing other Python environments. Then run `RUN_PHOTOBOOTH_WATCH.bat` with
the input folder as shown above. The BiRefNet model downloads automatically on
the first run, so that first run needs an Internet connection.

## Build the package

On the build computer, install Python 3.12 x64 and download the
`birefnet-general.onnx` model into `%USERPROFILE%\.u2net`. Run
`BUILD_PHOTOBOOTH.bat`; the portable package is created in `dist\Photobooth`.
The build includes the Python runtime, DirectML runtime, and both model
precisions. Do not commit `dist/` to GitHub; share it as a separate release
asset or copy the folder directly to the target computer.

## Project layout

- `src/`: Photobooth worker and shared image-segmentation engine.
- `docs/`: Vietnamese user guide.
- `INSTALL.bat`: installs the source runtime in an isolated Python environment.
- `build_photobooth.py`, `BUILD_PHOTOBOOTH.bat`: portable build scripts.
- `RUN_PHOTOBOOTH_WATCH.bat`: launches the portable worker.
