---
marp: true
theme: uncover
paginate: true
backgroundColor: #f8f9fa
color: #333
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 {
    color: #004085;
  }
  h2 {
    color: #0056b3;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

# 🏠 서울 부동산 시장 분석 리포트
### 강남권 매물 데이터를 중심으로 한 EDA 분석

---

## 📊 1. 분석 개요
- **목적**: 부동산 매물 데이터를 통한 시장 트렌드 파악
- **대상**: 서울 주요 지역(특히 강남구) 매물 데이터
- **주요 지표**: 보증금, 월세, 전용면적, 지하철 접근성 등

---

## 💰 2. 임대료 및 보증금 분포
<div class="columns">
<div>

- 월세와 보증금의 상관관계 분석
- 강남권의 높은 임대료 수준 확인
- 이상치(Outlier)를 통한 프리미엄 매물 특징 파악

</div>
<div>

![width:500px](./images/deposit_dist.png)

</div>
</div>

---

## 🏢 3. 건물 및 거래 유형별 분석
<div class="columns">
<div>

![width:500px](./images/price_type_count.png)

</div>
<div>

- 거래 유형(월세/전세) 비율 확인
- 오피스텔, 빌라 등 건물 유형에 따른 가격 차이
- 강남권의 '월세' 선호도 및 공급 현황

</div>
</div>

---

## 🔍 4. 키워드 분석 (TF-IDF)
<div class="columns">
<div>

- 매물 제목에서 추출한 핵심 키워드
- **'역세권'**, **'신축'**, **'풀옵션'** 등 강조 전략
- TF-IDF 가중치를 통한 매물 가치 판단

</div>
<div>

![width:500px](./images/keyword_tfidf.png)

</div>
</div>

---

## 📏 5. 면적 대비 가격 분석
<div class="columns">
<div>

![width:500px](./images/size_vs_deposit.png)

</div>
<div>

- 면적과 보증금/월세 간의 상관계수 확인
- 평당 단가가 높은 지역적 특성 분석
- 효율적인 공간 활용형 매물의 시장성

</div>
</div>

---

## 💡 6. 결론 및 전략적 인사이트
1. **강남권 집중화**: 특정 지역에 고가 매물이 집중되어 있음
2. **역세권 가치**: 지하철역과의 거리가 임대료에 결정적 영향
3. **키워드 마케팅**: '풀옵션' 및 '관리비 포함' 키워드가 매물 노출에 유리
4. **미래 전망**: 1인 가구 증가에 따른 소형 평수 수요 지속 예상

---

# Q&A
감사합니다!
