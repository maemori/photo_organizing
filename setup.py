from distutils.core import setup

setup(
    name='PhotoOrgnazing',
    version='0.1dev',
    packages=['photooragnaizing',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(), requires=['cv2', 'exifread', 'numpy', 'yaml']
)