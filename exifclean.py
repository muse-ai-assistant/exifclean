#!/usr/bin/env python3
"""exifclean - 批量清除照片 EXIF 信息的命令行工具
发照片/截图前，一键清除 GPS 位置、设备信息等隐私数据。
纯离线、单文件、只依赖 Pillow。
"""
import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow: pip install pillow")

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp"}

# 关注的 EXIF 标签（用于展示）
EXIF_NAMES = {
    271: "Make（厂商）",
    272: "Model（机型）",
    306: "DateTime（拍摄时间）",
    33434: "ExposureTime（曝光）",
    33437: "FNumber（光圈）",
    34855: "ISOSpeed（ISO）",
    37386: "FocalLength（焦距）",
    34853: "GPSInfo（GPS 位置）",
}


def iter_images(paths, recursive):
    seen = set()
    for p in paths:
        p = Path(p)
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            rp = p.resolve()
            if rp not in seen:
                seen.add(rp)
                yield p
        elif p.is_dir():
            it = p.rglob("*") if recursive else p.glob("*")
            for f in sorted(it):
                if f.is_file() and f.suffix.lower() in IMG_EXTS:
                    rp = f.resolve()
                    if rp not in seen:
                        seen.add(rp)
                        yield f
        else:
            print(f"跳过(不存在或不支持): {p}", file=sys.stderr)


def read_exif_info(src):
    """返回 (exif_dict, 展示用列表)。"""
    try:
        img = Image.open(src)
        exif = img.getexif()
    except Exception:
        return {}, []
    if not exif:
        return {}, []
    shown = []
    for tag_id, val in exif.items():
        name = EXIF_NAMES.get(tag_id, f"Tag {tag_id}")
        shown.append(name)
    return dict(exif), shown


def clean_one(src, out_dir, dry_run):
    exif, shown = read_exif_info(src)
    has_exif = bool(exif)
    if out_dir:
        dst = Path(out_dir) / src.name
    else:
        dst = src.parent / (src.stem + "_clean" + src.suffix)
    if dry_run:
        status = "含 EXIF" if has_exif else "无 EXIF"
        print(f"[dry] {src} -> {dst}  [{status}]")
        if shown:
            print(f"       将清除: {', '.join(shown)}")
        return has_exif, shown
    # 重新编码，丢掉全部 EXIF
    img = Image.open(src)
    if out_dir:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
    # PNG/WebP 等：不带 exif 参数保存即清除
    save_kw = {}
    if dst.suffix.lower() in (".jpg", ".jpeg"):
        img = img.convert("RGB")
        save_kw = {"quality": 95}
    img.save(dst, **save_kw)
    print(f"{src.name} -> {dst.name}")
    if shown:
        print(f"  已清除: {', '.join(shown)}")
    else:
        print("  (原本无 EXIF)")
    return has_exif, shown


def main():
    ap = argparse.ArgumentParser(
        prog="exifclean",
        description="批量清除照片 EXIF（GPS/设备信息），保护隐私。纯离线。")
    ap.add_argument("inputs", nargs="+", help="图片文件或目录（支持通配符）")
    ap.add_argument("-o", "--out", default=None,
                    help="输出目录（默认：原地，文件名加 _clean 后缀）")
    ap.add_argument("-r", "--recursive", action="store_true",
                    help="递归子目录")
    ap.add_argument("--dry-run", action="store_true",
                    help="只预览：显示会处理哪些文件、含什么 EXIF，不写入")
    args = ap.parse_args()

    total = 0
    cleaned = 0
    for src in iter_images(args.inputs, args.recursive):
        has_exif, _ = clean_one(src, args.out, args.dry_run)
        total += 1
        if has_exif:
            cleaned += 1
    mode = "预览" if args.dry_run else "处理"
    print(f"{mode}完成：{total} 个文件，其中 {cleaned} 个含 EXIF")


if __name__ == "__main__":
    main()
