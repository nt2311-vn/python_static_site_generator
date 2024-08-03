import os
import shutil


def copy_directory(src, dst):
    # Delete the contents of the destination directory
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    # Copy the contents recursively
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            print(f"Copying directory {src_path} to {dst_path}")
            shutil.copytree(src_path, dst_path)
        else:
            print(f"Copying file {src_path} to {dst_path}")
            shutil.copy2(src_path, dst_path)


def main():
    src_dir = "static"
    dst_dir = "public"
    copy_directory(src_dir, dst_dir)


if __name__ == "__main__":
    main()
