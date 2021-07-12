# README #

### What is this repository for? ###

* Code for the "REST Interface Generator (RESTInG)" project
* "webserver" directory: context for Docker image containing
    * "apache" directory: Apache 2 configuration files
    * "website" directory: Django website source code
* "postgres" directory: context for Docker image containing PostgreSQL configuration    
* "utils" directory: Python 3 module for simplifying client access to web server using Django REST framework
* "doc" directory: Sphinx documentation for the code in this repository

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
    * Docker
        * Official Python 3 image
            * Includes Django
        * Django REST framework (Python 3 version)
        * Apache 2
	* PostgreSQL
    * Python 3
    * Sphinx (Python 3 version)
    
* Database configuration
    * PostgreSQL is used as the database backend for the web server; setup is described in the documentation.
    
* How to run tests

* Deployment instructions
    * The Docker images produced by this tool are intended for use on the NERSC Spin platform, as described in the documentation.
    
### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Please reference us:
 <div class="row">
      <pre class="col-md-offset-2 col-md-8">
@InProceedings{IKE:2021,
author = {Kenneth Higa and Daniela Ushizima},
title = {REST Interface Generator (RESTInG)},
booktitle = {Transactions on Computational Science & Computational Intelligence, Series Ed.: H. R. Arabina},
month = {Jul},
year = {2021},
pages = {},
publisher = {Springer},
}      </pre>
    </div>
 
### Copyright Notice ###

REST Interface Generator (RESTInG) Copyright (c) 2021, The
Regents of the University of California, through Lawrence Berkeley
National Laboratory (subject to receipt of any required approvals
from the U.S. Dept. of Energy). All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit others to do so.