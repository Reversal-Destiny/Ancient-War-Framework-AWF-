# -*- coding: utf-8 -*-

class UIController(object):
    """
    项目 UI ScreenNode 可组合使用的轻量控制基类。
    """

    def __init__(self, screen_node, client_system=None):
        self.screen_node = screen_node
        self.client_system = client_system

    def find_path(self, root_path, suffix):
        from AncientWarFramework.Core.UI.PathResolver import PathResolver
        return PathResolver.find_by_suffix(self.screen_node, root_path, suffix)
