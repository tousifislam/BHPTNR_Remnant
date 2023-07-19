from setuptools import find_packages, setup

long_description = open('README.md').read()

setup(name='BHPTNRremnant',
      version='0.0.2',
      author='Tousif Islam, Scott Field, Gaurav Khanna',
      author_email='tousifislam24@gmail.com',
      #packages=['BHPTNRremnant'],
      #packages=find_packages(),
      packages=['BHPTNRremnant', 'BHPTNRremnant.data', 'BHPTNRremnant.tests'],
      license='MIT',
      include_package_data=True,
      contributors=['Tousif Islam, Scott Field, Gaurav Khanna'],
      description='Python package for remnant black hole properties using perturbation theory and NR',
      long_description=long_description,
      long_description_content_type='text/markdown',
      # will start new downloads if these are installed in a non-standard location
      # install_requires=["numpy","matplotlib","scipy"],
      classifiers=[
                'Intended Audience :: Other Audience',
                'Intended Audience :: Science/Research',
                'Natural Language :: English',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python',
                'Topic :: Scientific/Engineering',
                'Topic :: Scientific/Engineering :: Mathematics',
                'Topic :: Scientific/Engineering :: Physics',
      ],
)
