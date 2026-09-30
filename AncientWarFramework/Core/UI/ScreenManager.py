# -*- coding: utf-8 -*-

class ScreenManager(object):
    def __init__(self, runtime, registry):
        self.runtime = runtime
        self.registry = registry
        self.registered = set()
        self.instances = {}

    def register_all(self):
        api = self.runtime.adapter.api
        for screen_id, info in self.registry.items():
            api.RegisterUI(self.runtime.config.mod_name, info["ui_name"], info["python_path"], info["screen_def"])
            self.registered.add(screen_id)

    def create(self, screen_id, options=None):
        info = self.registry.require(screen_id)
        options = dict(options or {})
        if "isHud" not in options:
            options["isHud"] = 1 if info.get("is_hud") else 0
        ui = self.runtime.adapter.api.CreateUI(self.runtime.config.mod_name, info["ui_name"], options)
        self.instances[screen_id] = ui
        return ui

    def get(self, screen_id):
        return self.instances.get(screen_id)

    def remove(self, screen_id):
        ui = self.instances.pop(screen_id, None)
        if ui and hasattr(ui, "SetRemove"):
            ui.SetRemove()
        return ui is not None
