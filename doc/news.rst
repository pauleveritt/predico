====
News
====

- Callable adapters. Should have been like this in the first place. If
  an adapter has a ``.__call__``, return the call value instead of the
  adapter instance

- You can use an adapter as the first argument of ``injectedattr``