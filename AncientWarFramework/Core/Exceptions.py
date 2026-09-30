# -*- coding: utf-8 -*-

class AWFError(Exception):
    """
    AWF 基础异常。
    """


class ConfigurationError(AWFError):
    """
    框架配置错误。
    """


class FeatureError(AWFError):
    """
    Feature 生命周期或依赖错误。
    """


class FeatureDependencyError(FeatureError):
    """
    Feature 依赖缺失或存在循环。
    """


class RegistryError(AWFError):
    """
    Registry 基础异常。
    """


class RegistryConflictError(RegistryError):
    """
    Registry key 重复。
    """


class RegistryFrozenError(RegistryError):
    """
    Registry 冻结后发生非法变更。
    """


class ServiceError(AWFError):
    """
    Service 容器错误。
    """


class RPCError(AWFError):
    """
    RPC 协议或 endpoint 错误。
    """


class DataError(AWFError):
    """
    数据模型/Repository 错误。
    """


class DataMigrationError(DataError):
    """
    持久化数据迁移失败。
    """
