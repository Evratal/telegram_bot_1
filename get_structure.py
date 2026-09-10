import os

exclude_dirs = {".git", ".venv", "__pycache__"}

def walk_project():
    for root, dirs, files in os.walk("."):
        # убираем из обхода папки, которые не хотим видеть
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            print(os.path.join(root, f))

if __name__ == "__main__":
    walk_project()
