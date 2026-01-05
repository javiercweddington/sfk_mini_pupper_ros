from setuptools import setup, find_packages
from glob import glob

package_name = 'stanford_controller'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='champ',
    maintainer_email='champ@todo.com',
    description='Stanford controller',
    license='BSD',
)
