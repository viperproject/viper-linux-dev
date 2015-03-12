Viper Development Environment
=============================

An environment for developing
`Viper <https://bitbucket.org/viperproject/>`_ on Linux.

Quick start
===========

Clone repository:

.. code-block:: bash
  
  hg clone https://vakaras@bitbucket.org/vakaras/viper-dev

Run tests:

.. code-block:: bash
  
  make test

Start IntelliJ IDEA:

.. code-block:: bash
  
  make ide-silicon

Install Scala plugin: *Configure* → *Plugins* → *Install JetBrains
plugin…* → Search for “Scala” → *Install plugin* → *Restart
IntelliJ IDEA* → *OK* → *Restart*.

Open project: *Open* → ``/home/developer/source/silicon`` → *OK* →
Select these items:

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
