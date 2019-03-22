from setuptools import setup

setup(
    name='V2ray.Stats',
    version='1.0',
    url='https://github.com/Ricky-Hao/V2Ray.Stats',
    license='Apache License 2.0',
    author='Ricky Hao',
    description='Collect V2Ray traffic stats by API.',
    packages=['v2ray_stats'],
    install_requires=[
        'schedule',
        'texttable'
    ]
)