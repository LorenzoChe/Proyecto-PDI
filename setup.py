from setuptools import setup

setup(
    name="mysql_viewer",
    version="1.0",
    py_modules=["app"],
    install_requires=["mysql-connector-python"],
    entry_points={
        "gui_scripts": [
            "mysql_viewer = app:main",
        ],
    },
)
