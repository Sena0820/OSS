import openpyxl
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
# import chromedriver_binary
from selenium import webdriver

# googleで検索する文字
search_string = 'python'

# Seleniumを使うための設定とgoogleの画面への遷移
INTERVAL = 2.5
URL = "https://www.google.com/"
# driver_path = "./chromedriver"
# driver = webdriver.Chrome(executable_path=driver_path)
driver = webdriver.Chrome()
driver.maximize_window()
time.sleep(INTERVAL)
driver.get(URL)
time.sleep(INTERVAL)

# 文字を入力して検索
driver.find_element(By.NAME, 'q').send_keys(search_string)
#driver.find_elements(By.NAME, 'btnK')[1].click()  # btnKが2つあるので、その内の後の方
element = driver.find_element(By.CLASS_NAME, 'gNO89b')
driver.execute_script("arguments[0].click();", element)
time.sleep(INTERVAL)

results = []
flag = False
while True:
    g_ary = driver.find_elements(By.CLASS_NAME, 'g')
    for g in g_ary:
        result = {}
        # yuRUbf_tag = g.find_element(By.CLASS_NAME,'yuRUbf')
        # if yuRUbf_tag is not None:
        # result['url'] = yuRUbf_tag.find_element(By.TAG_NAME,'a').get_attribute('href')
        # try:
        #     result['url'] = g.find_element(By.CLASS_NAME,'yuRUbf').find_element(By.TAG_NAME,'a').get_attribute('href')
        # except NoSuchElementException e:
        #     print(e)
        # try:
        #     result['url'] = g.find_element(By.CLASS_NAME, "yuRUbf").find_element(By.TAG_NAME, "a").get_attribute("href")
        # except NoSuchElementException as e:
        #     print(e)
        # result['title'] = g.find_element(By.TAG_NAME, 'h3').text
        result1 = g.find_element(By.TAG_NAME, 'h3').text
        results.append(result1)
        if len(results) >= 30:  # 抽出する件数を指定
            flag = True
            break
    if flag:
        break
    driver.find_element(By.ID, 'pnnext').click()# これは次のページへの推移を書いている
    time.sleep(INTERVAL)

#resultsはリスト

for k in results:
    print(k)
for i in range(len(results)):
    title1 = results[i]
    if results[i] == 'Python 言語入門':
        print(f"{i}:{results[i]}")

        #print(i == 'Python 言語入門')


# print('Pythonとは？特徴やできること・人気の理由を初心者向けに解説' in results.values())
# 検索結果の一覧を取得する
# results = []
# flag = False
# while True:
#     g_ary = driver.find_elements(By.CLASS_NAME, 'g')
#     for g in g_ary:
#         result = {}
#         # yuRUbf_tag = g.find_element(By.CLASS_NAME,'yuRUbf')
#         # if yuRUbf_tag is not None:
#         # result['url'] = yuRUbf_tag.find_element(By.TAG_NAME,'a').get_attribute('href')
#         # try:
#         #     result['url'] = g.find_element(By.CLASS_NAME,'yuRUbf').find_element(By.TAG_NAME,'a').get_attribute('href')
#         # except NoSuchElementException e:
#         #     print(e)
#         # try:
#         #     result['url'] = g.find_element(By.CLASS_NAME, "yuRUbf").find_element(By.TAG_NAME, "a").get_attribute("href")
#         # except NoSuchElementException as e:
#         #     print(e)
#         result['title'] = g.find_element(By.TAG_NAME, 'h3').text
#         results.append(result)
#         if len(results) >= 50:  # 抽出する件数を指定
#             flag = True
#             break
#     if flag:
#         break
#     driver.find_element(By.ID, 'pnnext').click()
#     time.sleep(INTERVAL)

html = driver.page_source.encode("utf-8")

# ワークブックの作成とヘッダ入力
# workbook = openpyxl.Workbook()
# sheet = workbook.active
# sheet['A1'].value = 'タイトル'
# sheet['B1'].value = 'URL'

# シートにタイトルとURLの書き込み
# for row, result in enumerate(results, 2):
#     sheet[f"A{row}"] = result['title']
    #sheet[f"B{row}"] = result['url']
# URLが取得できていない：これを解明する必要がある
# workbook.save(f"google_search_{search_string}.csv")

driver.close()
