# 필수 라이브러리
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

# 자바스크립트 CVE 사이트
url = 'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=JavaScript'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# 전체 a 추출 (리스트화)
a_href = soup.select('a')
CVE_list = []
for i in a_href:
    text = i.get_text()
    if text.startswith("CVE-"):
        CVE_list.append(text)
# 데이터 프레임화
CVE_list_csv = pd.DataFrame(data=CVE_list,
                            columns = ['CVE'])
# Discriptions 추가 크롤링
discriptions = []
for td in soup.select('td'):
    # <a> 태그를 제거
    for a in td.select('a'):
        a.decompose()
    # 남은 텍스트 출력
    discriptions.append(td.get_text().strip())
# 공백 제외
discriptions = [discription for discription in discriptions if discription!='']
# 마지막 3줄이 필요 없는 문장이므로 삭제
discriptions = discriptions[1:-3]
# 데이터 프레임화
CVE_discription_csv = pd.DataFrame(data=discriptions,
                                   columns=['Discriptions'])
# 최종 자바스크립트 CVE 데이터만 추출
cve_discript = pd.concat(objs=[CVE_list_csv, CVE_discription_csv], axis=1)
# --------------------------------------------------------------------------------------------------
# 취약점 폴더 안에 있는 모든 CVE 파일을 보면서 CVE-2023-XXXX 부분과 reference->url 부분만 파싱
CVE_list = []
CVE_url = []
# 현재 디렉토리에 있는 CVE-2023 폴더 ls
first_folder_ls = os.listdir('./CVE-2022')
# 출력된 ls값(하위 폴더)에 대해 한번 더 for문을 사용해 하위 파일에 접근
for i in first_folder_ls:
    # 하위 폴더 위치
    second_folder_ls = f'./CVE-2022/{i}'
    # 하위 폴더에 대한 하위 파일 ls
    for j in os.listdir(second_folder_ls):
        # 다시 파일 위치 지정
        file_path = f'{second_folder_ls}/{j}'
        data = json.load(open(file_path, 'r', encoding='utf-8'))
        references = data['references']
        for url in references:
            CVE_list.append(j.split('.')[0])
            CVE_url.append(url['url'])
# 2023년에 대락 11만 6천개의 서로다른 url을 가진 CVE가 있음
cve_url = pd.DataFrame({'CVE': CVE_list, 'URL': CVE_url})
# 하지만, 결국 우리가 필요한 내용은 url에 github가 포함되어있는 내용이므로 해당 내용 파싱
cve_url = cve_url.loc[cve_url['URL'].str.contains('github')]
# 그 중에서 중복되어있는 CVE 값이 많으므로 groupby를 지정하겠음!
cve_url = cve_url.groupby(by='CVE').min()
# 여기서 우리는 javascript CVE만 필요하므로, 이전의 데이터프레임과 merge하겠음!
javascript_cve_url_discript = pd.merge(left=cve_discript,
                                       right=cve_url,
                                       on='CVE')[['CVE', 'URL', 'Discriptions']].sort_values(by='CVE').reset_index(drop=True)
# 최종 데이터를 csv로 저장!
javascript_cve_url_discript.to_csv('./2022_javascript_cve_url_discript.csv', index=False)