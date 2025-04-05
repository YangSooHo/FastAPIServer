from typing import TypeVar, Generic, List

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T') #제네릭

class PageInfo(BaseModel):
    page : int = 1
    size : int = 10

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

# Response 값으로 받는 Page 값
class PageResponse(GenericModel, Generic[T]):
    total : int
    items : List[T]
    page_info : PageInfo

