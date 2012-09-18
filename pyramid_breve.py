from os import stat
from zope.interface import implements
from pyramid.interfaces import IRendererFactory
from pyramid.path import AssetResolver
from breve import Template
from breve.tags import html


def includeme(config):
    template = Template(html.tags, xmlns=html.xmlns, doctype=html.doctype)
    # is there a better way to get application package?
    loader = BreveAssetLoader(config.registry.__name__)
    config.add_renderer('.b', BreveRendererFactory(template, loader))


class BreveRendererFactory(object):
    implements(IRendererFactory)

    def __init__(self, template, loader):
        self.template = template
        self.loader = loader

    def __call__(self, info):
        name = info.name

        def render(value, system):
            value.update(system)
            return self.template.render(name, value, loader=self.loader)
        
        return render


class BreveAssetLoader(object):

    def __init__(self, package):
        self.resolver = AssetResolver(package)

    def stat(self, name, root):
        if name.endswith('.b.b'):
            name = name[:-2]

        uid = self.resolver.resolve(name).abspath()
        timestamp = stat(uid).st_mtime
        return uid, timestamp

    def load(self, uid):
        return file(uid, 'rb').read()
