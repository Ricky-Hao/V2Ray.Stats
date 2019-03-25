from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='V2ray.Stats',
    version='0.3.0',
    url='https://github.com/Ricky-Hao/V2Ray.Stats',
    license='Apache License 2.0',
    author='Ricky Hao',
    author_email='a959695@live.com',
    description='Collect V2Ray traffic stats by API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['v2ray_stats'],
    install_requires=[
        'schedule',
        'texttable'
    ]
)