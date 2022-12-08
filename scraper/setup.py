from setuptools import setup, find_packages
setup(name='scraper',
      version='0.1',
      description='scraper for the web platforms',
      url='https://github.com/saikishan/cap_report_generator',
      author='sai kishan',
      author_email='saikishan2008@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'arrow==0.12.1',
            'beautifulsoup4==4.6.3',
            'bs4==0.0.1',
            'certifi==2022.12.7',
            'chardet==3.0.4',
            'idna==2.8',
            'python-dateutil==2.7.5',
            'requests==2.21.0',
            'urllib3==1.24.1'],
      zip_safe=False)