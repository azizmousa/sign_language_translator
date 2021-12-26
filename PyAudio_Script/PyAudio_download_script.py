import sys
import requests
import os
import struct


def format_url():
    
    ver=sys.version[0:3]
    py_ver = ver.replace('.','')

    py_bit=struct.calcsize("P")*8
    

    if int(py_ver) > 37:  
        txt_format = f'PyAudio-0.2.11-cp{py_ver}-cp{py_ver}-win_amd64.whl'
        
        if py_bit == 64:
            return txt_format
        
        else:
            txt_format = f'PyAudio-0.2.11-cp{py_ver}-cp{py_ver}-win{py_bit}.whl'
           
        
    else:
        txt_format=f'PyAudio-0.2.11-cp{py_ver}-cp{py_ver}m-win_amd64.whl'
    
        if py_bit == 64:
            return txt_format
        else:
            txt_format=  f'PyAudio-0.2.11-cp{py_ver}-cp{py_ver}m-win{py_bit}.whl'
    
    return txt_format
    

def download_file(url, path):
    """
    def download_model(model_url)
    download pretrained h5 model file
    Args:
        url (str): model download url
        path (str): download path
    Returns: True if download succeed
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
    
    
    
    
url = format_url()
url=f'https://download.lfd.uci.edu/pythonlibs/x6hvwk7i/{url}'


path = 'PyAudio.whl'
download_file(url, path)
