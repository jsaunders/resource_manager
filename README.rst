resource_manager
================

A resource management framework for leasing resources to software developers

This initial application will allow a user to "lease" a file from a remote s3 bucket for local editing.
Upon completion of the lease the changes will be updated in the S3 bucket and the local copy deleted.




Local Deployment
----------------

The following details how to deploy this application using locally using docker and docker-compose

Unless specified, all commands should be run from this repository's root location on the filesystem.

This assumes you do not have docker or docker-compose installed, if you already have them, skip to environment-configuration_.

Installing Docker
^^^^^^^^^^^^^^^^^

1. To install docker, run the following command:

.. code-block:: bash

    curl -sSL https://get.docker.com/ | sh

2. In order to run docker as non root, you must add the desired user to the docker group(Note: substitute "ubuntu" for the user that you wish to run the application with

.. code-block:: bash

    sudo usermod -aG docker ubuntu

3. Reload your bash session and type:

.. code-block:: bash

    docker version

If this command succeeded please continue

If this command does not succeed, please refer to : https://docs.docker.com/engine/installation/linux/ubuntulinux/ and follow their instructions

Installing Docker-Compose
^^^^^^^^^^^^^^^^^^^^^^^^^
1. To install docker-compose, you must run a few commands as root, Start by switching to root:

.. code-block:: bash

    sudo -i

2. Then run:

.. code-block:: bash

    curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

3. Exit root and type:

.. code-block:: bash

    docker-compose version

If this command succeeded, continue
If this command does not succeed, please refer to : https://docs.docker.com/compose/install/ and follow their instructions

.. _environment-configuration:
Environment Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^
* For convenience, an example .env file has been included. Before you run the app, just do:
.. code-block:: bash

   cp env.example .env


If you are going to be accessing this app via localhost in the browser, the only changes you will need to make will be to include your AWS information

This .env file may be further modified to fit your environment

Build Containers and Run Migrations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Execute the following command to build the docker containers:

.. code-block:: bash

    docker-compose build

2. And Run Migrations to setup initial database:

.. code-block:: bash

    docker-compose run django python manage.py migrate

3. Lastly, run the init.sh file as root in order to modify permissions on the shared folder

.. code-block:: bash

    sudo ./init.sh

Run Application
^^^^^^^^^^^^^^^
* After you have installed docker and docker-compose, built the containers, and ran the migrations: to execute the application use the command:
.. code-block:: bash

    docker-compose up

* Or to run in detached mode:
.. code-block:: bash

    docker-compose up -d

* To stop the application, run:
.. code-block:: bash

    docker-compose stop

The application should be accessible in your browser at http://localhost:80


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just load the webapp and localhost:80 and go to Sign Up and fill out the form. Once you submit it,
you'll see a "Successfully signed in" page. You can proceed by clicking the "Home" button and begin leasing resources!

* To create an **superuser account**, use this command (for debug purposes)::

    $ docker-compose run django python manage.py createsuperuser


Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ docker-compose run django coverage run manage.py test
    $ docker-compose run django coverage html
    $ open htmlcov/index.html


