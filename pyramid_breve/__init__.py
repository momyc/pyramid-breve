from __future__ import absolute_import

from .renderer import BreveRendererFactory


def includeme(config):
    config.add_renderer(u'.b', BreveRendererFactory(config))
