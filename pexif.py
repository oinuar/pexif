import exifread
import sys
import os
from datetime import datetime

def copy(source, dest, chunk_size=4096):
    with open(source, "rb") as source_file:
        with open(dest, "wb") as dest_file:
            while True:
                chunk = source_file.read(chunk_size)
                
                if not chunk:
                    break

                dest_file.write(chunk)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} [source directory] ([destination directory])".format(sys.argv[0]))
        sys.exit(1)

    source_directory = sys.argv[1]

    if len(sys.argv) > 1:
        destination_directory = sys.argv[2]
    else:
        destination_directory = source_directory

    for root, directory, files in os.walk(source_directory):
        for file in files:
            extension = file.split(".")[-1]
            source = os.path.join(root, file)
        
            # Skip all non-jpeg files.
            if extension.lower() not in ["jpg", "jpeg"]:
                continue

            with open(source, "rb") as handle:
                tags = exifread.process_file(handle)
                date = datetime.strptime(tags["EXIF DateTimeOriginal"].printable, "%Y:%m:%d %H:%M:%S")
                dest_directory = os.path.join(destination_directory, date.strftime("%Y/%m/%d"))

            # Ensure that destination directory exists.
            try:
                os.makedirs(dest_directory)
            except OSError:
                pass
            
            dest_file = date.strftime("%H-%M-%S.{}".format(extension))
            dest = os.path.join(dest_directory, dest_file)
            
            # We are done if file is already in correct place.
            if source == dest:
                continue
            
            # Ensure that filename is unique.
            counter = 1
            while os.path.exists(dest):
                dest_file = date.strftime("%H-%M-%S_{}.{}".format(counter, extension))
                dest = os.path.join(dest_directory, dest_file)
                counter += 1

            # Move file to destination.
            if source_directory == destination_directory:
                os.rename(source, dest)
                
            # Copy file to destination.
            else:
                copy(source, dest)

            print("{} => {}".format(source, dest))
