from setuptools import setup

long_description = open('README.md').read()

setup(name='gwtools',
      version='1.1.4',
      author='Tousif Islam',
      author_email='tousifislam24@gmail.com',
      packages=['BHPTNRremnant'],
      license='MIT',
      include_package_data=True,
      contributors=[# Alphabetical by last name.""],
      description='Python package for remnant black hole properties using perturbation theory and NR',
      long_description=long_description,
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
