======
Design
======

What's the architecture and design behind Predico? In this document we cover
some of the internals and decisions.

Predicate Action
================

Dectate's key idea is *actions* in a registry. Each action corresponds to
a directive which configures a part of the registry. Each of these registry
parts have their own policies, semantics, meaning, etc.

Predicate actions are a particular kind of Dectate action. They support the
goal of overriding and finding the best registration.

For example, an app might have a concept of a *view*. So its registry has a
view action and you can register classes as views using the decorator.

The app might have some built-in views, but wants to allow projects the
option of replacing some of those views with their own custom views. This
is *overriding*.

Or the project might want to have different flavors for a view in different
circumstances. The ``IndexView`` for an ``Article`` might be different than
the ``IndexView`` for a ``Section``.

As an extreme case, the ``IndexView`` for a specific article -- say, at
``/geography/continents/africa`` -- might need to be overridden.

Predicate actions make it easy to write a Dectate action which supports
multiple registrations of one thing then finding the best-match later.

Predicates
==========

When registering something, the arguments you provide to the decorator are
the predicates. They are usually (but not always) used in the best-match
lookup of the right registration for an action.

Predicates are their own objects and can have their own metadata, for
example how to determine whether it matches and what is the weight for that
predicate (meaning, some predicates are more important than others.)

Services
========

That's the system for looking up a registration. You can then make an
instance of the class -- for example, a view -- and merrily proceed.

Except, larger systems are more complex than that. The view machinery might
have some configuration it needs from the system. It might maintain some
state. It might have some special rules it obeys when it constructs its
instances, or provide some helpers.

Thus, each action corresponds to a service. The view service, for example,
is a factory instance which makes view instances.

Service Manager
===============



- Best match

- Custom vocabulary for an action

- Based on dectate