from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class ParaphraseModel(BaseModel):
    tree: str


_Model = TypeVar('_Model', bound=ParaphraseModel)


class ParaphraseResponse(GenericModel, Generic[_Model]):
    paraphrases: list[_Model]
