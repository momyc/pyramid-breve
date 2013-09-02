from __future__ import absolute_import

from os import stat

from zope.interface import implements, providedBy

from pyramid.interfaces import IRendererFactory
from pyramid.settings import asbool
from pyramid.path import AssetResolver, caller_package

from breve import Template
from breve.tags import html

from .monitor import IFileMonitor, IntervalMonitor


class BreveRendererFactory(object):

    implements(IRendererFactory)

    def __init__(self, config):
        settings = dict((name[6:], value) for name, value in
                        config.registry.settings.items()
                        if name.startswith('breve.'))
        self.tags = config.maybe_dotted(settings.get('tags', html.tags))
        self.doctype = settings.get('doctype', html.doctype)
        if self.doctype and not self.doctype.startswith('<!DOCTYPE '):
            self.doctype = '<!DOCTYPE %s>' % self.doctype
        self.xmlns = settings.get('xmlns', html.xmlns)
        self.fragment = asbool(settings.get('fragment', False))

        if 'monitor' in settings:
            monitor = config.maybe_dotted(settings['monitor'])
            assert IFileMonitor in providedBy(monitor)
        else:
            interval = int(settings.get('monitor_interval', 5))
            monitor = IntervalMonitor(interval)

        default_package = settings.get('default_package', caller_package(6))
        self.loader = TemplateLoader(default_package, monitor)

    def __call__(self, info):

        def render(value, system):
            value.update(system)
            fragment = value.pop('breve_fragment', self.fragment)
            template = Template(self.tags, xmlns=self.xmlns,
                                doctype=self.doctype)
            return template.render(info.name, vars=value, fragment=fragment,
                                   loader=self.loader)

        return render


class TemplateLoader(object):

    def __init__(self, default_package=None, monitor=None):
        self.resolver = AssetResolver(default_package)
        self.monitor = monitor

    def stat(self, name, root):
        name = self.resolver.resolve(name).abspath()
        if name.endswith('.b.b'):
            name = name[:-2]

        if self.monitor is not None:
            timestamp = self.monitor.last_modified(name)
        else:
            timestamp = stat(name).st_mtime
        return name, timestamp

    def load(self, name):
        return file(name, 'rb').read()
