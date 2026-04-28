import requests
import json
import sqlite3
import os
import pandas as pd

def flatten_list(val):
    if isinstance(val, list):
        return "|".join(map(str, val))
    return val

def main():
    # 1. 설정
    base_url = "https://www.nemoapp.kr/api/store/search-list"
    params = {
        "CompletedOnly": "false",
        "NELat": "37.506424719363245",
        "NELng": "127.0416657857026",
        "SWLat": "37.48956437903264",
        "SWLng": "127.01415685062328",
        "Zoom": "15",
        "SortBy": "29",
        "PageIndex": 0
    }
    headers = {
        "referer": "https://www.nemoapp.kr/store",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0",
        "sec-ch-ua": '"Microsoft Edge";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }
    
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    db_path = os.path.join(data_dir, "nemo_data.db")
    
    all_items = []
    page_index = 0
    
    # 2. 데이터 반복 요청
    while True:
        params["PageIndex"] = page_index
        print(f"페이지 {page_index} 요청 중...")
        
        try:
            response = requests.get(base_url, params=params, headers=headers)
            if response.status_code != 200:
                print(f"요청 실패 (상태 코드: {response.status_code})")
                break
            
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                print("더 이상 수집할 데이터가 없습니다.")
                break
            
            all_items.extend(items)
            print(f"페이지 {page_index}: {len(items)}개 아이템 수집 완료 (누적: {len(all_items)}개)")
            
            page_index += 1
            # 과도한 요청 방지를 위한 짧은 대기
            import time
            time.sleep(0.5)
            
        except Exception as e:
            print(f"오류 발생: {e}")
            break

    if not all_items:
        print("수집된 데이터가 없습니다.")
        return

    # 3. 데이터 평탄화 (Flattening)
    df = pd.json_normalize(all_items)
    
    # 리스트 형태의 데이터는 문자열로 변환
    for col in df.columns:
        df[col] = df[col].apply(flatten_list)

    # 4. SQLite 저장
    conn = sqlite3.connect(db_path)
    df.to_sql("stores", conn, if_exists="replace", index=False)
    conn.close()
    
    print(f"\n전체 {len(all_items)}개의 데이터가 평탄화되어 {db_path}에 저장되었습니다.")

if __name__ == "__main__":
    main()
