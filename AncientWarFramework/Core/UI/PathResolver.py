# -*- coding: utf-8 -*-

class PathResolver(object):
    @staticmethod
    def find_by_suffix(screen_node, root_path, suffix):
        for path in screen_node.GetAllChildrenPath(root_path) or []:
            if path.endswith(suffix):
                return path
        return None

    @staticmethod
    def find_all_by_suffix(screen_node, root_path, suffix):
        return [path for path in (screen_node.GetAllChildrenPath(root_path) or []) if path.endswith(suffix)]

    @staticmethod
    def child_by_name(control, name):
        return control.GetChildByName(name)
