import argparse
from pathlib import Path

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
DEFAULT_MODEL = "birefnet-general"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tach nen anh bang mo hinh BiRefNet."
    )
    parser.add_argument("path", type=Path, help="Duong dan den mot anh hoac thu muc anh")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=("birefnet-general", "birefnet-portrait", "isnet-general-use"),
        help=(
            "birefnet-general: nguoi va vat the; birefnet-portrait: uu tien chan dung; "
            "isnet-general-use: mo hinh cu de doi chieu."
        ),
    )
    parser.add_argument(
        "--alpha-matting",
        action="store_true",
        help="Tinh chinh alpha va mau o vien; cham hon, huu ich khi con vien trang.",
    )
    parser.add_argument(
        "--keep-model-colors",
        action="store_true",
        help="Tat khu loang mau o vien (mac dinh dang bat).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = args.path.expanduser().resolve()
    if not input_path.exists():
        print("Khong tim thay tep/thu muc:", input_path)
        return 1

    try:
        from PIL import Image, ImageOps
        from rembg import new_session, remove
    except ImportError:
        print("Chua cai thu vien. Hay chay INSTALL.bat truoc.")
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
    if not files:
        print("Khong tim thay anh JPG/JPEG/PNG/WEBP/BMP.")
        return 0

    output_dir = output_parent / "output_no_bg"
    output_dir.mkdir(exist_ok=True)

    print(f"Tim thay {len(files)} anh.")
    print(f"Mo hinh: {args.model}")
    if args.alpha_matting:
        print("Tinh chinh vien: alpha matting (cham hon)")
    else:
        print("Tinh chinh vien: khu loang mau")
    print("Dang khoi tao mo hinh AI (lan dau co the tai mo hinh)...\n")
    try:
        session = new_session(args.model)
    except Exception as error:
        print(f"Khong the tai mo hinh {args.model}: {error}")
        print("Kiem tra ket noi Internet trong lan chay dau tien.")
        return 1

    ok = fail = 0
    for i, src in enumerate(files, 1):
        dst = output_dir / (src.stem + ".png")
        try:
            with Image.open(src) as opened:
                image = ImageOps.exif_transpose(opened).convert("RGB")
                # Remove color left over from the original background on soft edges.
                options = {"decontaminate": not args.keep_model_colors}
                if args.alpha_matting:
                    options.update(
                        alpha_matting=True,
                        alpha_matting_foreground_threshold=240,
                        alpha_matting_background_threshold=10,
                        alpha_matting_erode_size=10,
                    )
                result = remove(image, session=session, **options)
                result.save(dst, "PNG")
            ok += 1
            print(f"[{i}/{len(files)}] OK  {src.name}")
        except Exception as error:
            fail += 1
            print(f"[{i}/{len(files)}] LOI {src.name}: {error}")

    print("\n==============================")
    print("HOAN TAT")
    print("Thanh cong:", ok)
    print("Loi:", fail)
    print("Ket qua:", output_dir)
    if not args.alpha_matting:
        print("Da bat khu loang mau vien. Neu can sua ca hinh dang mep, thu --alpha-matting.")
    print("==============================")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
