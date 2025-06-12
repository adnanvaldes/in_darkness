from setuptools import setup, find_packages

setup(
    name="in_darkness",
    version="1.0",
    description="A 2D survival game made with Pygame",
    author="Your Name",
    packages=find_packages(),
    install_requires=["pygame"],
    entry_points={"console_scripts": ["in-darkness=in_darkness.main:main"]},
    include_package_data=True,
)
