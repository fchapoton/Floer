from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='Floer',
      version='0.1',
      description='computation of Floer homology groups of knots',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Jean-Marie Droz',
      license='GPL',
      packages=['Floer'],
      entry_points={
          'console_scripts': ['Floer=Floer:main']},
      package_data={
          'Floer': ['knotAtlasV1.txt', 'knotAtlas.pic']
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
          "Operating System :: OS Independent",
          "Topic :: Scientific/Engineering :: Mathematics",
      ],
      zip_safe=False)
