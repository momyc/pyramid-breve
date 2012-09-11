from os import stat
from zope.interface import implements
from pyramid.interfaces import IRendererFactory, ITemplateRenderer
from pyramid.path import AssetResolver, caller_package
from breve import Template
from breve.tags import html


def includeme(config):
    template = Template(html.tags, xmlns=html.xmlns, doctype=html.doctype)
    loader = BreveAssetLoader(caller_package(3))
    config.add_renderer('.b', BreveRendererFactory(template, loader))


class BreveRendererFactory(object):

    def __init__(self, template, loader=None):
        self.loader = loader
        self.template = template

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
        timestamp = stat(uid)
        return uid, timestamp

    def load(self, uid):
        return file(uid, 'rb').read()

