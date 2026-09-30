# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Registry.Registry import Registry


class UIRegistry(Registry):
    def __init__(self, runtime=None):
        Registry.__init__(self, "ui", runtime)

    def register_screen(self, screen_id, ui_name, python_path, screen_def, is_hud=False, source=None):
        return self.register(screen_id, {
            "id": screen_id,
            "ui_name": ui_name,
            "python_path": python_path,
            "screen_def": screen_def,
            "is_hud": bool(is_hud),
        }, source)
