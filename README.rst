=============================
Viper Development Environment
=============================

An environment for developing
`Viper <https://bitbucket.org/viperproject/>`_ on Linux.

Requirements
============

+   `Docker <https://docker.com/>`_

    +   Installation instructions for Ubuntu can be found
        `here <https://docs.docker.com/installation/ubuntulinux/>`_.
    +   How to use docker without sudo can be found
        `here <https://docs.docker.com/installation/ubuntulinux/#giving-non-root-access>`_.

Quick start
===========

Clone repository:

.. code-block:: bash

  hg clone https://bitbucket.org/viperproject/viper-linux-dev

Build Docker image:

.. code-block:: bash

  make build_image

**Note:** Dockerfile assumes that your user id is 1000 (default for main
user in most Linux distributions). If it is different, you have to
manually update the Dockerfile and rebuild the image.

Run tests:

.. code-block:: bash

  make test

Start IntelliJ IDEA:

.. code-block:: bash

  make ide

Follow the instructions of the IntelliJ IDEA setup wizard. On step
“Featured plugins”, install Scala plugin.

Open project: *Open* → ``/home/developer/source/silicon`` (or
``/home/developer/source/carbon`` if you want to develop Carbon instead
of Silicon) → *OK* → Select these items:

+   Use auto-import
+   Project SDK: *New…* → ``/usr/lib/jvm/java-7-oracle`` → *OK*

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

If you want to use a Carbon and Silicon from command line, build
packages by using this command (in addition it requires ``gcc`` and
``git`` to be installed):

.. code-block:: bash

  make build-standalone

and add ``bin/silicon`` and ``bin/carbon`` to your ``PATH``. Now you
should be able to verify Silver file:

.. code-block:: bash

  silicon test.sil

*Note:* these Bash scripts under the hood start the Docker container
with `Nailgun <http://www.martiansoftware.com/nailgun/index.html>`_
server. If the server is too slow to start, the first execution of the
script might fail.

Tips
=====

If you want to get into interactive shell, use:

.. code-block:: bash

  make shell

In the bin directory you can find Bash scripts ``silicon-ide`` and
``carbon-ide`` that can be used to integrate Silicon and Carbon into
text editors. You can find
`Syntastic <https://github.com/scrooloose/syntastic/>`_ based
integration for VIM `here <https://github.com/vakaras/vim-silver>`_.
