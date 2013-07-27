import unittest


tags = {}
monitor = object()


class RendererTests(unittest.TestCase):

    def test_includeme(self):
        from pyramid.config import Configurator
        from pyramid_breve.renderer import BreveRendererFactory

        config = Configurator()
        config.include('pyramid_breve')
        config.commit()

        intr = config.registry.introspector.get('renderer factories', u'.b')
        assert isinstance(intr['factory'], BreveRendererFactory)

    def test_factory(self):
        from pyramid.config import Configurator
        from pyramid_breve.renderer import BreveRendererFactory

        for name, value, attr_value in (
            ('tags', '.renderer_tests.tags', tags),
            ('doctype', 'html5', '<!DOCTYPE html5>'),
            ('doctype', '<!DOCTYPE unknown>', '<!DOCTYPE unknown>'),
            ('xmlns', None, None),
            ('fragment', 'on', True),
            ('fragment', 'yes', True),
            ('fragment', 'off', False),
            ('fragment', 'no', False),
        ):
            config = Configurator(settings={'breve.{0}'.format(name): value})
            factory = BreveRendererFactory(config)
            assert getattr(factory, name) == attr_value

        config = Configurator(
            settings={'breve.monitor': '.renderer_tests.monitor'})
        factory = BreveRendererFactory(config)

        assert factory.loader.monitor == monitor

    def test_renderer(self):
        from collections import namedtuple
        from pyramid.config import Configurator
        from pyramid_breve.renderer import BreveRendererFactory

        config = Configurator()
        factory = BreveRendererFactory(config)

        Info = namedtuple('Info', 'name package')

        info = Info('pyramid_breve:tests/template.b', 'pyramid_breve')
        render = factory(info)

        assert isinstance(render({}, {}), basestring)


class LoaderTests(unittest.TestCase):

    def test_stat(self):
        loader = self.loader()

        path, timestamp = loader.stat('pyramid_breve:tests/template.b', None)

        assert path.endswith('/tests/template.b')
        assert isinstance(timestamp, (int, float))

    def test_load(self):
        loader = self.loader()

        path, timestamp = loader.stat('pyramid_breve:tests/template.b', None)
        content = loader.load(path)

        assert content == file(path).read()

    def loader(self, *args, **kwargs):
        from pyramid_breve.renderer import TemplateLoader

        return TemplateLoader(*args, **kwargs)
