from setuptools import setup

setup(
    name="show-hierarchy-linked-parent",
    version="0.1.0",
    author="Rory McCann",
    author_email="rory@technomancy.org",
    py_modules=['showhierarchy'],
    platforms=['any',],
    requires=[],
    entry_points={
        'console_scripts': [
            'showhierarchy = showhierarchy:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
    ],
)
