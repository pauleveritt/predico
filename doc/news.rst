====
News
====

- New request.adapt_resource(SomeAdapter, some_resource) finds the right
  adapter for the passed in resource *and* makes that resource the one
  used for DI on the returned adapter instance. Uses existing
  ``props`` feature which has higher precedence than injectables or
  adapters.

- ``get_adapter`` only worked on the resource/resourceid/parentid of
  ``request.resource``. Now allow ``adapter_service.get_adapter`` to
  pass in ``resource=some_resource`` to override usage of
  ``request.resource``

- Fixed ``call=False``, the flag wasn't being looked at correctly.

- Have the injector do ``field.metadata.get(attr, None)``
  instead of ``field.metadata[attr]`` to allow missing values
  to report back with None

- Make ``Resources`` an injectable, pointed at
  ``services['resources'].resources`` which is now an instance of
  ``Resources(dict)``

- Allow ``make_request`` to pass in props from the outside, e.g.
  Sphinx pagename, body, prev, next from the page context

- Forgot to hook up requestservice.config.factory to actually be used in
  ``make_request``

- Initial implementation of rendering. Add an option to the ``view``
  decorator that allows providing some rendering information via an
  adapter. Then add ``request.render`` to make it transparent.

- Get rid of ``for_`` on views.

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