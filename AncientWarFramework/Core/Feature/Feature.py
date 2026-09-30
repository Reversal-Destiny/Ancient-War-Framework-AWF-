# -*- coding: utf-8 -*-

class Feature(object):
    feature_id = None
    dependencies = ()
    sides = ("server", "client")

    def __init__(self, runtime):
        self.runtime = runtime

    def register(self):
        """
        REGISTER 阶段：注册 Registry、Service、静态定义。
        """
        pass

    def resolve(self):
        """
        RESOLVE 阶段：获取依赖 Service 并完成交叉绑定。
        """
        pass

    def enable(self):
        """
        FREEZE 后启用运行期逻辑。
        """
        pass

    def disable(self):
        """
        SHUTDOWN 前逆序关闭。
        """
        pass
