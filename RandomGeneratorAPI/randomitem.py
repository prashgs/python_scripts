import json

from mimesis.schema import Field, Schema
from pydantic import BaseModel, validator

class RandomItem(BaseModel):
    input_json_string: str = None
    output_json_string: str = None

    @validator('input_json_string')
    def validate_json(cls, input_json_string):
        if not app.is_json(input_json_string):
            raise ValueError('Invalid Json text')
        else:
            cls.input_json_string = json.loads(input_json_string)
        return input_json_string

    @classmethod
    def parse_json(cls, number=1):
        output_list = []
        cls.output_json_string = cls.input_json_string
        if cls.output_json_string is not None:
            description = (lambda: cls.output_json_string)
            schema = Schema(schema=description)
            output_list = schema.create(iterations=1)
        return output_list
        # output_list = []
        # cls.output_json_string = cls.input_json_string
        # if cls.output_json_string is not None:
        #     for i in range(number):
        #         for key in cls.output_json_string:
        #             if str(cls.output_json_string[key]) in 'address':
        #                 cls.output_json_string[key] = fake.address().replace('\n', ', ')
        #             if str(cls.output_json_string[key]) in 'name':
        #                 cls.output_json_string[key] = fake.name()
        #         output_list.append(cls.output_json_string)
        # return output_list
