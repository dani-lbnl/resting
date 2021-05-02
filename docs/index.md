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
        * Django REST framework
        * Apache 2
	* PostgreSQL
    * Python 3
    * Sphinx
    
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
 
