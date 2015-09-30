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
2.  If you want to use Viper tools as stand-alone commands, or if you
    want to have Silver and Chalice support in your text editor, please
    follow the steps in the subsection `Using Viper`_.
3.  If you want to use IDE for Viper development, please follow the
    steps in the subsection `Developing Viper`_.

-----------
Environment
-----------

Clone repository:

.. code-block:: bash

  hg clone https://bitbucket.org/viperproject/viper-linux-dev

Build Docker image (**note**: this command uses ``sudo`` to get root access):

.. code-block:: bash

  make build_image

**Note:** Dockerfile assumes that your user id is 1000 (default for main
user in most Linux distributions). If it is different, you have to
manually update the Dockerfile and rebuild the image.

Run tests (**note**: this command uses ``sudo`` to get root access):

.. code-block:: bash

  make test

This command runs Silicon, Carbon and Chalice2Silver test suites. If you
need to run the test suite regularly and entering ``sudo`` password each
time annoys you, you can start a shell inside a container and invoke
``sbt`` directly:

.. code-block:: bash

  make shell
  # If succeeded, now you are inside Docker container.
  # To run Chalice2Silver tests, execute:
  cd source/chalice2silver
  sbt test

-----------
Using Viper
-----------

Build packages by using this command (in addition it requires ``gcc``
and ``git`` to be installed):

.. code-block:: bash

  make build-standalone

and add ``bin`` to your ``PATH``.

**Note:** You need to rebuild packages each time you update sources.

Now you should be able to use Silicon and Carbon from the command line:

.. code-block:: bash

  silicon test.sil

**Note:** these Bash scripts under the hood start the Docker container
with `Nailgun <http://www.martiansoftware.com/nailgun/index.html>`_
server. If the server is too slow to start, the first execution of the
script might fail.

You can start the server manually by executing:

.. code-block:: bash

  nailgun-server

You can avoid automatically starting server by passing
``--assume-server-running`` flag:

.. code-block:: bash

  silicon --assume-server-running test.sil

Sublime Text 3
--------------

Requirements:

1.  `Sublime Text 3 <https://www.sublimetext.com/3>`_.
2.  `Package Control <https://packagecontrol.io/installation>`_.
3.  `SublimeLinter 3 <http://www.sublimelinter.com/>`_.

Installation:

1.  Start editor.
2.  Open the Command Palette (``ctrl+shift+p`` on Linux).
3.  Execute ``Package Control: Add Repository`` and
    enter ``https://github.com/vakaras/Sublime-Silver`` to the input
    field.
4.  Open the Command Palette → ``Package Control: Install Package``
    → ``Sublime-Silver``.
5.  Open the Command Palette → ``Package Control: Add Repository`` →
    ``https://github.com/vakaras/SublimeLinter-contrib-silicon``.
6.  Open the Command Palette → ``Package Control: Install Package``
    → ``SublimeLinter-contrib-silicon``.

Usage:

1.  Start Silicon as Nailgun server:

  .. code-block:: bash

    nailgun-server

2.  Start (or restart, if already started) editor.
3.  Open a file with ``.sil`` extension.

VIM
---

Requirements:

1.  Package manager like `Pathogen
<http://www.vim.org/scripts/script.php?script_id=2332>`_
2.  `Syntastic <https://github.com/scrooloose/syntastic>`_

Installation:

1.  Install ``https://github.com/vakaras/vim-silver`` via
    your favorite package manager.

Usage:

1.  Start Silicon as Nailgun server:

  .. code-block:: bash

    nailgun-server

2.  Open a file with ``.sil`` extension.

----------------
Developing Viper
----------------

Docker image has a
`IntelliJ IDEA Community Edition <https://www.jetbrains.com/idea/>`_
installed, which you can use for developing Viper.

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
