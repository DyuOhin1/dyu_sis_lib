import os
import shutil

def main():
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                shutil.rmtree(cache_path)
                print(f"Deleted: {cache_path}")

if __name__ == "__main__":
    main()