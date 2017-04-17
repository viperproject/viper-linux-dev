=============================
Viper Development Environment
=============================

An environment for developing and using `Viper
<http://www.pm.inf.ethz.ch/research/viper.html>`_ on Linux.

Requirements
============

+   `Docker <https://docker.com/>`_

    +   Installation instructions for Ubuntu can be found
        `here <https://docs.docker.com/installation/ubuntulinux/>`_.

Quick Start
===========

1.  As a first step, please follow the instructions in the subsection
    `Environment`_ to set up the environment.
2.  If you want to use IDE for Viper development, please follow the
    steps in the subsection `Developing Viper`_.

-----------
Environment
-----------

Clone repository and ``cd`` into it:

.. code-block:: bash

  hg clone https://bitbucket.org/viperproject/viper-linux-dev
  cd viper-linux-dev

Build Docker image (**note**: this command uses ``sudo`` to get root access):

.. code-block:: bash

  make build_image

Start container (**note**: this command uses ``sudo`` to get root access):

.. code-block:: bash

  make start_server

Connect to the container and run Chalice2Viper tests:

.. code-block:: bash

  make connect
  # If succeeded, now you are inside Docker container.
  # To run Silicon tests, execute:
  cd source/silicon
  sbt test
  # Similarly, to run Carbon tests, execute:
  cd
  cd source/carbon
  sbt test

----------------
Developing Viper
----------------

Docker image has a
`IntelliJ IDEA Community Edition <https://www.jetbrains.com/idea/>`_
installed, which you can use for developing Viper.

Connect to container and start IntelliJ IDEA:

.. code-block:: bash

  make connect
  idea

Follow the instructions of the IntelliJ IDEA setup wizard. On step
“Featured plugins”, install Scala plugin.

Open project: *Open* → ``/home/developer/source/silicon`` (or
``/home/developer/source/carbon`` if you want to develop Carbon instead
of Silicon) → *OK* → Select these items:

+   Use auto-import
+   Project SDK: *New…* → ``/usr/lib/jvm/java-8-oracle`` → *OK*

Press *OK*.

If you want to have the ``sbt test`` and ``sbt compile`` targets:

#.  Open the *Edit Configurations…* window by pressing Shift key twice, typing
    “Edit Configurations” and pressing Enter.
#.  Create new *SBT Task*:

    +   Name: *Test*
    +   Tasks: *test*
    +   Remove *Make* from *Before launch*

#.  Create new *SBT Task*:

    +   Name: *Compile*
    +   Tasks: *compile*
    +   Remove *Make* from *Before launch*

*Note:* It is expected that IntelliJ cannot find ``brandingData``. Just
ignore this error.

Tips
=====

-----------------
Building Packages
-----------------

Debian
======

To create debian packages:

.. code-block:: bash

    make connect
    cd ~/source/silicon/
    sbt stage
    cd ~/source/carbon/
    sbt stage
    cd ~
    # Assuming repo is a symlink to a folder served by HTTP server:
    /home/developer/source/packaging/create.py debian /home/developer/repo
    cd repo
    ~/source/bin/debian_package

Homebrew
========

Build files and upload to the Bintray repository:

.. code-block:: bash

    make package_homebrew

Update the Homebrew formula:

.. code-block:: bash

    cd homebrew
    cp ../workspace/package/homebrew/*.rb .
    git add *.rb
    git commmit -m "New version."
    git push
