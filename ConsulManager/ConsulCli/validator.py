from prompt_toolkit.validation import Validator, ValidationError
import re

class dateValidator(Validator):
    def validate(self, document):
        ok = re.match(r'\d\d\/\d\d\/\d\d\d\d', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid date (DD/MM/YYYY)',
                cursor_position=len(document.text))  # Move cursor to end

class MontoValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message='Porfavor, seleciona un monto valido',
                cursor_position=len(document.text))