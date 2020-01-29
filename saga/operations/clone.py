import requests
import zipfile
from os import remove

def clone(clone_url: str):
    with requests.get(clone_url, stream=True) as response:
        # throw an error, if there is wone
        response.raise_for_status()
        with open("sagatmp.zip", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()

    with zipfile.ZipFile("sagatmp.zip", 'r') as zip_ref:
        zip_ref.extractall()
    remove("sagatmp.zip")

    print(f"Cloned {clone_url}")
