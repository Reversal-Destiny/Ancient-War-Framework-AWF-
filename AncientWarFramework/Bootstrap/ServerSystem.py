# -*- coding: utf-8 -*-

# Loader/root-system organization is structurally derived from QuModLibs LoaderSystem,
# but AWF uses one explicit Feature manifest instead of import-side-effect loading.

import mod.server.extraServerApi as serverApi
from AncientWarFramework.Bootstrap.Config import get_config
from AncientWarFramework.Bootstrap.Runtime import FrameworkRuntime

ServerSystem = serverApi.GetServerSystemCls()


class AWFServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.awf = FrameworkRuntime("server", self, get_config())
        self.awf.start()

    def Update(self):
        return ServerSystem.Update(self)

    def Destroy(self):
        self.awf.shutdown()
