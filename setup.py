from setuptools import setup

setup(
    name="show-hierarchy-linked-parent",
    version="1.0.0",
    author="Rory McCann",
    author_email="rory@technomancy.org",
    py_modules=['showhierachy'],
    platforms=['any',],
    requires=[],
    entry_points={
        'console_scripts': [
            'showhierachy = showhierachy:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
    ],
)
