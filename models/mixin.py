#Audit 정보 - 테이블로 저장하지 않고 개념적인 느낌으로 사용할 경우만
from datetime import datetime
from time import timezone

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class AuditMixin:
    created_by = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda : datetime.now(timezone.utc), nullable=True)
    updated_by = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=lambda : datetime.now(timezone.utc), onupdate=lambda : datetime.now(timezone.utc), nullable=True)