# exifclean 🧹

> 🌐 **在线体验（手机优先，照片不出设备）: https://muse-ai-assistant.github.io/exifclean/web/**
> 🌐 **Try online (mobile-friendly, photos never leave your device): https://muse-ai-assistant.github.io/exifclean/web/**

Strip EXIF metadata (GPS location, device info, camera settings) from photos in batch — before posting to social media or second-hand marketplaces. **Fully offline**, single file, only depends on Pillow.

批量清除照片 EXIF 信息（GPS 位置、设备信息、拍摄参数），发图前保护隐私。纯离线、单文件、只依赖 Pillow。

## Why

Online EXIF removers require uploading your original photos — do you really want your GPS-tagged pictures on someone else's server? `exifclean` never leaves your machine.

在线去 EXIF 工具要你上传原图——带 GPS 的照片传到别人服务器上，你放心吗？exifclean 全程离线。

## Install

```bash
pip install -r requirements.txt
```

```bash
pip install pillow
# run directly, or:
pip install .
```

## Usage

```bash
# Clean one photo (writes photo_clean.jpg next to the original)
exifclean photo.jpg

# Clean a whole folder
exifclean ./photos -o ./clean

# Recursive
exifclean ./photos -r -o ./clean

# Preview only: see which files have EXIF and what would be stripped
exifclean ./photos --dry-run
```

Example output:

```
photo.jpg -> photo_clean.jpg
  已清除: Make（厂商）, Model（机型）, GPSInfo（GPS 位置）, ISOSpeed（ISO）
处理完成：1 个文件，其中 1 个含 EXIF
```

### Options

- `-o/--out` — output directory (default: same dir, `_clean` suffix — originals are never overwritten)
- `-r/--recursive` — include subdirectories
- `--dry-run` — preview only, list files and the EXIF tags that would be removed

Supported formats: jpg, jpeg, png, webp, tiff, bmp.

## Privacy

Re-encoding drops **all** EXIF tags. Image pixels are preserved (JPEG re-saved at quality 95).

## License

MIT
