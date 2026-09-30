# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from AncientWarFramework.Bootstrap.Config import get_config
from AncientWarFramework.Bootstrap.Runtime import FrameworkRuntime

ClientSystem = clientApi.GetClientSystemCls()


class AWFClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.awf = FrameworkRuntime("client", self, get_config())
        self.awf.start()

    def Update(self):
        return ClientSystem.Update(self)

    def Destroy(self):
        self.awf.shutdown()
