import sys, platform
from setuptools import setup, find_packages

mysys = sys.platform
pyver_ = platform.python_version()
pyver = pyver_[0:3]

if mysys == 'win32':
    if pyver == '3.7':
        my_package_data = ['liboctq_f90wrap.cp37-win_amd64.pyd',
            'libgfortran-5.dll','libgcc_s_seh-1.dll',
            'libquadmath-0.dll','libwinpthread-1.dll']
        my_option = 'py37'
    if pyver == '3.8':
        my_package_data = ['liboctq_f90wrap.cp38-win_amd64.pyd',
            'libgfortran-5.dll','libgcc_s_seh-1.dll',
            'libquadmath-0.dll','libwinpthread-1.dll']
        my_option = 'py38'
    if pyver == '3.9':
        my_package_data = ['liboctq_f90wrap.cp39-win_amd64.pyd',
            'libgfortran-5.dll','libgcc_s_seh-1.dll',
            'libquadmath-0.dll','libwinpthread-1.dll']
        my_option = 'py39'
if mysys == 'linux':
    if pyver == '3.8':
        my_package_data = ['liboctq_f90wrap.cpython-38-x86_64-linux-gnu.so',
		'libc.so.6','libgcc_s.so.1',
		'libgfortran.so.5','libm.so.6',
		'libquadmath.so.0']
        my_option = 'py38'


with open('README.md') as f:
    long_description = f.read()

setup(
    author='Chunhui Luo',
    author_email='matprocomp@gmail.com',
    description='A PyPI package for OpenCalphadPython',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    name='ocpython',
    url='https://github.com/Jerry1999/OpenCalphad-Python',
    version='0.0.1',
    license='GPL',

    packages=find_packages(),

    package_data={'':my_package_data },
    include_package_data=True,

    install_requires=[
        'numpy>=1.18',
    ],
    
    options={"bdist_wheel": {"python_tag": my_option,
    }},

    classifiers=[

        "License :: OSI Approved :: GPL License",

        # Supported Python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

    ],

    python_requires='>=3.7',
)