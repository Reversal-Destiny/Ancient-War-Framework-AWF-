# -*- coding: utf-8 -*-

from AncientWarFramework.Core.Event.Decorators import engine_event
from AncientWarFramework.Core.Feature.Feature import Feature
from AncientWarFramework.Core.UI.ScreenManager import ScreenManager
from AncientWarFramework.Core.UI.UIRegistry import UIRegistry


class UIInfrastructureFeature(Feature):
    feature_id = "ui"
    sides = ("client",)

    def register(self):
        """
        注册客户端 UI Registry 与 ScreenManager。
        """
        registry = self.runtime.registries.register(UIRegistry(self.runtime))
        self.runtime.services.register("ui", ScreenManager(self.runtime, registry))

    @engine_event("UiInitFinished")
    def on_ui_init_finished(self, event):
        """
        在网易 UI 初始化完成后统一注册项目声明的 Screen。
        """
        self.runtime.services.require("ui").register_all()
