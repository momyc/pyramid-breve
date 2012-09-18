pyramid-breve
=============

Breve template engine renderer for Pyramid framework



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
use = egg:hello_world

pyramid.includes =
	pyramid_breve
```


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
