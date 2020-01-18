# pexif
Keeps your images organized by date.

## Dependencies

You need to install `exifread` dependency via `pip` before using this tool:
```bash
pip install exifread
```

## Usage

You can organize your JPEG photos to directory by date taken (read from exif data):

```bash
python pefix.py photos/source some/where/organized-photos
```

This will process all JPEG image files recursively from `./photos/source` directory, creates a directory structure `{year}/{month}/{day}/{hour}-{minute}-{second}.jpg` to `some/where/organized-photos` where values are read from image exif data and copies images to the respective directories. If image already exists in destination, a unique number will be prepended to filename.

Another way to use the tool is to organize photos in place:

```bash
python pefix.py photos/source
```

This will work just like copying but instead of copying images, it will work in the same root directory (`./photos/source` in this case) and moves images to correct directories.
