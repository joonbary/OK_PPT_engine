"""
한국어 텍스트를 비즈니스 음슴체로 변환하는 유틸리티
"""

import re
from typing import List


class EumsumStyleConverter:
    """
    McKinsey 스타일 음슴체 변환기
    서술체 → 음슴체 변환

    예시:
    "AI는 기업을 재구성한다" → "AI는 기업을 재구성"
    "시장이 성장하고 있다" → "시장이 성장 중"
    """

    CONVERSION_RULES = [
        (r"(.+)한다$", r"\1"),
        (r"(.+)된다$", r"\1됨"),
        (r"(.+)이다$", r"\1"),
        (r"(.+)있다$", r"\1있음"),
        (r"(.+)없다$", r"\1없음"),
        (r"(.+)하고 있다$", r"\1 중"),
        (r"(.+)하였다$", r"\1함"),
        (r"(.+)했다$", r"\1함"),
        (r"(.+)할 것이다$", r"\1 예정"),
    ]

    @classmethod
    def convert(cls, text: str) -> str:
        s = text or ""
        for pattern, replacement in cls.CONVERSION_RULES:
            s = re.sub(pattern, replacement, s)
        return s

    @classmethod
    def convert_bullet_points(cls, points: List[str]) -> List[str]:
        return [cls.convert(p or "") for p in points or []]

    @classmethod
    def convert_headline(cls, headline: str) -> str:
        return cls.convert(headline or "")

