from distutils.core import setup

setup(
    name='PhotoOrgnazing',
    version='0.9.1',
    packages=['organize','everyone'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    requires=['cv2', 'exifread', 'numpy', 'yaml', 'PyQt5']
)

