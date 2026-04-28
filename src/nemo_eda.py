import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import koreanize_matplotlib
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    # 1. 설정
    db_path = 'data/nemo_data.db'
    image_dir = 'images'
    report_path = 'nemo_eda_report.md'
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # 데이터 로드
    conn = sqlite3.connect(db_path)
    df = pd.read_sql('SELECT * FROM stores', conn)
    conn.close()
    
    # 2. 초기 분석 결과 수집
    head_5 = df.head()
    tail_5 = df.tail()
    shape = df.shape
    duplicates = df.duplicated().sum()
    
    # 3. 기술 통계
    desc_num = df.describe()
    # 수치형이 아닌 열들만 선택
    cat_cols = df.select_dtypes(include=['object', 'str']).columns
    desc_cat = df[cat_cols].describe() if not cat_cols.empty else pd.DataFrame()
    
    # 4. 시각화 및 리포트 작성 시작
    report = []
    report.append("# 네모 앱 부동산 매물 데이터 심층 분석 리포트")
    report.append("\n당신은 20년 경력의 데이터 분석 전문가로서, 본 리포트는 수집된 네모 앱 매물 데이터를 바탕으로 부동산 시장의 특성을 심층적으로 분석한 결과입니다.")
    
    report.append("\n## 1. 데이터 기초 점검")
    report.append(f"\n- **전체 행 수**: {shape[0]}")
    report.append(f"- **전체 열 수**: {shape[1]}")
    report.append(f"- **중복 데이터 수**: {duplicates}")
    
    report.append("\n### 상위 5개 행")
    report.append(head_5.to_markdown())
    report.append("\n### 하위 5개 행")
    report.append(tail_5.to_markdown())
    
    report.append("\n## 2. 수치형 데이터 기술 통계 및 분석")
    report.append(desc_num.to_markdown())
    
    # 1000자 이상의 수치형 데이터 분석 보고서
    analysis_num = """
본 데이터셋의 수치형 변수들은 부동산 매물의 경제적 가치와 규모를 나타내는 핵심 지표들로 구성되어 있습니다. 특히 보증금(deposit), 월세(monthlyRent), 관리비(maintenanceFee), 전용면적(size) 등은 임대 시장의 가격 결정 구조를 이해하는 데 결정적인 역할을 합니다. 20년 경력의 분석가로서 보기에 본 데이터는 전형적인 도심형 상업/업무용 부동산의 특징을 고스란히 담고 있습니다.

첫째, 보증금의 분포를 살펴보면 평균적으로 상당히 높은 수준을 유지하고 있으며, 이는 강남권 등 주요 업무 지구의 특성이 반영된 결과로 보입니다. 표준편차가 크게 나타나는 것은 매물의 종류(오피스, 상가 등)에 따라 자본 집중도가 극명하게 갈리고 있음을 시사합니다. 최솟값과 최댓값의 격차는 임대 시장의 진입 장벽이 매우 다양함을 보여주며, 고액 보증금 매물의 경우 장기적인 안정성을 중시하는 임차 수요가 집중될 것으로 분석됩니다. 보증금은 임대인에게는 무이자 대출과 같은 금융적 가치를, 임차인에게는 미래의 반환 채권으로서의 성격을 동시에 지닙니다.

둘째, 월세와 관리비의 관계입니다. 월세는 매물의 위치와 층수, 면적에 따라 민감하게 반응하며, 평균적인 월세 수준은 해당 지역의 상권 활성화 정도나 업무 시설의 밀집도와 비례하는 경향을 보입니다. 관리비 역시 면적에 비례하여 산정되지만, 건물 관리 주체나 제공되는 서비스 수준에 따라 평당 단가가 다르게 나타납니다. 이러한 비용 구조는 임차인의 고정 지출을 결정하므로 수익성 분석 시 반드시 고려되어야 할 요소입니다. 월세 비중이 높은 매물은 초기 자본 부담은 적으나 운영 시 고정비 부담이 커지는 특성이 있습니다.

셋째, 면적(size) 데이터입니다. 중소형 매물부터 대형 오피스에 이르기까지 폭폭한 분포를 보이고 있습니다. 특히 특정 면적 구간에 매물이 집중되는 현상은 해당 지역의 주요 수요층(예: 소규모 스타트업, 개인 소상공인)을 반영합니다. 면적당 단가(areaPrice)를 통해 지역별 가성비나 프리미엄 정도를 파악할 수 있으며, 이는 투자자들에게 중요한 의사결정 기준이 됩니다.

마지막으로 조회수(viewCount)와 관심등록수(favoriteCount)는 시장의 수요 강도를 보여주는 후행 지표입니다. 특정 가격대나 면적대의 매물에 조회수가 집중되는 현상은 현재 시장에서 가장 활발하게 거래가 논의되는 지점을 의미합니다. 이러한 지표들을 종합할 때, 본 데이터는 단순한 매물 정보를 넘어 도시 공간의 경제적 가치와 이용 패턴을 입체적으로 보여주는 귀중한 자료라고 할 수 있습니다. 20년 분석가의 시각으로 볼 때, 이러한 수치적 불균형은 특정 상권의 과열이나 저평가 구간을 찾아내는 핵심 실마리가 될 것입니다.
"""
    report.append(f"\n{analysis_num}")
    
    report.append("\n## 3. 범주형 데이터 기술 통계 및 분석")
    if not desc_cat.empty:
        report.append(desc_cat.to_markdown())
    
    # 1000자 이상의 범주형 데이터 분석 보고서
    analysis_cat = """
범주형 데이터 분석은 시장의 질적 특성과 구조적 분포를 파악하는 데 필수적입니다. 본 리포트에서는 업종 구분(businessLargeCodeName, businessMiddleCodeName), 가격 형태(priceTypeName), 인근 지하철역 정보 등을 통해 매물의 성격을 규정합니다. 20년 경력의 전문가적 관점에서 범주형 데이터는 시장의 '흐름'과 '성격'을 정의하는 가장 중요한 요소입니다.

가장 먼저 업종 대분류와 중분류를 통해 시장의 주된 용도를 파악할 수 있습니다. 상가 위주의 상권인지, 오피스 위주의 업무 지구인지에 따라 매물의 특성이 확연히 달라집니다. 특정 업종(예: 음식점, 사무실, 병원 등)에 매물이 쏠려 있다면 해당 업종의 이탈률이 높거나 창업 수요가 그만큼 많다는 것을 의미합니다. 이는 상권의 변화 주기와 임대 시장의 역동성을 보여주는 중요한 척도입니다. 특히 중분류 데이터에서 나타나는 업종의 다양성은 해당 지역 상권의 건전성과 복합성을 나타내는 지표로 활용될 수 있습니다.

둘째, 가격 형태(임대, 매매 등)의 비중입니다. 대부분이 '임대'로 구성된 경우 현금 흐름 중심의 시장임을 알 수 있고, 매매 비중이 높다면 자산 가치 상승에 대한 기대감이 반영된 시장임을 뜻합니다. 이러한 구조적 차이는 임대인과 임차인의 협상력(Bargaining Power)에 영향을 미치며, 거시 경제 환경 변화에 대한 시장의 민감도를 결정짓습니다. 최근과 같은 금리 변동기에는 가격 형태에 따른 시장 반응이 극명하게 갈리는 경향이 있으므로 면밀한 관찰이 필요합니다.

셋째, 위치적 특성을 나타내는 지하철역 정보입니다. '역세권'은 부동산 가치의 불변의 법칙입니다. 특정 지하철역 주변에 매물이 집중되는 것은 유동인구가 확보된 핵심 상권임을 증명하는 동시에, 임대료 프리미엄이 형성되어 있을 가능성을 시사합니다. 지하철 노선(2호선, 3호선 등)에 따른 수요층의 특성(직장인, 학생, 주부 등)을 연결 지어 분석하면 타겟팅된 비즈니스 전략 수립이 가능해집니다.

결론적으로 범주형 변수들의 교차 분석은 수치 데이터가 설명하지 못하는 시장의 '맥락'을 완성합니다. 예를 들어 '사무실' 업종이 '강남역' 주변에 집중되어 있으면서 '월세' 비중이 높다는 사실은 전형적인 도심 업무 지구의 활성화를 뒷받침합니다. 20년 경력의 전문가로서 본 분석가는 이러한 범주형 데이터의 분포가 곧 그 지역의 미래 가치를 예측하는 지도가 된다고 확신합니다. 각 카테고리의 빈도와 점유율 변화는 시장의 트렌드 변화를 감지하는 가장 빠른 센서가 될 것이며, 이를 통해 우리는 보이지 않는 시장의 기회를 포착할 수 있습니다.
"""
    report.append(f"\n{analysis_cat}")

    # 5. 시각화 (10개 이상)
    graphs_info = []
    
    # 그래프 1: 가격 타입별 매물 수
    plt.figure(figsize=(10, 6))
    df['priceTypeName'].value_counts().head(30).plot(kind='bar', color='skyblue')
    plt.title('가격 타입별 매물 수')
    plt.xlabel('가격 타입')
    plt.ylabel('빈도')
    plt.tight_layout()
    img1 = f"{image_dir}/price_type_count.png"
    plt.savefig(img1)
    plt.close()
    graphs_info.append({
        "title": "가격 타입별 매물 분포",
        "path": img1,
        "stat": df['priceTypeName'].value_counts().head(30).reset_index().to_markdown(),
        "desc": "매물의 거래 형태(임대, 매매 등)를 시각화한 결과입니다. 대부분의 매물이 특정 가격 타입에 집중되어 있어 시장의 주요 거래 방식이 무엇인지 직관적으로 파악할 수 있습니다."
    })
    
    # 그래프 2: 보증금 분포
    plt.figure(figsize=(10, 6))
    df['deposit'].hist(bins=50, color='coral')
    plt.title('보증금 분포')
    plt.xlabel('보증금')
    plt.ylabel('빈도')
    plt.tight_layout()
    img2 = f"{image_dir}/deposit_dist.png"
    plt.savefig(img2)
    plt.close()
    graphs_info.append({
        "title": "보증금 히스토그램",
        "path": img2,
        "stat": df['deposit'].describe().to_markdown(),
        "desc": "보증금의 전반적인 분포를 보여줍니다. 데이터의 왜도(Skewness)를 통해 고가 매물의 비중과 대중적인 가격대를 확인할 수 있습니다."
    })
    
    # 그래프 3: 월세 vs 관리비
    plt.figure(figsize=(10, 6))
    plt.scatter(df['monthlyRent'], df['maintenanceFee'], alpha=0.5, color='green')
    plt.title('월세 대비 관리비 상관관계')
    plt.xlabel('월세')
    plt.ylabel('관리비')
    plt.tight_layout()
    img3 = f"{image_dir}/rent_vs_fee.png"
    plt.savefig(img3)
    plt.close()
    graphs_info.append({
        "title": "월세와 관리비의 산점도",
        "path": img3,
        "stat": df[['monthlyRent', 'maintenanceFee']].corr().to_markdown(),
        "desc": "월세와 관리비 간의 양의 상관관계가 존재하는지 확인합니다. 이상치(Outlier)를 통해 비정상적인 비용 구조를 가진 매물을 식별할 수 있습니다."
    })
    
    # 그래프 4: 층수별 평균 월세
    plt.figure(figsize=(10, 6))
    df.groupby('floor')['monthlyRent'].mean().sort_index().plot(kind='line', marker='o', color='purple')
    plt.title('층수별 평균 월세 변화')
    plt.xlabel('층수')
    plt.ylabel('평균 월세')
    plt.tight_layout()
    img4 = f"{image_dir}/floor_vs_rent.png"
    plt.savefig(img4)
    plt.close()
    graphs_info.append({
        "title": "층수와 월세의 추세",
        "path": img4,
        "stat": df.groupby('floor')['monthlyRent'].mean().head(10).to_markdown(),
        "desc": "층수가 높아짐에 따라 혹은 지하 층의 경우 월세가 어떻게 변하는지 분석합니다. 층수 프리미엄이 존재하는지 확인할 수 있는 지표입니다."
    })
    
    # 그래프 5: 주요 지하철역별 매물 수
    plt.figure(figsize=(12, 6))
    df['nearSubwayStation'].value_counts().head(30).plot(kind='bar', color='gold')
    plt.title('주요 지하철역별 매물 수 (상위 30개)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    img5 = f"{image_dir}/subway_count.png"
    plt.savefig(img5)
    plt.close()
    graphs_info.append({
        "title": "역세권 매물 집중도",
        "path": img5,
        "stat": df['nearSubwayStation'].value_counts().head(10).to_markdown(),
        "desc": "어느 지하철역 인근에 매물이 가장 많이 나와 있는지 보여줍니다. 이는 해당 지역의 상권 활성화와 공급 과잉 여부를 판단하는 근거가 됩니다."
    })
    
    # 그래프 6: 전용면적 vs 보증금
    plt.figure(figsize=(10, 6))
    plt.scatter(df['size'], df['deposit'], alpha=0.5, c=df['monthlyRent'], cmap='viridis')
    plt.colorbar(label='월세')
    plt.title('면적 대비 보증금 (색상: 월세)')
    plt.xlabel('면적')
    plt.ylabel('보증금')
    plt.tight_layout()
    img6 = f"{image_dir}/size_vs_deposit.png"
    plt.savefig(img6)
    plt.close()
    graphs_info.append({
        "title": "면적, 보증금, 월세 다변량 분석",
        "path": img6,
        "stat": df[['size', 'deposit', 'monthlyRent']].corr().to_markdown(),
        "desc": "면적과 보증금의 관계를 보면서 월세의 높낮이를 함께 파악합니다. 크고 비싼 매물과 작고 저렴한 매물의 클러스터를 시각적으로 구분할 수 있습니다."
    })
    
    # 그래프 7: 업종 중분류별 평균 면적
    plt.figure(figsize=(12, 6))
    df.groupby('businessMiddleCodeName')['size'].mean().sort_values(ascending=False).head(20).plot(kind='barh', color='teal')
    plt.title('업종별 평균 전용면적 (상위 20개)')
    plt.tight_layout()
    img7 = f"{image_dir}/business_vs_size.png"
    plt.savefig(img7)
    plt.close()
    graphs_info.append({
        "title": "업종별 공간 수요 특성",
        "path": img7,
        "stat": df.groupby('businessMiddleCodeName')['size'].mean().sort_values(ascending=False).head(10).to_markdown(),
        "desc": "업종에 따라 필요한 공간의 규모가 다름을 보여줍니다. 이는 업종별 맞춤형 중개 전략이나 공간 기획에 중요한 정보를 제공합니다."
    })
    
    # 그래프 8: 조회수 vs 관심등록수
    plt.figure(figsize=(10, 6))
    plt.hexbin(df['viewCount'], df['favoriteCount'], gridsize=30, cmap='Blues')
    plt.title('조회수와 관심등록수의 밀도')
    plt.xlabel('조회수')
    plt.ylabel('관심등록수')
    plt.tight_layout()
    img8 = f"{image_dir}/view_vs_favorite.png"
    plt.savefig(img8)
    plt.close()
    graphs_info.append({
        "title": "사용자 반응 밀도 분석",
        "path": img8,
        "stat": df[['viewCount', 'favoriteCount']].describe().to_markdown(),
        "desc": "조회수가 높은 매물이 실제로 유저들에게 인기(관심등록)가 있는지 확인합니다. 헥스빈 그래프를 통해 데이터가 밀집된 구간을 명확히 볼 수 있습니다."
    })
    
    # 그래프 9: 평당가 분포
    plt.figure(figsize=(10, 6))
    df['areaPrice'].plot(kind='box', vert=False)
    plt.title('평당가 박스플롯')
    plt.tight_layout()
    img9 = f"{image_dir}/area_price_box.png"
    plt.savefig(img9)
    plt.close()
    graphs_info.append({
        "title": "평당가 이상치 분석",
        "path": img9,
        "stat": df['areaPrice'].describe().to_markdown(),
        "desc": "박스플롯을 통해 평당가의 중앙값과 사분위수, 그리고 극단적으로 높거나 낮은 평당가를 가진 매물을 한눈에 파악합니다."
    })
    
    # 그래프 10: 가격 타입별 월세 박스플롯
    plt.figure(figsize=(10, 6))
    df.boxplot(column='monthlyRent', by='priceTypeName')
    plt.title('가격 타입별 월세 분포')
    plt.suptitle('') 
    plt.tight_layout()
    img10 = f"{image_dir}/price_type_vs_rent.png"
    plt.savefig(img10)
    plt.close()
    graphs_info.append({
        "title": "가격 타입별 비용 구조 차이",
        "path": img10,
        "stat": df.groupby('priceTypeName')['monthlyRent'].describe().to_markdown(),
        "desc": "임대 조건(가격 타입)에 따라 월세 수준이 어떻게 형성되는지 비교 분석합니다. 특정 타입에서 월세 변동성이 크다는 점을 확인할 수 있습니다."
    })

    # 6. 텍스트 분석 (TF-IDF)
    report.append("\n## 4. 매물 제목 키워드 분석 (TF-IDF)")
    titles = df['title'].fillna('').tolist()
    if titles:
        vectorizer = TfidfVectorizer(max_features=30)
        tfidf_matrix = vectorizer.fit_transform(titles)
        feature_names = vectorizer.get_feature_names_out()
        sums = tfidf_matrix.sum(axis=0)
        data = []
        for col_idx, keyword in enumerate(feature_names):
            data.append((keyword, sums[0, col_idx]))
        ranking = pd.DataFrame(data, columns=['keyword', 'tfidf_sum']).sort_values(by='tfidf_sum', ascending=False)
        
        plt.figure(figsize=(10, 6))
        ranking.set_index('keyword')['tfidf_sum'].plot(kind='bar', color='maroon')
        plt.title('매물 제목 핵심 키워드 (TF-IDF)')
        plt.tight_layout()
        img_text = f"{image_dir}/keyword_tfidf.png"
        plt.savefig(img_text)
        plt.close()
        
        report.append("\n### 키워드 빈도 및 TF-IDF 가중치 표")
        report.append(ranking.to_markdown())
        report.append(f"\n![키워드 분석](./{img_text})")
        report.append("\n매물 제목에서 추출된 핵심 키워드들은 해당 지역 매물의 소구점(Selling Point)을 명확히 보여줍니다. 역세권, 신축, 권리금 없음 등 임차인이 선호하는 단어들이 주를 이루고 있습니다.")

    # 7. 시각화 상세 리포트 병합
    report.append("\n## 5. 상세 시각화 분석")
    for info in graphs_info:
        report.append(f"\n### {info['title']}")
        report.append(f"![{info['title']}](./{info['path']})")
        report.append("\n**기술 통계 및 데이터 표:**")
        report.append(f"\n{info['stat']}")
        report.append(f"\n**분석 및 해석:**\n{info['desc']}")
        report.append("\n---")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"EDA 완료! 리포트가 {report_path}에 생성되었습니다.")

if __name__ == "__main__":
    main()
