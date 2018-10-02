========
Scenario
========


Imagine we're building a big system atop Sphinx. This system imagines:

- **System**: Sphinx itself as base driving everything

- **Application**: A ready-to-go "app" atop the system, such as
  `ABlog <https://ablog.readthedocs.io>`_

- **Themes**: Packages such as
  `Alabaster <https://alabaster.readthedocs.io/en/latest/>`_ which are
  expected to (a) work with the System (Sphinx) and (b) the Application
  (ABlog) and (c) any of the following to generate compliant HTML

- **Extensions**: Packages such as
  `Napoleon <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/>`_
  to give new capabilities to the System, but consumabable by any
  Application or Theme

- **Customizations**: A particular site using all of this for an
  organization is going to want to (a) assemble pieces and (b) "tweak"
  things (where "tweak" includes unbelievably esoteric demands)

- **Components**: JavaScript-y kinds of things that are the hot new
  rage in modern web development

All these actors are at arm's length from each other, but their stuff needs
to work together. It's a fantastically hard problem.

But one that Predico wants to tackle. Predico hopes to let you make a
``BreadcrumbComponent`` which:

- Works reliably in combinations of the above

- Can easily be customized on a specific page of the site without
  forking the universe

- Could actually work between Sphinx, Flask, Pyramid, etc.

Sounds like an impossible dream. How does Predico plan to do that?

- Break systems up into their pieces (request, resource, view, component,
  or new kinds of things)

- A registry lets those pieces get added to the software in managed, sane
  ways

- Each piece maps to a configurable, stateful service managed by a
  configurable, stateful service manager

- Predicates which let a piece of software get looked up in very specific
  cases (e.g. only for this resource)

- Dependency Injection insulates the callee from the caller, so the
  ``BreadcrumbsComponent`` has some control over its construction

- Existing services for: requests, views, resources, and adapters
  (which can customize each of the others for a particular System,
  Application, etc.)

- (Later) Template components which are isolated, self-contained,
  renderable universes

Predico tries to achieve this not with weirdo machinery. It taps into a
few modern Python features, available in Python 3.6 (with some backports):

- Decorators to manage the connection of a class into the registry

- Dataclasses to govern the construction of the object and provide complete
  encapsulation for that piece's functionality. If you correctly construct
  the dataclass, you have everything.

- Type hints to indicate what kinds of things are needed from/to the system

With Predico, the big picture is decomposed into lots of small surface areas
that can be augmented or replaced in rich, reliable ways.
