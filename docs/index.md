# README #

### What is this repository for? ###

* Code for the "REST Interface Generator (RESTInG)" project
* "webserver" directory: context for Docker image containing
    * "apache" directory: Apache 2 configuration files
    * "ssl" directory:
    * "website" directory: Django website source code
* "postgres" directory: context for Docker image containing PostgreSQL configuration    
* "resting" directory: Python 3 module for simplifying client access to web server using Django REST framework
* "doc" directory: Sphinx documentation for the code in this repository

### How do I get set up? ###

* Several software packages must be available on the computer on which RESTInG will be run, which we will call the "development system."
  * On a Debian 10 computer, run as root (or with sudo): "apt-get install git python3 python3-sphinx"
  * On a Mac OS X computer, as an Administrator:
    * Open a Terminal and run "git"; if you receive an error, you may need to run "xcode-select --install" (see https://apple.stackexchange.com/questions/254380/why-am-i-getting-an-invalid-active-developer-path-when-attempting-to-use-git-a).
    * Install the Sphinx Documentation Generator using one of the options described here: https://www.sphinx-doc.org/en/master/usage/installation.html
      * Running "pip3 install -U sphinx" in a Terminal is likely the easiest approach
  * On a Windows 10 computer, as an Administrator:
    * Install Cygwin (download setup-x86_64.exe from http://www.cygwin.org/ and verify the file using the available signature), and through the Cygwin Setup program, mark the latest versions of the git, python39, python39-sphinx, python39-sphinxcontrib-applehelp, python39-sphinxcontrib-devhelp, python39-sphinxcontrib-htmlhelp, python39-sphinxcontrib-qthelp, and python39-alabaster packages for installation.
* From a terminal window (Linux or Mac) or a Cygwin terminal (Windows):
  * Clone the RESTInG repository by running "git clone https://github.com/dani-lbnl/resting.git".
  * Build the documentation: from the "resting" subdirectory of the cloned repository, run sphinx.sh using "./sphinx.sh" or a command such as "bash sphinx.sh". The script will provide the name of a local file (and a corresponding URL) for the documentation index, which can be viewed with a web browser. Unfortunately, under Cygwin on a Windows computer, the file path is only recognizable to programs installed under Cygwin, so one will typically instead direct a web browser to a file such as "C:\cygwin64\home\<username>\resting\doc\_build\html\index.html", or a corresponding URL such as "file:///C:/cygwin64/home/<username>/resting/doc/_build/html/index.html"
  * Click on the "Setup" link on the documentation page for continued setup instructions.
    
### Contribution guidelines ###
* Writing tests
* Code review
* Other guidelines
   
### Example of deployment
- Please see a [covidscreen.lbl.gov](https://covidscreen.lbl.gov/) for an example

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
