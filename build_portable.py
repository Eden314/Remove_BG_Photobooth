"""Build independent, self-contained Windows packages for each workflow."""

import importlib.metadata
from pathlib import Path
import shutil
import site
import sys

from PyInstaller.__main__ import run as pyinstaller_run


ROOT = Path(__file__).resolve().parent
MODEL = Path.home() / ".u2net" / "birefnet-general.onnx"
MODEL_FP16 = ROOT / ".build_models" / "birefnet-general-fp16.onnx"
DIST_ROOT = ROOT / "dist"


def find_nvidia_bin_dirs():
    for site_dir in site.getsitepackages():
        candidate = Path(site_dir) / "nvidia"
        bin_dirs = sorted(path for path in candidate.glob("*/bin") if path.is_dir())
        if bin_dirs:
            return bin_dirs
    raise FileNotFoundError(
        "Khong tim thay cac DLL CUDA/cuDNN trong NVIDIA Python packages. "
        "Hay chay BUILD_PACKAGES.bat trong moi truong build da cai dat."
    )


def check_environment():
    if sys.version_info[:2] != (3, 10) or sys.maxsize <= 2**32:
        raise RuntimeError("Build can Python 3.10 x64.")
    required = ("onnxruntime-gpu", "pillow", "numpy", "onnx", "pyinstaller")
    missing = []
    for package in required:
        try:
            importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            missing.append(package)
    if missing:
        raise RuntimeError("Thieu thu vien Python 3.10 build: " + ", ".join(missing))
    if importlib.metadata.version("onnxruntime-gpu") != "1.23.2":
        raise RuntimeError("Build can onnxruntime-gpu 1.23.2 de dong bo CUDA runtime.")
    if not MODEL.is_file():
        raise FileNotFoundError(f"Khong tim thay model: {MODEL}")


def ensure_fp16_model():
    if MODEL_FP16.is_file():
        return
    MODEL_FP16.parent.mkdir(parents=True, exist_ok=True)
    print("Chuyen model sang FP16 de tang toc tren GPU...", flush=True)
    from onnxruntime.transformers.float16 import convert_float_to_float16
    import onnx

    fp16_model = convert_float_to_float16(
        str(MODEL), keep_io_types=True, disable_shape_infer=True
    )
    onnx.save(fp16_model, str(MODEL_FP16))


def build_package(name, entry_script, runner, readme, nvidia_bin_dirs):
    output_dir = DIST_ROOT / name
    work_dir = ROOT / "build" / name
    args = [
        "--noconfirm",
        "--clean",
        "--onedir",
        "--console",
        f"--name={name}",
        f"--distpath={DIST_ROOT}",
        f"--workpath={work_dir}",
        f"--add-data={MODEL};models",
        f"--add-data={MODEL_FP16};models",
    ]
    for dll_dir in nvidia_bin_dirs:
        relative_dest = dll_dir.relative_to(dll_dir.parents[2]).as_posix()
        args.insert(-1, f"--add-data={dll_dir};{relative_dest}")
    args.append(str(ROOT / entry_script))
    print(f"\nDang dong goi {name}...", flush=True)
    pyinstaller_run(args)

    shutil.copy2(ROOT / runner, output_dir / runner)
    shutil.copy2(ROOT / readme, output_dir / readme)
    print(f"Da tao: {output_dir}", flush=True)


def main():
    check_environment()
    nvidia_bin_dirs = find_nvidia_bin_dirs()
    ensure_fp16_model()
    print(f"Python build: {sys.executable}")
    print(f"Model FP32: {MODEL} ({MODEL.stat().st_size / (1024**3):.2f} GiB)")
    print(f"Model FP16: {MODEL_FP16} ({MODEL_FP16.stat().st_size / (1024**3):.2f} GiB)")
    print(f"CUDA/cuDNN DLL folders: {len(nvidia_bin_dirs)}")

    build_package(
        "Remove_BG", "remove_bg_app.py", "RUN_REMOVE_BG_PORTABLE.bat",
        "README_REMOVE_BG.txt", nvidia_bin_dirs,
    )
    build_package(
        "Photobooth", "photobooth_worker.py", "RUN_PHOTOBOOTH_WATCH.bat",
        "README_PHOTOBOOTH.txt", nvidia_bin_dirs,
    )
    print("\nBUILD HOAN TAT: dist\\Remove_BG va dist\\Photobooth")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("BUILD THAT BAI:", error)
        raise SystemExit(1)
