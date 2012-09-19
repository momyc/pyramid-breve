from os import stat
from zope.interface import implements
from pyramid.interfaces import IRendererFactory
from pyramid.path import AssetResolver
from breve import Template
from breve.tags import html


def includeme(config):
    loader = BreveAssetLoader(config.registry.__name__)
    config.add_renderer(u'.b', BreveRendererFactory(loader))


class BreveRendererFactory(object):
    implements(IRendererFactory)

    def __init__(self, loader):
        self.loader = loader

    def __call__(self, info):
        def render(value, system):
            value.update(system)
            template = Template(html.tags, xmlns=html.xmlns, doctype=html.doctype)
            return template.render(info.name, value, loader=self.loader)
        return render


class BreveAssetLoader(object):

    def __init__(self, package):
        self.resolve = AssetResolver(package).resolve

    def stat(self, name, root):
        if name.endswith(u'.b.b'):
            name = name[:-2]

        uid = self.resolve(name).abspath()
        timestamp = stat(uid).st_mtime
        return uid, timestamp

    def load(self, uid):
        return file(uid, 'U').read()
