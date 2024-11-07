import os
from glob import glob
from setuptools import setup

package_name = 'ModeManuel'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Wilson Duguet',
    maintainer_email='wilson.duguet@etu.uca.fr',
    description='Package of manual control mode',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['manuel = ModeManuel.ModeManuel:main'
        ],
    },
    data_files=[
        (os.path.join('share', ModeManuel, 'launch'),glob(os.path.join('launch', '*launch.[pxy][yma]*')))
        ]
)
