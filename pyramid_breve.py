from os import stat
import re
from zope.interface import implements
from pyramid.interfaces import IRendererFactory
from pyramid.path import AssetResolver, DottedNameResolver
from breve import Template
from breve.tags import html


def includeme(config):
    config.add_renderer(u'.b', BreveRendererFactory(config))


class BreveRendererFactory(object):
    implements(IRendererFactory)

    tags = html.tags
    doctype = html.doctype
    xmlns = html.xmlns

    def __init__(self, config):
        registry = config.registry
        self.loader = BreveAssetLoader(registry.__name__)

        settings = dict((name[6:], value) for name, value in registry.settings.items() if name.startswith('breve.'))

        self.tags = config.maybe_dotted(settings.get('tags', self.tags))

        self.doctype = settings.get('doctype', self.doctype)
        if self.doctype and not self.doctype.startswith('<!DOCTYPE '):
            self.doctype = '<!DOCTYPE %s>' % self.doctype

        self.xmlns = settings.get('xmlns', self.xmlns)

    def __call__(self, info):
        def render(value, system):
            value.update(system)
            template = Template(self.tags, xmlns=self.xmlns, doctype=self.doctype)
            return template.render(info.name, vars=value, loader=self.loader)
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
