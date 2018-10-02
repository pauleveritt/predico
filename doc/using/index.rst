=============
Using Predico
=============

Systems built on Predico can be extended in rich and interesting
ways. In this section we look at each of Predico's main pieces, showing
how to write code that extends a system.

.. toctree::
    :maxdepth: 1

Dataclasses
===========

Predico is based on Python dataclasses, a new feature in Python
3.7 with a backport available for Python 3.6. In fact, Predico can optionally
use ``pydantic`` as your dataclass, to give runtime validation.

Why dataclasses? Predico uses them as the interface between the outside
system and the things you register.

We register the view with a decorator from the registry. In this case, we
are registering a "view", which we defined above on the ``MySimpleApp`` registry.

In this registry, ``view`` is an "action". It is passed arguments needed to
correctly register the view. These arguments are all internal to the
definition of the ``view`` action, which says ``for_`` is a required argument.


Configuration
=============

Registry
========

Services
========

Service Manager
===============

Actions
=======

Predicates
==========

Resources
=========

Views
=====

Renderers
=========

Requests
========

Adapters
========

Components
==========
