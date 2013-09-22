pyramid-breve
=============

`Breve <http://breve.twisty-industries.com/>`_ template engine renderer for
`Pyramid <http://www.pylonsproject.org/>`_ framework that uses 
`asset specification <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/assets.html>`_
to locate and load templates.
Latest source code and bug tracker are avaliable at `GitHub <http://github.com/momyc/pyramid-breve>`_.


Usage
-----

Call ``config.include('pyramid_breve')`` in your `WSGI <http://wsgi.org/>`_
applicatication factory function as following:

.. code:: python

        def main(global_config, ````settings):
            config = Configurator(settings=settings)

            config.include('pyramid_breve')

            config.add_static_view('static', 'static', cache_max_age=3600)
            config.scan()

            return config.make_wsgi_app()

Another way is to add it to ``pyramid.includes`` in your INI-file:

.. code:: ini

        [app:main]
        pyramid.includes = pyramid_breve


Now use it to render templates:

.. code:: python

        # using absolute asset specification
        @view_config(route_name='home', renderer='my.lovely.app:templates/home.b')
        def home_view(request):
            return {real: 'content'}

        # using relative asset specification
        @view_config(route_name='login', renderer='templates/login.b')
        def login_view(request):


Configuration parameters
------------------------

There are few configuration parameters that control rendering. They can be set in
INI-file as following:

.. code:: ini

        [app:main]
        breve.tags = my_package.breve.tags
        breve.doctype = html
        # optionally, enforce default package name if pyramid-breve fails to detect it
        breve.default_package = myapp

Breve renderer accepts following parameters:

``breve.default_package``
	Package name to use for resolving ``relative asset specifications``, i.e. assets without explicit package
	name. Pyramid-breve tries to detect your application name and use it as default package name but it's
	a tricky business and this parameter allowes to enforce default package name.
 
``breve.tags``
	This parameter will be resolved from dotted name string into Python object.
	Default is ``breve.tags.html.tags``.

``breve.doctype``
	"<!DOCTYPE html>" or just "html".
	Default is content of ``breve.tags.html.doctype``.

``breve.xmlns``
	Will be sent as-is to the constructor.
	Default is content of ``breve.tags.html.xmlns``.

``breve.fragment``
	This boolean variable will be used as ``fragment`` parameter to
	breve.Template.render call. This parameter can also be controlled by setting
	``breve_fragment`` template variable as following:

.. code:: python

        @view_config(renderer='templates/home.b')
        def home_view(request):
            return {
                # other variables used in template
                'breve_fragment': True,
                }

Template variable ``breve_fragment`` overrides global ``breve.fragment`` setting.
If none is set default is False.


Template file modification monitoring
-------------------------------------

Starting from version 0.6dev there is ``pyramid_breve.monitor.IFileMonitor`` interface.
Implementations of that interface can be used to help ``pyramid_breve.renderer.TemplateLoader``
to get template file status without calling os.stat each time template is about to be rendered.

There is ``pyramid_breve.monitor.IntervalMonitor`` implementation of that interface which is used
by ``BreveRendererFactory`` by default. That class simply caches os.stat value for fixed amount
of time. Its constructor accepts single parameter ``interval`` that should be interval in seconds
between invalidating cached values. This parameter can be configure via INI-file variable
``breve.monitor_interval`` like following:

.. code:: ini

        [app:main]
        # cache os.stat calls for 15 seconds
        breve.monitor_interval = 15

It is possible to implement custom ``IFileMonitor`` using more advanced techiques,
like ``inotify`` or ``File Alteration Monitor`` features. 

Lets create simple ``IFileMonitor`` implementation and configure ``pyramid_breve`` to
use it.

First, we need to implement ``IFileMonitor`` interface:

.. code:: python

        # myapp/utils.py

        from zope.interface import implements
        from pyramid_breve.monitor import IFileMonitor

        class DummyMonitor(object):

            implements(IFileMonitor)

            def last_modified(self, name):
                # Never even look at real modification time and
                #  templates being cached forever once it's loaded
                return 0

        monitor = DummyMonitor()

Use ``breve.monitor`` variable in INI-file:

.. code:: ini

        [app:main]
        breve.monitor = myapp.utils.monitor

