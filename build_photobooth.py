"""Build the standalone Photobooth package with DirectML and CPU fallback."""

import importlib.metadata
from pathlib import Path
import shutil
import sys

from PyInstaller.__main__ import run as pyinstaller_run


ROOT = Path(__file__).resolve().parent
SRC_ROOT = ROOT / "src"
MODEL = Path.home() / ".u2net" / "birefnet-general.onnx"
MODEL_FP16 = ROOT / ".build_models" / "birefnet-general-fp16.onnx"
DIST_ROOT = ROOT / "dist"


def check_environment():
    if sys.version_info[:2] != (3, 12) or sys.maxsize <= 2**32:
        raise RuntimeError("Build can Python 3.12 x64.")
    required = (
        "onnxruntime-directml", "pillow", "numpy", "onnx", "pyinstaller"
    )
    missing = []
    for package in required:
        try:
            importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            missing.append(package)
    if missing:
        raise RuntimeError("Thieu thu vien Python 3.12 build: " + ", ".join(missing))
    if importlib.metadata.version("onnxruntime-directml") != "1.24.4":
        raise RuntimeError("Build can onnxruntime-directml 1.24.4.")
    if not MODEL.is_file():
        raise FileNotFoundError(f"Khong tim thay model: {MODEL}")


def ensure_fp16_model():
    if MODEL_FP16.is_file():
        return
    MODEL_FP16.parent.mkdir(parents=True, exist_ok=True)
    print("Chuyen model sang FP16 de giam bo nho GPU...", flush=True)
    from onnxruntime.transformers.float16 import convert_float_to_float16
    import onnx

    fp16_model = convert_float_to_float16(
        str(MODEL), keep_io_types=True, disable_shape_infer=True
    )
    onnx.save(fp16_model, str(MODEL_FP16))


def build_package(name, entry_script, runner, readme):
    output_dir = DIST_ROOT / name
    work_dir = ROOT / "build" / name
    work_dir.mkdir(parents=True, exist_ok=True)
    args = [
        "--noconfirm",
        "--clean",
        "--onedir",
        "--console",
        f"--specpath={work_dir}",
        f"--name={name}",
        f"--distpath={DIST_ROOT}",
        f"--workpath={work_dir}",
        f"--add-data={MODEL};models",
        f"--add-data={MODEL_FP16};models",
    ]
    args.append(str(SRC_ROOT / entry_script))
    print(f"\nDang dong goi {name}...", flush=True)
    pyinstaller_run(args)

    shutil.copy2(ROOT / runner, output_dir / runner)
    shutil.copy2(ROOT / readme, output_dir / Path(readme).name)
    print(f"Da tao: {output_dir}", flush=True)


def main():
    check_environment()
    ensure_fp16_model()
    print(f"Python build: {sys.executable}")
    print(f"Model birefnet-general FP32: {MODEL} ({MODEL.stat().st_size / (1024**3):.2f} GiB)")
    print(f"Model FP16 for DirectML GPUs: {MODEL_FP16} ({MODEL_FP16.stat().st_size / (1024**3):.2f} GiB)")
    print("Backend: ONNX Runtime DirectML; CPU fallback.")

    build_package(
        "Photobooth", "photobooth_worker.py", "RUN_PHOTOBOOTH_WATCH.bat",
        "docs/README_PHOTOBOOTH.txt",
    )
    print("\nBUILD HOAN TAT: dist\\Photobooth")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("BUILD THAT BAI:", error)
        raise SystemExit(1)
