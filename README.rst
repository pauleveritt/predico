=================
kaybee_components
=================

A disposable experiment during August 2018 at an architecture for Kaybee and
components. This idea is influenced by Angular, React, Pyramid, and Zope.

If this goes anywhere, it will be thrown away and re-imagined as:

- A package (or multiple packages)

- Possibly using PyScaffold

- Possibly in a kaybee namespace

Implementation-wise, this experiment relies on some other packages:

- Dectate for the registry and configuration system

- pydantic for model schemas and validation

-

Overview
========

- Predicate Registry provides the heart of everything.

- Services provide the pluggable basis for everything

- Views

- Component

- Adapter

- Utility

- Renderers

- Requests

- Configuration

- Schema

- Resolver

Services
========

A service does some work for an application. Services can be part of "the
system" (like the component service), part of an extension (Kaybee might
provide a request service), or your own application (the "Counter" service).

The Service Manager is a configurable, stateful "service" which manages
the various services:

- Take some initial state, whether configuration or otherwise

- Act as a factory that stamps out instances of services (which then stamp
  out instances of "their kind of thing"

- Services can be dependencies and have dependencies

- Services can be overridden and replaced

Some services are singleton-y. For example,