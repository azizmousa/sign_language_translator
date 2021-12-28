import os
import requests


def download_file(url, path):
    """
    def download_model(model_url)
    download pretrained h5 __model file
    Args:
        url (str): __model download url
        path (str): download path
    Returns:
        True if download succeed
        False otherwise
    """
    try:
        request = requests.get(url, allow_redirects=True)
        path_parent = os.path.abspath(os.path.join(path, os.pardir))
        os.makedirs(path_parent, exist_ok=True)
        open(path, 'wb').write(request.content)
        return True
    except:
        return False


def update_model(model_path):
    pass