# README #

[Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Bitbucket access ###

I was unable to clone using HTTPS and Google/LBNL login. However, going to "Personal settings"; "SSH keys" on the Bitbucket site and copying in an SSH public key gave me passwordless SSH access to the repository.

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Code for the "ACTS: Amplifying COVID-19 Testing and Surveillance" project
* "webserver" directory: context for Docker image containing
    * "apache" directory: Apache 2 configuration files
    * "website" directory: Django website source code
* "postgres" directory: context for Docker image containing PostgreSQL configuration    
* "client" directory: Python 3 module for simplifying client access to web server using Django REST framework
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
    * The Docker containers described by this repository are intended for use on the NERSC Spin system, as described in the documentation.
    
### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines
