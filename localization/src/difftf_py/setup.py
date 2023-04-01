from setuptools import setup

package_name = 'difftf_py'

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
    maintainer='peng',
    maintainer_email='peng@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "diff_tf = difftf_py.diff_tf:main",
            "odom_publisher = difftf_py.trans_odom:main",
            "robotvtowheelv = difftf_py.robotvtowheelv:main"
        ],
    },
)