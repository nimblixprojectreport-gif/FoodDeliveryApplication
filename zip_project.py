import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in ['.git', '.venv', 'venv', '__pycache__', '.idea', '.vscode', 'node_modules']]
        
        for file in files:
            if file.endswith('.pyc') or file == 'food_delivery_project.zip' or file == 'zip_project.py':
                continue
            
            file_path = os.path.join(root, file)
            # Use relative path for archive name so it doesn't include the full path c:\Users\Dell...
            arcname = os.path.relpath(file_path, path)
            ziph.write(file_path, arcname)

if __name__ == '__main__':
    project_path = os.getcwd()
    zip_path = os.path.join(project_path, 'food_delivery_project.zip')
    
    print(f"Zipping directory: {project_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(project_path, zipf)
    
    print(f"Project zipped successfully to: {zip_path}")
