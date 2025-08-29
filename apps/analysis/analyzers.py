from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from django.core.files.base import ContentFile

from apps.transaction_history.models import Transaction  # 예시: 거래 내역 모델

from .models import Analysis


class Analyzer:
    def __init__(self, user, start_date, end_date, analysis_type="weekly", about="총 지출"):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date
        self.analysis_type = analysis_type
        self.about = about

    def run(self):
        # 1️⃣ 거래 내역 가져오기
        qs = Transaction.objects.filter(user=self.user, date__range=[self.start_date, self.end_date])

        # 2️⃣ Pandas 데이터프레임 생성
        df = pd.DataFrame(list(qs.values("date", "amount", "category")))

        # 3️⃣ 주/월 단위로 집계
        if self.analysis_type == "weekly":
            df_grouped = df.groupby(pd.Grouper(key="date", freq="W"))["amount"].sum()
        else:
            df_grouped = df.groupby(pd.Grouper(key="date", freq="M"))["amount"].sum()

        # 4️⃣ Matplotlib 그래프 생성
        plt.figure(figsize=(8, 5))
        df_grouped.plot(kind="bar")
        plt.title(f"{self.about} ({self.analysis_type})")
        plt.ylabel("Amount")
        plt.tight_layout()

        # 5️⃣ 이미지 저장
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        # 6️⃣ Analysis 모델 생성
        analysis_instance = Analysis.objects.create(
            user=self.user,
            about=self.about,
            type=self.analysis_type,
            period_start=self.start_date,
            period_end=self.end_date,
            description=f"{len(df)}개의 거래 내역을 분석",
        )
        analysis_instance.result_image.save("analysis.png", ContentFile(buffer.read()))
        plt.close()
        return analysis_instance
