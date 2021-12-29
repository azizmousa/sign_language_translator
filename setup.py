from setuptools import setup, find_packages
 
classifiers = [
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.8',
]


with open('requirements.txt') as f:
    dependancies = f.read().splitlines()

with open("README.md", "r") as readme:
    long_descript = readme.read()
 

setup(
  name = 'stos',
  version = '1.0.0',
  
  description = 'Converting the American sign language into speech or text, and vice versa.',
  long_description = long_descript,
  long_description_content_type = "text/markdown",
  
  url = 'https://github.com/azizmousa/sign_language_translator',  
  author = 'azizmousa',
  author_email = 'azizmousa1010@gmail.com',
  
  license = 'MIT', 
  classifiers = classifiers,
  keywords = 'ASL translation', 
  packages = find_packages(),
  install_requires = dependancies 
)
