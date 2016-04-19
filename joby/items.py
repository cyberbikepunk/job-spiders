# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field
from scrapy.loader import Identity, ItemLoader
from scrapy.loader.processors import TakeFirst


class JobItem(Item):
    website_url = Field()
    website_language = Field()

    publication_date = Field()
    posting_id = Field()
    url = Field()
    number_of_views = Field()

    contact_email = Field()
    contact_name = Field()

    employment_type = Field()
    workload = Field()
    duration = Field()
    remote = Field()

    title = Field(primary_key=True)
    keywords = Field()
    abstract = Field()
    description = Field()

    salary = Field()
    level = Field()

    responsabilities = Field()
    required_skills = Field()
    required_languages = Field()

    company = Field(primary_key=True)
    city = Field()
    country = Field()
    postal_code = Field()

    company_website = Field()
    company_category = Field()
    company_description = Field()

    start_date = Field()
    end_date = Field()


class DataScienceJobsJobItem(JobItem):
    pass


class JobItemLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()


class DataScienceJobsItemLoader(JobItemLoader):
    pass
