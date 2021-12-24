import requests


def download_model(model_url):
    request = requests.get(model_url, allow_redirects=True)
    open('cv_model.h5', 'wb').write(request.content)


def update_model(model_path):
    pass

