from django.db import models


class TimeStampedModel(models.Model):
    # 생성일시 - 생성될 때 자동으로 현재 시간 저장
    created = models.DateTimeField(auto_now_add=True)
    # 수정일시 - 수정될 때마다 자동으로 현재 시간 저장
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # DB 테이블 생성 안함 (상속용으로만 사용)
