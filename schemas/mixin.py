from datetime import datetime
from pydantic import BaseModel

class AuditSchemaMixin(BaseModel):
    created_by: str | None = None
    created_at: datetime | None = None
    updated_by: str | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True                  # pydantic v2에서부터 생긴 옵션, orm_mode = True를 대체함
        #orm_mode = True                         # SQLAlchemy 모델을 그대로 응답 모델로 사용할 수 있게 함 (dict처럼 변환 가능)
        #extra = "forbid"                       # 정의되지 않은 필드가 들어오면 에러 발생
        #allow_population_by_field_name = True  # 필드 이름으로도 값을 채울 수 있게 허용
        #use_enum_values = True                 # Enum을 응답할 때 .value 값으로 변환해서 출력