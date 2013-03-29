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

There are few configuration parameters that control rendering. They can be set in INI-file as following:

```
[app:main]
# other application parameters ...

breve.tags = my_package.breve.tags
breve.doctype = html
breve.fragment = on
```

Breve renderer accepts following parameters:

*	_breve.tags_

	This parameter will be resolved from dotted name string into Python object.
	Default is `breve.tags.html.tags`.
*	_breve.doctype_

	"<!DOCTYPE html>" or just "html".
	Default is content of `breve.tags.html.doctype`.
*	_breve.xmlns_

	Will be sent as-is to the constructor.
	Default is content of `breve.tags.html.xmlns`.
*	_breve.fragment_

	This boolean variable will be used as `fragment` parameter to breve.Template.render call. This parameter
	can also be controlled by setting `breve_fragment` template variable as following:

```python

@view_config(renderer='templates/home.b')
def home_view(request):
    return {
        # other variables used in template
        'breve_fragment': True,
        }
```

	Template variable `breve_fragment` overrides global `breve.fragment` setting. If none is set default is False.


Notes
-----

Please note that unlike `breve.Template` which searches for template files under `root` `pyramid_breve` renderer uses `asset specification` to locate
and load templates.

```python
@view_config(route_name='home', renderer='templates/index.b')
def home_view(request):
    return {}


@view_config(route_name='login', renderer='my.lovely.package:templates/login.b')
def login_view(request):
    return {}
```
