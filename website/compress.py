import os
import gzip


INPUT_PATH = os.path.join(os.path.dirname(__file__), "static")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "staticfiles")
SKIP_COMPRESS_EXTENSIONS = [
    # Images
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    # Compressed files
    ".zip",
    ".gz",
    ".tgz",
    ".bz2",
    ".tbz",
    ".xz",
    ".br",
    # Flash
    ".swf",
    ".flv",
    # Fonts
    ".woff",
    ".woff2",
]


def remove_files(path):
    print(f"Removing files from {path}")
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def main():
    # remove all files from "staticfiles"
    remove_files(OUTPUT_PATH)

    for dirpath, dirs, files in os.walk(INPUT_PATH):
        for filename in files:
            input_file = os.path.join(dirpath, filename)
            with open(input_file, "rb") as f:
                data = f.read()
            # compress if file extension is not part of SKIP_COMPRESS_EXTENSIONS
            name, ext = os.path.splitext(filename)
            if ext not in SKIP_COMPRESS_EXTENSIONS:
                # save compressed file to the "staticfiles" directory
                compressed_output_file = os.path.join(OUTPUT_PATH, f"{filename}.gz")
                print(f"\nCompressing {filename}")
                print(f"Saving {filename}.gz")
                output = gzip.open(compressed_output_file, "wb")
                try:
                    output.write(data)
                finally:
                    output.close()
            else:
                print(f"\nSkipping compression of {filename}")
            # save original file to the "staticfiles" directory
            output_file = os.path.join(OUTPUT_PATH, filename)
            print(f"Saving {filename}")
            with open(output_file, "wb") as f:
                f.write(data)


if __name__ == "__main__":
    main()