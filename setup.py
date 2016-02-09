from setuptools import setup
from setuptools import find_packages

version = '0.0.1.dev0'

setup(
    name='Products.CMFPlone',
    version=version,
    description="A modular Twitch bot written in Python with a web interface.",
    long_description=open("README.md").read() + "\n" + open("CHANGES.md").read(),
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Communications :: Chat :: Internet Relay Chat",

    ],
    keywords='Twitch Irc Bot',
    author='Gagaro',
    author_email='gagaro42@gmail.com',
    url='https://github.com/Gagaro/PimpMyBot',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-daemon'
        'bottle',
        'requests',
    ],
    entry_points="""\
      [console_scripts]
      plone-generate-gruntfile = Products.CMFPlone._scripts.generate_gruntfile:main
      plone-compile-resources = Products.CMFPlone._scripts.compile_resources:main
      """
)
