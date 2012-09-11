from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.b')
def home_view(request):
    return {'project':'my_app'}
