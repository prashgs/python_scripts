from fastapi import Request, FastAPI, Body
from typing import Optional
import uvicorn
from faker import Faker
import json
from mimesis.schema import Field, Schema
from mimesis.enums import Gender
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from pydantic import BaseModel, validator
from randomitem import RandomItem
import asyncio


app = FastAPI(openapi_url="/api/v1/openapi.json")
fake = Faker('en_US')
_ = Field('en')


def is_json(json_string):
    try:
        json_object = json.loads(json_string)
    except ValueError as e:
        return False
    return True


def generate_texts(number: int = 1):
    sentences = []
    for _ in range(number):
        sentences.append(fake.sentence())
    return {"texts": sentences}


def generate_random_numbers(number: int = 1, digits: int = 10):
    random_numbers = []
    for _ in range(number):
        random_numbers.append(fake.random_number(digits=digits))
    return {"randomnumbers": random_numbers}


def generate_names(number: int = 1):
    names = []
    for _ in range(number):
        names.append(fake.name())
    return {"names": names}


def generate_addresses(number: int = 1):
    addresses = []
    for _ in range(number):
        address = fake.address().replace('\n', ', ')
        addresses.append(address)
    return {"addresses": addresses}


def generate_email_ids(number: int = 1):
    emails_ids = []
    for _ in range(number):
        email_id = fake.company_email()
        emails_ids.append(email_id)
    return {"emails_ids": emails_ids}


def generate_company_names(number: int = 1):
    company_names = []
    for _ in range(number):
        company_name = fake.company()
        company_names.append(company_name)
    return {"company_names": company_names}


def format_phone_number(number):
    leading_zeros = len(number) - len(number.lstrip('0'))
    if leading_zeros > 0:
        new_number = str(number[leading_zeros:])
        new_number = new_number.ljust(leading_zeros + len(new_number), '0')
    else:
        new_number = number
    return '-'.join([new_number[:3], new_number[3:6], new_number[6:]])


def generate_phone_numbers(number: int = 1):
    phone_numbers = []
    for _ in range(number):
        phone_number = fake.msisdn()
        phone_number = phone_number[-10:]
        phone_number = format_phone_number(phone_number)
        phone_numbers.append(phone_number)
    return {"phone_numbers": phone_numbers}


def generate_people(number: int = 1):
    people = []
    for _ in range(number):
        person = fake.profile(sex=None)
        people.append(person)
    return {"people": people}


@app.get('/names')
async def names_generator(number: int = 1):
    """
    Accepts 'number' as query parameter and returns json response with list of names
    """
    json_compatible_item_data = jsonable_encoder(generate_names(number=number))
    return JSONResponse(content=json_compatible_item_data)


@app.get('/addresses')
def addresses_generator(number: int = 1):
    """
    Accepts 'number' as query parameter and returns json response with list of addresses
    """
    json_compatible_item_data = jsonable_encoder(generate_addresses(number=number))
    return JSONResponse(content=json_compatible_item_data)


@app.get('/emailids')
def emailids_generator(number: int = 1):
    """
    Accepts 'number' as query parameter and returns json response with list of email Ids
    """
    json_compatible_item_data = jsonable_encoder(generate_email_ids(number=number))
    return JSONResponse(content=json_compatible_item_data)


@app.get('/companynames')
def company_names_generator(number: int = 1):
    """
    Accepts 'number' as query parameter and returns json response with list of Company names
    """
    json_compatible_item_data = jsonable_encoder(generate_company_names(number=number))
    return JSONResponse(content=json_compatible_item_data)


@app.get('/phonenumbers')
def phone_numbers_generator(number: int = 1):
    """
    Accepts 'number' as query parameter and returns json response with list of phone numbers in the format xxx-xxx-xxxx
    """
    json_compatible_item_data = jsonable_encoder(generate_phone_numbers(number=number))
    return JSONResponse(content=json_compatible_item_data)


@app.get('/people')
def person_generator(number: int = 1):
    """
    Accepts 'number' as query parameter and returns json response with list of composite items
    """
    json_compatible_item_data = jsonable_encoder(generate_people(number=number))
    return JSONResponse(content=json_compatible_item_data)


@app.get('/texts')
def texts_generator(number: int = 1):
    """
    Accepts 'number' as query parameter and returns json response with list of sentences
    """
    json_compatible_item_data = jsonable_encoder(generate_texts(number=number))
    return JSONResponse(content=json_compatible_item_data)


@app.get('/randomnumbers')
def random_number_generator(number: int = 1, digits: int = 10):
    """
    Accepts 'number' and 'digits' as query parameters and returns json response with list of random numbers
    """
    json_compatible_item_data = jsonable_encoder(generate_random_numbers(number=number, digits=digits))
    return JSONResponse(content=json_compatible_item_data)


@app.post('/items')
def get_body(payload: dict = Body(default='Any')):
    # JsonRequest.validate_json(json.dumps(payload))
    print(payload)
    response_json = RandomItem.parse_json(json.dumps(payload))
    return response_json


if __name__ == '__main__':
    uvicorn.run(app='app:app', host='127.0.0.1', port=8000, reload=True, debug=True)
