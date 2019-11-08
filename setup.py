from setuptools import setup, find_packages
from hostseditor import __version__

NAME = 'hostseditor'
with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

if __name__ == '__main__':
    setup(
        name=NAME,
        packages=find_packages(),
        python_requires=">=3.6",
        install_requires=REQUIREMENTS,
        setup_requires=REQUIREMENTS,
        version=__version__,
        url='https://github.com/AlexBrin/' + NAME,
        license='MIT License',
        author='Alexander Gorenkov',
        author_email='g.a.androidjc2@ya.ru',
        description='CLI hosts editor (for Windows, Linux and WSL)',
        entry_points={
            "console_scripts": [
                "hostseditor=hostseditor.__main__:run"
            ]
        }
    )
