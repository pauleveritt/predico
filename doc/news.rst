====
News
====

- ``make_request`` can now use a factory (i.e. a class) specified in
  ``ResourceServiceConfig.factory`` for making the request. Defaults to
  ``CommonRequest``.  This lets systems like Sphinx implement and register
  a ``SphinxRequest`` which maps Sphinx-isms to Predico-isms and can be
  extended with Sphinx-isms such as ``body``, ``prev``, ``next``, etc.

- The idea of ``callable: SomeCallableAdapter`` is flawed, because
  ``SomeCallableAdapter`` isn't the type of ``callable``. Change to
  get make it happen as part of ``injectedattr`` which will change to
  ``injected`` and can handle attr vs. keys and implicitly looks
  for ``__call__`` there. Also, make call=True or call=False arguments
  you can pass to ``injected()``.

- Make base classes (later, maybe protocols) for View, Adapter, Request,
  etc. to make it easy to jump around in the system and also to issue
  blanket registrations

- Added a ``ServiceManager.add_injectable`` method to formalize
  the API, instead of working with the dict directly.

- Callable adapters. Should have been like this in the first place. If
  an adapter has a ``.__call__``, return the call value instead of the
  adapter instance

- You can use an adapter as the first argument of ``injectedattr``