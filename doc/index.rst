=======
Predico
=======

Building big applications is hard. Building big ecosystems, with different
players plugging in different things in different ways, is even harder.

Predico is a system for such pluggable systems. It learns from experience with
Zope/Pyramid on the Python side and Angular/React on the frontend side to
bring three major pieces together:

- ``Pre`` means predicate registry, a way to expose the smallest surface
  area to overriding in rich, managed ways

- ``di`` means dependency injection, to allow an ecosystem of small
  components which don't depend on the others to get it right

- ``co`` means components, or small, reusable bits of
  presentation/logic/policy

.. note::

    The "co" in Predico -- components -- isn't yet included. It
    mostly works in a side project, but an edge case isn't yet
    supported. It will be described here but clearly marked as "Future".

Predico is built atop Martijn Faassen's
`Dectate <http://dectate.readthedocs.io>`_, a config-oriented registry
system.


.. toctree::
    :maxdepth: 2

    scenario
    tour
    features
    using/index
    developing
    design
    news