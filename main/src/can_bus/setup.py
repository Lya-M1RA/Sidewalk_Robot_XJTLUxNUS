from setuptools import setup

package_name = 'can_bus'

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
    maintainer='root',
    maintainer_email='l.yang.ze.s@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'send_can0        = can_bus.can0_tx:main',
            'recv_can0        = can_bus.can0_rx:main',
            'encoder_can0     = can_bus.can0_encoder:main',
        ],
    },
)
