====
News
====

- Make base classes (later, maybe protocols) for View, Adapter, Request,
  etc. to make it easy to jump around in the system and also to issue
  blanket registrations

- Added a ``ServiceManager.add_injectable`` method to formalize
  the API, instead of working with the dict directly.

- Callable adapters. Should have been like this in the first place. If
  an adapter has a ``.__call__``, return the call value instead of the
  adapter instance

- You can use an adapter as the first argument of ``injectedattr``