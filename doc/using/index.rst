=============
Using Predico
=============

Systems built on Predico can be extended in rich and interesting
ways. In this section we look at each of Predico's main pieces, showing
how to write code that extends a system.

.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    *

Dataclasses
===========

Nearly every piece is Predico is organized as a Python 3.7 (3.6 with
backport) dataclass.

See :ref:`dataclasses` for more information.

Configuration
=============

Each piece in Predico can be configured with a custom dataclass. You
instantiate it and the System uses it during startup.

See :ref:`configuration` for more information.

Registry
========

Predico believes in configuration over convention. There's no magic.
Instead, everything gets registered with a registry based on
`Dectate <http://dectate.readthedocs.io>`_ instead of executing at
import time.

See :ref:`registry` for more information.

Services
========

Each piece in Predico -- views, requests, resources, adapters, etc. --
corresponds to a registry action (decorator) but also a service. You can
make new kinds of pieces for other decorators/services.

See :ref:`services` for more information.

Service Manager
===============

Services are bootstrapped in rich ways. The service manager is the
top entry point to everything for services.

See :ref:`service_manager` for more information.

Actions
=======

Each thing in the registry (view, request, etc.) is implemented as a
Dectate action.

See :ref:`actions` for more information.

Predicates
==========

The actions (decorators) are called with arguments called predicates.
These predicates are rich objects which know how to rank themselves
relative to others, whether they participate in lookups, etc.

See :ref:`predicates` for more information.

Resources
=========

Resources model the data part of the system. The Resource Service
provides access to the state and returns instances of registered
resource types, as well as registering resource types.

See :ref:`resources` for more information.

Views
=====

Views model the interaction between the System, a particular Request
into the System, and the rendering output for that Request.

See :ref:`views` for more information.

Renderers
=========

Renderers let you implement different ways of rendering (Jinja2, JSON,
Python Format String) and templating (from a string, file path,
package filename.)

See :ref:`renderers` for more information.

Requests
========

Package up the information from the outside environment for a particular
rendering. Each System implements and registers its own subclass of
Request, e.g. ``SphinxRequest``.

See :ref:`requests` for more information.

Adapters
========

Pluggable, overridable access to most parts of the system. Adapters let
one part (e.g. a BreadcrumbsComponent) get access to another part
(e.g. the Resources in the site) via code the callee (BreadcrumbsComponent)
manages. Adapters can be registered in very particular situations (use
this Logo for all parts of the site *except* underneath this section.)

See :ref:`adapters` for more information.

Components
==========

*Future*. Isolated, renderable units of views plus Jinja2 (or format
string.) Can be used in the middle of a Jinja2 template as an
extension "tag", e.g. ``{% Breadcrumbs depth=10%}``.

See :ref:`components` for more information.
