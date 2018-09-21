====
Tour
====

Let's see the high-level look end-to-end.

Scenario
========

Predico was extracted from a system called Kaybee, a "knowledge base" (hence
kb) for Sphinx. Kaybee has a concept of views for resource types. Let's take
a look at working with resources, then views, then the pieces that go with
both.

Registry
========

Systems like this have lots of machinery -- resource types, views, etc. All
these things can come in from lots of places -- the system itself, add-on
packages you ``pip install``, and your own project.

We need something that let's all these pieces register stuff in a managed
way. Python ``import`` isn't good enough. Let's make something called a
``Registry`` and make an instance of it.

Predico's registry is based on ``Dectate`` from Martijn Faassen. Here we
make a registry.

.. note::
    This is usually done by the system/app:

>>> import dectate
>>> class UselessApp(dectate.App):
...     pass

This registry doesn't do anything. Nothing can be registered in it.
Let's solve that by adding in an "action" from Predico to register views.

Views
=====

The concept of view is very familiar in the world of Django, Flask, and
Pyramid. Predico has a built-in "action" that lets your register and locate
views in rich ways. Let's make a registry that understands views:

>>> from kaybee_component.services.view.action import ViewAction
>>> class MySimpleApp(dectate.App):
...     view = dectate.directive(ViewAction)

As a reminder, this is usually in the system you are using, such as Kaybee.

We now have a registry which does stuff. For example, in some
``views.py`` file, I can register a view:

>>> from dataclasses import dataclass
>>> from kaybee_component.services.view.base_view import IndexView
>>> @MySimpleApp.view(for_=IndexView)
... @dataclass
... class ForView:
...     site_name: str = 'Default Site Name'

Let's take a look at what this does.

Dataclasses
-----------

First...Predico is based on Python dataclasses, a new feature in Python
3.7 with a backport available for Python 3.6. In fact, Predico can optionally
use ``pydantic`` as your dataclass, to give runtime validation.

Why dataclasses? Predico uses them as the interface between the outside
system and the things you register.

Decorator
---------

We register the view with a decorator from the registry. In this case, we
are registering a "view", which we defined above on the ``MySimpleApp`` registry.

In this registry, ``view`` is an "action". It is passed arguments needed to
correctly register the view. These arguments are all internal to the
definition of the ``view`` action, which says ``for_`` is a required argument.

We'll see more about this later in the tour when we make a new kind of
registry action.

``IndexView``
-------------

We import the built-in ``IndexView`` and use it as the target of the
``for_`` argument. This is one of the key concepts in Predico. We can use
a system with built-in views, but we can also override them. In this case,
we are overriding any built-in view for the ``IndexView`` target.

Using This View
---------------

Once the system is ready, it "commits" all of its registrations:

>>> dectate.commit(MySimpleApp)

Later, during processing, the system needs to find the best-match for an
``View``:

>>> view_class = ViewAction.get_class(MySimpleApp, 'view', for_=IndexView)
>>> view_instance = view_class()
>>> view_instance.site_name
'Default Site Name'

It found the view that we registered. Big deal -- it's the only thing in
the registry. Let's expand matters a bit to show overriding and finding
views in very specific cases.

Resources
=========

Kaybee lets you model "your kinds of things" as resource types with schemas
and other stuff. Resources can be defined by some system (e.g. Kaybee), some
add-ons for that system (Kaybee Articles), or by your site. Resources can
then be used in rich ways, for example as part of targeted view registrations.

Let's start from the system side by extending the registry above to include
resources:

We're using the Predico built-in concept of resources (the
``ResourceAction``.) With that in place, we can now register some resources:

TODO two resource types

Note that decorator is using ``MyResourceApp``, since the action is on
that registry. Again, this is done by the system you are using (unless you
are writing your own pluggable app.)

We can now make an ``IndexView`` specific to the each kind of resource:

TODO view registrations for both resource types

Let's see if the system can locate the best view in each case:

TODO show location

That's good progress! But what if the view wanted information from the
the resource? In Predico, this is the "di" part: dependency injected.

Dependency Injection
====================

We register things that can be looked up by the system in interesting ways
(a predicate registry.) But these looked-up things need information from the
outside system. They can't always control the caller that uses them.

Instead, the caller asks "the system" to call these things. This allows the
target to tell the system "when you call me, hand me this list of things
that you know about, which I need." This is *dependency injection*.

Let's redo the views above to ask for and use information from the resources:

TODO Views which have