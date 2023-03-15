from setuptools import setup

package_name = 'motor_control'

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
            'local_controller           = motor_control.local_controller:main',
            'encoder_counter_l          = motor_control.encoder_counter_l:main',
            'encoder_counter_r          = motor_control.encoder_counter_r:main',
            'upper_controller           = motor_control.upper_node:main'
        ],
    },
)
1