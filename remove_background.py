import argparse
import hashlib
import os
import sys
import time
import urllib.request
from pathlib import Path

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
DEFAULT_MODEL = "birefnet-general"
FP16_MODEL = "birefnet-general-fp16.onnx"
MODEL_URL = (
    "https://github.com/danielgatis/rembg/releases/download/v0.0.0/"
    "BiRefNet-general-epoch_244.onnx"
)
MODEL_MD5 = "7a35a0141cbbc80de11d9c9a28f52697"
CUDA_DLL_HANDLES = []


def register_cuda_dll_paths(ort):
    """Expose CUDA/cuDNN DLL folders bundled in pip's NVIDIA packages."""
    site_packages = Path(ort.__file__).resolve().parent.parent
    nvidia_dir = site_packages / "nvidia"
    if not nvidia_dir.is_dir() or not hasattr(os, "add_dll_directory"):
        return 0
    dll_dirs = sorted(nvidia_dir.glob("*/bin"))
    for dll_dir in dll_dirs:
        CUDA_DLL_HANDLES.append(os.add_dll_directory(str(dll_dir)))
    if dll_dirs:
        os.environ["PATH"] = os.pathsep.join(
            [*(str(path) for path in dll_dirs), os.environ.get("PATH", "")]
        )
    return len(dll_dirs)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tach nen anh bang mo hinh BiRefNet."
    )
    parser.add_argument("path", type=Path, help="Duong dan den mot anh hoac thu muc anh")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=(DEFAULT_MODEL,),
        help=(
            "Mo hinh BiRefNet General duoc dung trong ban portable."
        ),
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Ep buoc xu ly bang CPU, khong thu dung GPU NVIDIA.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help=(
            "Giu mo hinh trong RAM/VRAM va cho anh moi trong thu muc; "
            "dung cho photobooth."
        ),
    )
    parser.add_argument(
        "--keep-mask",
        type=Path,
        help=(
            "Anh mask den-trang cung kich thuoc: vung trang se duoc giu lai "
            "(dung de sua vat bi AI xoa nham)."
        ),
    )
    return parser.parse_args()


def model_file(model_home: Path) -> Path:
    model_path = model_home / f"{DEFAULT_MODEL}.onnx"
    if model_path.is_file():
        return model_path

    model_home.mkdir(parents=True, exist_ok=True)
    partial_path = model_path.with_suffix(".onnx.part")
    print("Dang tai model lan dau (gan 1 GB)...", flush=True)

    def report_progress(block_count, block_size, total_size):
        if total_size > 0:
            percent = min(100, int(block_count * block_size * 100 / total_size))
            print(f"\rTai model: {percent}%", end="", flush=True)

    try:
        urllib.request.urlretrieve(MODEL_URL, partial_path, report_progress)
        digest = hashlib.md5()
        with partial_path.open("rb") as downloaded:
            for chunk in iter(lambda: downloaded.read(8 * 1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != MODEL_MD5:
            raise ValueError("Checksum cua model khong dung; tep tai xuong bi loi.")
        partial_path.replace(model_path)
        print("\nTai model xong.")
    except Exception:
        partial_path.unlink(missing_ok=True)
        raise
    return model_path


def predict_mask(session, image, np, Image):
    """Run the same BiRefNet-General preprocessing and mask scaling as rembg."""
    resized = image.convert("RGB").resize((1024, 1024), Image.Resampling.LANCZOS)
    pixels = np.asarray(resized, dtype=np.float64)
    pixels /= max(float(pixels.max()), 1e-6)
    mean = np.asarray((0.485, 0.456, 0.406), dtype=np.float64)
    std = np.asarray((0.229, 0.224, 0.225), dtype=np.float64)
    pixels = (pixels - mean) / std
    tensor = np.expand_dims(pixels.transpose((2, 0, 1)), axis=0).astype(np.float32)

    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: tensor})[0][:, 0, :, :]
    prediction = 1.0 / (1.0 + np.exp(-output))
    low = float(prediction.min())
    high = float(prediction.max())
    if high > low:
        prediction = (prediction - low) / (high - low)
    else:
        prediction.fill(0)
    mask = Image.fromarray(
        (np.squeeze(prediction) * 255).astype("uint8"), mode="L"
    )
    return mask.resize(image.size, Image.Resampling.LANCZOS)


def wait_for_new_images(
    folder: Path, processed: set, stable: dict, excluded: Path = None
):
    """Wait until new image files have stopped changing before opening them."""
    while True:
        ready = []
        for path in sorted(folder.iterdir()):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED:
                continue
            if excluded and path.resolve() == excluded:
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            identity = (str(path.resolve()), stat.st_size, stat.st_mtime_ns)
            if identity in processed:
                continue
            if stable.get(str(path.resolve())) == identity:
                ready.append((path, identity))
            else:
                stable[str(path.resolve())] = identity
        if ready:
            return ready
        time.sleep(0.5)


def main(force_watch=False, allow_watch=True):
    args = parse_args()
    if force_watch:
        args.watch = True
    elif args.watch and not allow_watch:
        print("Remove_BG chi xu ly anh theo yeu cau; dung goi Photobooth de theo doi thu muc.")
        return 1
    input_path = args.path.expanduser().resolve()
    if not input_path.exists():
        print("Khong tim thay tep/thu muc:", input_path)
        return 1

    print("Dang nap thu vien AI...", flush=True)
    bundled_model_dir = None
    if getattr(sys, "frozen", False):
        bundled_root = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        bundled_model_dir = bundled_root / "models"
        os.environ["U2NET_HOME"] = str(bundled_model_dir)
    try:
        from PIL import Image, ImageChops, ImageOps
        import onnxruntime as ort
        import numpy as np
    except ImportError:
        print("Chua cai thu vien. Hay chay INSTALL.bat truoc.")
        return 1
    print("Thu vien da san sang.", flush=True)
    if bundled_model_dir and not (
        bundled_model_dir / f"{DEFAULT_MODEL}.onnx"
    ).is_file():
        print("Goi portable bi thieu model birefnet-general.onnx:", bundled_model_dir)
        return 1

    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED:
            print("Dinh dang khong ho tro. Dung JPG/JPEG/PNG/WEBP/BMP.")
            return 1
        files = [input_path]
        output_parent = input_path.parent
    elif input_path.is_dir():
        files = sorted(
            p for p in input_path.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED
        )
        output_parent = input_path
    else:
        print("Duong dan khong phai tep anh hoac thu muc:", input_path)
        return 1
    if not files and not args.watch:
        print("Khong tim thay anh JPG/JPEG/PNG/WEBP/BMP.")
        return 0
    if args.watch and not input_path.is_dir():
        print("Che do --watch can duong dan la thu muc.")
        return 1

    keep_mask_path = args.keep_mask.expanduser().resolve() if args.keep_mask else None
    if keep_mask_path and not keep_mask_path.is_file():
        print("Khong tim thay mask:", keep_mask_path)
        return 1
    if keep_mask_path:
        files = [p for p in files if p.resolve() != keep_mask_path]
        if input_path.is_file() and input_path.resolve() == keep_mask_path:
            print("Mask phai la tep rieng, khong the dung cung tep anh goc.")
            return 1
        if not files:
            print("Khong con anh dau vao nao sau khi loai tep mask.")
            return 0

    output_dir = output_parent / "output_no_bg"
    output_dir.mkdir(exist_ok=True)

    print(f"Tim thay {len(files)} anh.")
    print(f"Mo hinh: {args.model}")
    print("Tinh chinh vien alpha theo kich thuoc anh goc")
    available = ort.get_available_providers()
    providers = (
        ["CUDAExecutionProvider", "CPUExecutionProvider"]
        if "CUDAExecutionProvider" in available and not args.cpu
        else ["CPUExecutionProvider"]
    )
    if providers[0] == "CUDAExecutionProvider":
        dll_dir_count = register_cuda_dll_paths(ort)
        if dll_dir_count:
            print(f"Da dang ky {dll_dir_count} thu muc DLL CUDA/cuDNN.")
        if dll_dir_count == 0 and hasattr(ort, "preload_dlls"):
            print("Dang nap thu vien CUDA/cuDNN...")
            try:
                ort.preload_dlls(directory="")
            except Exception as error:
                print(f"Khong the nap DLL CUDA/cuDNN: {error}")
    model_home = bundled_model_dir or Path(
        os.environ.get("U2NET_HOME", Path.home() / ".u2net")
    )
    model_path = None
    cpu_model_path = None
    session_started = time.perf_counter()
    print("Dang khoi tao mo hinh AI...\n")
    try:
        cpu_model_path = model_file(model_home)
        model_path = cpu_model_path
        fp16_path = model_home / FP16_MODEL
        if "CUDAExecutionProvider" in providers and fp16_path.is_file():
            model_path = fp16_path
            print("GPU dung ban FP16 da toi uu; CPU du phong van dung model goc.")
        session = ort.InferenceSession(
            str(model_path), providers=providers
        )
    except Exception as error:
        if "CUDAExecutionProvider" in providers:
            print(f"CUDA khong khoi tao duoc ({error}); thu lai bang CPU.")
            try:
                cpu_model_path = cpu_model_path or model_file(model_home)
                model_path = cpu_model_path
                providers = ["CPUExecutionProvider"]
                session = ort.InferenceSession(str(model_path), providers=providers)
            except Exception as cpu_error:
                print(f"Khong the khoi tao ONNX Runtime tren CPU: {cpu_error}")
                return 1
        else:
            print(f"Khong the khoi tao model {args.model}: {error}")
            return 1
    active = session.get_providers()
    if "CUDAExecutionProvider" in active:
        print("CUDA provider da khoi tao; dang thu suy luan tren GPU NVIDIA.")
    else:
        print("Xu ly bang: CPU (GPU CUDA chua san sang)")
    print(f"Thoi gian nap model/session: {time.perf_counter() - session_started:.2f} giay.")

    if args.watch:
        print("Che do photobooth: mo hinh se duoc giu san; nhan Ctrl+C de dung.")
    processed = set()
    stable = {}
    totals = {"ok": 0, "fail": 0}
    while True:
        if args.watch:
            ready = wait_for_new_images(
                input_path, processed, stable, keep_mask_path
            )
            files = [item[0] for item in ready]
            identities = {item[0]: item[1] for item in ready}
            print(f"Nhan duoc {len(files)} anh moi.", flush=True)
        else:
            identities = {}
        ok = fail = 0
        for i, src in enumerate(files, 1):
            started = time.perf_counter()
            dst = output_dir / (src.stem + ".png")
            try:
                with Image.open(src) as opened:
                    image = ImageOps.exif_transpose(opened).convert("RGB")
                    try:
                        mask = predict_mask(session, image, np, Image)
                    except Exception as gpu_error:
                        if "CUDAExecutionProvider" not in providers:
                            raise
                        print(f"\nCUDA gap loi khi suy luan ({gpu_error}); dang thu lai bang CPU.")
                        providers = ["CPUExecutionProvider"]
                        model_path = cpu_model_path
                        session = ort.InferenceSession(
                            str(model_path), providers=providers
                        )
                        print("Da chuyen sang CPU.")
                        mask = predict_mask(session, image, np, Image)
                    result = image.convert("RGBA")
                    result.putalpha(mask)
                    if keep_mask_path:
                        with Image.open(keep_mask_path) as opened_mask:
                            keep_mask = opened_mask.convert("L")
                            if keep_mask.size != image.size:
                                keep_mask = keep_mask.resize(
                                    image.size, Image.Resampling.LANCZOS
                                )
                            alpha = ImageChops.lighter(
                                result.getchannel("A"), keep_mask
                            )
                            result.putalpha(alpha)
                    result.save(dst, "PNG")
                    if i == 1 and "CUDAExecutionProvider" in providers:
                        active = session.get_providers()
                        if "CUDAExecutionProvider" in active:
                            print("Xac nhan: anh dang duoc suy luan tren GPU NVIDIA.")
                        else:
                            print(
                                "CANH BAO: CUDA/cuDNN loi; ONNX Runtime da chuyen sang CPU. "
                                "Hay cap nhat driver NVIDIA de tuong thich voi CUDA 12.8."
                            )
                ok += 1
                totals["ok"] += 1
                print(
                    f"[{i}/{len(files)}] OK  {src.name} "
                    f"({time.perf_counter() - started:.2f} giay)"
                )
            except Exception as error:
                fail += 1
                totals["fail"] += 1
                print(f"[{i}/{len(files)}] LOI {src.name}: {error}")
            finally:
                if args.watch:
                    processed.add(identities[src])

        if args.watch:
            print(
                f"Lo anh xong: thanh cong {ok}, loi {fail}. "
                f"Dang cho anh moi trong: {input_path}",
                flush=True,
            )
            continue
        break

    print("\n==============================")
    print("HOAN TAT")
    print("Thanh cong:", totals["ok"])
    print("Loi:", totals["fail"])
    print("Ket qua:", output_dir)
    print("Mask AI duoc noi suy khi dua ve kich thuoc anh goc.")
    if keep_mask_path:
        print("Da ap dung mask giu vat:", keep_mask_path)
    print("==============================")
    return 0 if totals["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
