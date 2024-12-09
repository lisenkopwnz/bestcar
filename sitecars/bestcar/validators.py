import logging

from django.utils import timezone

from django.core.exceptions import ValidationError

import inspect

logger = logging.getLogger('duration_request_view')

class Validators_date_model:
    def __init__(self, message='Ведите коректную дату.'):
        self.message = message

    def __call__(self, value):
        now = timezone.now()
        logger.info(now)
        logger.info(value)
        if value < now:
            raise ValidationError(self.message)

    def deconstruct(self):
        path = "%s.%s" % (
            inspect.getmodule(self).__name__,
            self.__class__.__name__,
        )
        return path, (), {}
