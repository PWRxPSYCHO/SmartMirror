import os
import  sys
from setuptools import setup, find_packages

if os.getuid() != 0:
    print('ERROR: Need to run as root')
    sys.exit(1)

print('INFO: Checking and installing requirements')
os.system('! dpkg -S python-imagingtk && apt-get -y install python-imaging-tk')

print('INFO: Generating the requirements form requirements.txt')
package = []

for line in open('requirements.txt').read():
    if not line.startswith('#'):
        package.append(line.strip())

setup(
    name='SmartMirror',
    version='1.0.0',
    install_requires=package,
    packages=find_packages(),
    url='https://github.com/PWRxPSYCHO/SmartMirror',
    license='MIT License',
    author='PWRxPSYCHO',
    author_email='',
    description=''
)
