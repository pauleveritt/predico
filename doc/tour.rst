====
Tour
====

Predico is used to build systems that are extended in rich, productive
ways. To introduce Predico, we'll use an existing sample application in
``predico/sample/__init__.py``.

Hello World
===========

The system will provide a "service manager", the state, logic, configuration,
registry, and more.

Here we ask the sample to make us a working system, then print the *rendered*
*view* of a *resource*:

.. literalinclude:: ../predico/sample/tour/hello_world.py

Lots of magic behind the ``setup`` function, but that's the point: the
person writing the system will wire things up.

Later we'll use the registry outside of the service manager to extend the
system.

Behind The Scenes
=================

Let's unpack some of that magic to see the high-level of how things are
processed.

.. literalinclude:: ../predico/sample/tour/behind_the_scenes.py

- We do the ``setup`` again to populate a working system

- We ask the the ``servicemanager`` to get the ``request`` service

- The ``request`` then makes a request for us, given the id of a resource

- We then ask the ``request`` to help us render some output

Behind the scenes, Predico is doing a good put of "find the best thing".
Let's explore some of that.

First Customization
===================

The sample application has some resource types (Article, Section) and
one generic view for all resource types.

We previously saw the rendered view for ``more/index``, which the sample
application creates as a *Section* resource. Let's register a custom view,
just for Article, and check the output:

.. literalinclude:: ../predico/sample/tour/first_customization.py

Lots more to look at in this one:

- We use Python *decorators* to register this view class (though we can
  also do it "imperatively", done frequently in the tests)

- The decorator use the registry's ``view`` method to add a view with two
  arguments called *predicates*.

- The first predicate says this view is for requests pointed at a
  ``resource`` instances of type ``Resource``

- The second predicate uses simple Python format string processing, using
  the view instance as the input context (other rendering is available)

- Predico is heavily based on Python 3.7 *dataclasses*. We'll show why in a
  moment. *Note: dataclasses are available in 3.6 with a backport.* Our
  View is a dataclass.

If you render ``more/index``, you'll see that this new view doesn't disturb
the output of ``more/index``. That view is still there. Predico uses
predicates to find the best view. This new ``ArticleView`` is registered for
the ``Article`` resource. When the ``resourceid`` matches a resource whose
class is ``Article``, this view is used.

That is the first big idea about Predico. Let's see another example of
predicate matching.


Specific Article
================

Ever seen a Jinja2 template with a whole bunch of ``{% if %}`` testing which
page you're on? In Predico, you can register a view not just for the
resource type at an ID, but for the ID itself:

.. literalinclude:: ../predico/sample/tour/specific_article.py

In this example we register a second view. Instead of a ``resource``
predicate, it has a ``resourceid`` predicate. This view matches exactly
one resource in the system.

That's pretty handy, but sometimes you want to customize a part of your
site. Predico anticipates that with a ``parentid`` predicate which will
match on all resources "under" a part of the site. *Note: Your resources
simply need to implement a ``parentid`` and ``parentids`` as shown in the
sample application.*

So far our view dataclasses only have values that are either defaults or
passed in when the view is created. We don't create the view: the system
does. How do we get data from the outside world into the view?

Current Request
================

Keeping callers and callees at arm's length is a key goal of Predico.
The "di" in Predico stands for dependency injection, and it's used to let
a view ask the *system* to provide needed data, not the caller.

Let's rewrite our ``ArticleView`` to render the title of the current resource:

.. literalinclude:: ../predico/sample/tour/current_request.py

First, our dataclass added ``resource: Resource`` as a dataclass field.
Predico, when constructing the dataclass instance, looks at the field types.
If the field type matches an "injectable" type, that injectable value is
passed in.

We switched the main block back to manually making a request to help
illustrate the chain. The current request runs its render. The current
request is *injectable*. When the request looks for the matching view, it
can construct it because ``Request`` is in the injectables.

Finally, since everything on the view is available in the template, we
render it with ``{request.resource.title}``.

Current Resource
================

Here's another example, injecting the current resource instead of going
through the request:

.. literalinclude:: ../predico/sample/tour/current_resource.py

Not much different, other than showing that ``Resource`` is an injectable.

But let's get into a more interesting form of DI, one which shows the
need for dataclasses.

Resource Title
==============

Predico has custom dataclass fields which arrange the field "metadata" to
communicate with the rest of Predico. In this example we ask that our
view get constructed with just one attribute off of the resource:

.. literalinclude:: ../predico/sample/tour/resource_title.py

Several things to look at:

- ``injected`` is a custom dataclass field. It expects the first argument
  be an injectable (or an adapter...more on that later). The field can also
  supply ``attr``, ``key``, or leave nothing and the first argument will
  have its ``__call__`` invoked if present.

- The ``str`` refers to the type of what is expected from the right-hand side.
  Predico doesn't want to hijack the type to mean something it doesn't.

- The template string now can point to just the variable it needs

Why all this machinery? Predico wants each unit to expose, and be exposed to,
the smallest surface area necessary. This is a big lesson from systems like
React and Angular. With this, you could construct a view instance with
just a string, instead of a huge "request" with who-knows-what contracts
in it.

Predico's dependency injection (DI) system is pretty useful. Let's show
some extra power that can solve real problems in large-scale ecosystems.

Breadcrumbs
===========

Views are dataclasses, which are...classes. They can have properties and
methods. Let's implement breadcrumbs, which show the parents plus the
current resource.

.. literalinclude:: ../predico/sample/tour/breadcrumbs.py

It's a little busier, but it's doing a lot. The view now has its own
logic in the ``breadcrumbs`` property. It walks up the parents to the
root, collecting resources via their ``id``. The visual representation is in
the ``breadcrumb_titles`` property, used in the template string.

But this is bringing a lot into the view. We'd prefer to have lots of little,
reusable pieces. Let's move ``breadcrumbs`` to an "adapter", then show a
follow-on that explains the big idea on breadcrumbs.

First Adapter
=============

We can make our view dumber by make a *adapter* which collects the data for
the breadcrumbs on a particular resource.

.. literalinclude:: ../predico/sample/tour/first_adapter.py

We start by defining a "kind of thing" called Breadcrumbs that we want
to work with. Views can then say: "Give me a Breadcrumbs instance" and
Predico will go off and find the best fit.

In this case we've just registered one *adapter* that can make a Breadcrumbs.
All the logic about what is needed for Breadcrumbs is moved off of the view,
onto this class. Like views, adapters participate in DI and can ask the system
to hand them stuff.

This is important. It decouples the caller (the view) from the callee (the
adapter.) If you have lots of potential callers -- a system, an
application built on the system, a theme, some components, some views -- it
will be hard to keep them all coordinated on what to pass into Breadcrumbs.

The ``BreadcrumbsAdapter`` class defines a ``__call__`` which does its work.

Then, the view can simply say ``breadcrumbs: Breadcrumbs`` and the system
will (a) find the best class, (b) use DI to instantiate it, and (c) use DI
again to add it to the constructor for the view.

Pretty sweet. But what if we we say Section resources shouldn't have
breadcrumbs? Or this particular artical at this ID should have a prefix put
on the last title?

Adapters are part of predicates. So let's make a more specific adapter.

Specific Adapter
================

Let's make a policy that Section resources don't show the root home page
in the list of breadcrumbs. We'll make a ``SectionBreadcrumbsAdapter``.

.. literalinclude:: ../predico/sample/tour/specific_adapter.py

When we change the ``resourceid`` at the bottom to render a Section
resource instead of some other resource type, we see the new behavior.
``Home Page`` isn't listed in the breadcrumbs.

(Future) Components
===================

The last syllable of Predico is missing. As explained in
:doc:`../using/index`, the work on components isn't finished. But
briefly:

- Components are like in React (or even moreso, Angular): standalone
  units of data, templating, and rendering

- They manifest themselves as Jinja2 extensions, so the components
  you write an be used in your Jinja2 view templates

- For example ``{% Breadcrumbs %}`` would map to a dataclass registered
  to a component

- The Breadcrumbs component can use passed in props for its data, e.g.
  ``{% Breadcrumbs root=True, resources=resources %}``

- But the component can also use DI to get data such as resources, without
  the caller needing to pass it in
