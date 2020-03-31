# -*- coding: utf-8 -*-


class OutputPipeline(object):
    """This pipeline allows your process to return object
    """
    results = []

    def process_item(self, item, spider):
        self.results.append(dict(item))
