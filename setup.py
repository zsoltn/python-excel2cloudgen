#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems Kurt Garloff, Zsolt Nagy

import os
from setuptools import setup, find_packages
import platform

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files= package_files('excelcloud/terraform') + package_files('excelcloud/excels')

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
   
    
long_description = (
    read('README.rst')
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(name='python-excel2cloudgen',
			version=read('VER').strip(),
			description='ExcelCloud Client Tool',
			long_description=long_description,
			url='https://github.com/OpenTelekomCloud/python-excelcloud',
			author='Zsolt Nagy',
			author_email='Z.Nagy@t-systems.com',
			license='MIT License',
			packages=find_packages(),
            include_package_data=True, 
            package_data={
                '': extra_files,
                },
			keywords="otc, openstack, cloud, devops, t-systems, aws, azure",
			classifiers=[
				"Development Status :: 6 - Mature",
				"Intended Audience :: Developers",
				"Intended Audience :: Science/Research",
				"License :: OSI Approved :: MIT License",
				"Programming Language :: Python",
				"Topic :: Software Development :: Libraries :: Python Modules"
			],
			zip_safe=False,
			entry_points = {
				'console_scripts': [
					'excelcloud = excelcloud.excelcloud:main'
				]
			},
			test_suite="tests"
            ,data_files=[],                         
            install_requires=['requests', 'python-terraform', 'watchdog','xlwt','xlrd','wsgidav','cheroot'], 
            #,data_files=[man_file]
		)
# this will be excelcloud --init terraform command 
#from excelcloud.utils_directory import download_terraform
#download_terraform()
#from excelcloud.providers.otc.terraform.utils_terraform import startTerraform
#startTerraform(init=True)
