""" Custom contract classes. """

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail
from scrapy.item import BaseItem


class ProcessingContract(Contract):
    """ Check if fields have been scraped and processed correctly.

    @pipeline field_name field_value_after_processing

    """
    name = 'pipeline'

    def post_process(self, outputs):
        for output in outputs:
            if isinstance(output, BaseItem):
                # noinspection PyTypeChecker
                item = dict(output)
                field_name = self.args[0]
                expected_value = ' '.join(self.args[1:])
                scraped_value = item[field_name]

                if field_name not in item.keys():
                    raise ContractFail('%s field is missing' % field_name)

                if scraped_value != expected_value:
                    parameters = (field_name, expected_value, scraped_value)
                    raise ContractFail('%s field expecting %s, scraped %s' % parameters)
