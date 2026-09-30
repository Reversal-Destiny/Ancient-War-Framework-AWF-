# -*- coding: utf-8 -*-

class MemoryBackend(object):
    def __init__(self):
        self.data = {}

    def load(self, subject_id, storage_key):
        return self.data.get((str(subject_id), str(storage_key)))

    def save(self, subject_id, storage_key, value):
        self.data[(str(subject_id), str(storage_key))] = value
        return True

    def delete(self, subject_id, storage_key):
        return self.data.pop((str(subject_id), str(storage_key)), None) is not None


class ModAttrBackend(object):
    def __init__(self, adapter, sync=True):
        self.adapter = adapter
        self.sync = sync

    def load(self, subject_id, storage_key):
        return self.adapter.get_mod_attr(subject_id, storage_key, None)

    def save(self, subject_id, storage_key, value):
        return self.adapter.set_mod_attr(subject_id, storage_key, value, self.sync)

    def delete(self, subject_id, storage_key):
        return self.adapter.set_mod_attr(subject_id, storage_key, None, self.sync)


class ExtraDataBackend(object):
    def __init__(self, adapter, sync=True):
        self.adapter = adapter
        self.sync = sync

    def load(self, subject_id, storage_key):
        return self.adapter.get_extra_data(storage_key, None)

    def save(self, subject_id, storage_key, value):
        return self.adapter.set_extra_data(storage_key, value, self.sync)

    def delete(self, subject_id, storage_key):
        return self.adapter.set_extra_data(storage_key, None, self.sync)


class BlockEntityBackend(object):
    def __init__(self, adapter):
        self.adapter = adapter

    def load(self, subject_id, storage_key):
        data = self.adapter.get_block_entity_data(subject_id)
        if data is None:
            return None
        return data.get(storage_key)

    def save(self, subject_id, storage_key, value):
        data = self.adapter.get_block_entity_data(subject_id)
        if data is None:
            return False
        data[storage_key] = value
        return True

    def delete(self, subject_id, storage_key):
        data = self.adapter.get_block_entity_data(subject_id)
        if data is None or storage_key not in data:
            return False
        del data[storage_key]
        return True
