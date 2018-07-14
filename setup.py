from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read().strip()


setup(
    name='followthegrant_extractor',
    version='0.0.1alpha',
    description='Extract data from downloaded papers',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities'
    ],
    url='https://github.com/followthegrant/Extractor',
    author='Simon Wörpel',
    author_email='simon.woerpel@medienrevolte.de',
    license='MIT',
    packages=['extractor'],
    entry_points={
        'console_scripts': [
            'ftg_extractor=extractor.entry:main'
        ]
    },
    install_requires=[
        'pyyaml',
        'BeautifulSoup4',
        'lxml'
    ],
    zip_safe=False
)
