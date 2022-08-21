import os
import requests
import shutil

def get_files(folder_path):
    return [os.path.join(folder_path, item) for item in os.listdir(folder_path) if item.endswith('.mkv')]

def download_image(url, destination):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(destination, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return destination

    return False