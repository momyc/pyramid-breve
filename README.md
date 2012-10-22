=============
pyramid-breve
=============

Breve template engine renderer for Pyramid framework


Usage
-----

Call `config.include('pyramid_breve')` in your WSGI applicatication factory function as following:

```python
def main(global_config, **settings):
    """ This is just an example of how to register renderer for Breve templates.
    """
    config = Configurator(settings=settings)

    config.include('pyramid_breve')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    
    return config.make_wsgi_app()
```

Another way is to add it to `pyramid.includes` in your INI-file:

```
[app:main]
pyramid.includes =
	pyramid_breve
```

Configuration parameters
------------------------

`pyramid_breve.BreveRendererFactory` will pass the following configuration parameters to `breve.Template` constructor:

*	_breve.tags_

	This parameter will be resolved from dotted name string into Python object. By default,
	it is `breve.tags.html.tags`
*	_breve.doctype_

	"<!DOCTYPE html>" or just "html". Default is content of `breve.tags.html.doctype`.
*	_breve.xmlns_

	Will be sent as-is to the constructor. Default is content of `breve.tags.html.xmlns`.


To configure it via INI-file add parameters as following:

```
[app:main]
breve.tags = my_package.breve.tags
breve.doctype = html6
```

Notes
-----

Please note that unlike `breve.Template` which searches for template files under `root` `pyramid_breve` renderer uses `asset specification` to locate
and load templates.

```python
@view_config(route_name='home', renderer='templates/index.b')
def hove_vew(request):
    return {}


@view_config(route_name='login', renderer='my.lovely.package:templates/login.b')
def login_view(request):
    return {}
```
