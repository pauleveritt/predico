"""

A ServiceManager that manages registered services.

We need a single entry point for the various kinds of things we want
to do -- views, renderers, etc. This single entry point needs:

- Initial configuration

- State

- A way to discover and register services

- A way to retrieve services

Each service needs:

- A way to register with the service manager

- An entry point, called by the service manager, to do setup

- Initial configuration

- State

- Registry

- A reference back to the service manager

"""
