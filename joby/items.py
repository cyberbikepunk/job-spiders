# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field
from scrapy.loader import Identity, ItemLoader
from scrapy.loader.processors import TakeFirst


class Job(Item):
    website_url = Field(hash_key=True)
    website_language = Field()

    job_url = Field()
    website_job_id = Field()
    company_job_id = Field()

    publication_date = Field()
    days_since_posted = Field()
    reference_id = Field()
    number_of_views = Field()

    contact_email = Field()
    contact_person = Field()
    contact_phone = Field()
    apply_url = Field()

    job_category = Field()
    contract_type = Field()
    workload = Field()
    duration = Field()
    allows_remote = Field()

    job_title = Field(hash_key=True)
    keywords = Field()
    abstract = Field()
    description = Field()

    salary = Field()
    level = Field()

    responsabilities = Field()
    required_skills = Field()
    required_languages = Field()

    company_address = Field()
    company_city = Field()
    company_country = Field()
    company_zipcode = Field()

    company_name = Field()
    company_url = Field()
    company_category = Field()
    company_description = Field()

    start_date = Field()
    end_date = Field()


class JobLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()
