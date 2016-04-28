# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from json import dumps
from logging import getLogger
from settings import JSON_BUCKET


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open(JSON_BUCKET, 'wb')
        self.log = getLogger(__name__)

    def process_item(self, job, spider):
        line = dumps(dict(job)) + '\n'
        self.file.write(line)
        self.log.info('Writing a job from %s to json', spider.name)
        return job
