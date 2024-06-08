import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        new_parameters.append(
            inspect.Parameter(
                name=field_name,
                kind=inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...)
                if model_field.is_required
                else Form(model_field.default),
                annotation=model_field.annotation,
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls
