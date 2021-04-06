Local Docker setup under Debian 10
==================================

Under Debian 10, install the ``docker.io`` package::

  apt-get install docker.io

Add intended Docker users to the ``docker`` group by using, for instance::

  adduser <username> docker

It might be necessary to log in again under these user accounts for these changes to take effect. Then as outlined at https://docs.docker.com/get-started/ , one can confirm that Docker is installed properly::

  docker run hello-world
  docker image ls
  docker ps --all

We can now build the Docker image for the website, as described in other sections of this documentation.
