import os
import requests


def download_model(model_url):
    """
    def download_model(model_url)
    download pretrained h5 model file
    Args:
        model_url (str): model download url

    Returns: True if download succeed
            False otherwise
    """
    try:
        request = requests.get(model_url, allow_redirects=True)
        os.makedirs('model', exist_ok=True)
        open(os.path.join('model', 'cv_model.h5'), 'wb').write(request.content)
        return True
    except:
        return False


def update_model(model_path):
    pass

