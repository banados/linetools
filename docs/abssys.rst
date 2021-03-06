.. _AbsSystem:

******************
AbsSystem Class
******************

.. index:: AbsSystem

Notebooks
=========

.. toctree::
   :maxdepth: 1

   Simple Examples <AbsSystem_examples>

Overview
========

This Class is designed to organize and analyze an absorption system.
This is generally constructed of one or more :ref:`AbsComponent`.
The base class is abstract, i.e. one must instantiate one of its
flavors (e.g. HILyman, MgII, LLS, DLA).

By definition, an AbsSystem is a unique collection of
absorption components.  It is specified by:

=============== ========   ============== ============================================
Property        Variable   Type           Description
=============== ========   ============== ============================================
RA, DEC         radec      tuple or coord RA,DEC in deg or astropy.coordinate
Redshift        z          float          absorption redshift
Velocity limits vlim       Quantity array -/+ velocity limits of the system
=============== ========   ============== ============================================


Instantiation
=============

The AbsSystem Class may be instantiated in a few ways.
The default sets the properties listed above::

	gensys = GenericAbsSystem((15.23*u.deg,-23.22*u.deg), 1.244, [-500,500]*u.km/u.s, NHI=16.)

More commonly, one will instantiate with one or more AbsComponent objects::

    # HI Lya, Lyb
    radec = SkyCoord(ra=123.1143*u.deg, dec=-12.4321*u.deg)
    lya = AbsLine(1215.670*u.AA)
    lya.analy['vlim'] = [-300.,300.]*u.km/u.s
    lya.attrib['z'] = 2.92939
    lyb = AbsLine(1025.7222*u.AA)
    lyb.analy['vlim'] = [-300.,300.]*u.km/u.s
    lyb.attrib['z'] = lya.attrib['z']
    abscomp = AbsComponent.from_abslines([lya,lyb])
    abscomp.coord = radec
    # Finish
    HIsys = LymanAbsSystem.from_components([abscomp])


One may also instantiate from a *dict*, usually read
from the hard-drive::

    abscomp = AbsSystem.from_dict(idict)

Attributes
==========

Sub Classes
===========

Generic
-------

A catch-all subclass for AbsSystem.
More options are provided in
`pyigm <https://github.com/pyigm/pyigm>`_.


Plots
=====

Methods
=======

AbsLines
--------

There are a few methods related to the AbsLine objects within
an AbsSystem.  One can generate a list of all the AbsLine objects
with::

   lines = abssys.list_of_abslines()

One can retrieve one or more AbsLine objects matching the name
or rest-wavelength of a transition, e.g. ::

   lyb = abssys.get_absline('HI 1025')
   # or
   lyb = abssys.get_absline(1025.72*u.AA)  # Nearest 0.01 A is required


ionN
----

Fill the _ionN attribute with a QTable of column densities.
These are derived from the components ::

   abssys.fill_ionN()
   print(abssys._ionN)

Output
======

One may generate a *dict* of the key properties of the AbsSystem
with the to_dict() method::

   odict = HIsys.to_dict()

This dict is required to be JSON compatible.


