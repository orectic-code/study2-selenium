import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

# Chromeを起動する関数
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
 
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://google.com')



def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

##1
# main処理
def main():
    search_keyword = "高収入"
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(3)
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(3)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

    # 1ページ分繰り返し
    print(len(name_list))
    for name in name_list:
        exp_name_list.append(name.text)
        print(name.text)

 # 課題2(2) for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
    print("複数項目の取得処理開始")
    exp_tr_list = []
    for num in range(1, 5):
        tr = driver.find_elements_by_css_selector(
            f"div.cassetteRecruit__main > table > tbody > tr:nth-child({num})"
        )
        tmp_list = [""] * len(tr)
        for i, value in enumerate(tr):
            tmp_list[i] = value.text
        print(tmp_list)
        exp_tr_list.append(tmp_list)
        print("項目目の取得完了")
    print("複数項目の取得処理完了")

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    exp_first_year_fee_list = []
    count = 0
    success = 0
    fail = 0
    while True:
        # 検索結果の一番上の会社名を取得(まれに１行目が広告の場合、おかしな動作をするためcassetteRecruit__headingで広告を除外している)
        name_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__name")
        copy_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__copy")
        status_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .labelEmploymentStatus")
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition") # 初年度年収

 # 1ページ分繰り返し
        for name, copy, status, table in zip(name_list, copy_list, status_list,table_list):
            try:
                # try~exceptはエラーの可能性が高い箇所に配置
                exp_name_list.append(name.text)
                exp_copy_list.append(copy.text)
                exp_status_list.append(status.text)
                # 初年度年収をtableから探す
                first_year_fee =(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
                exp_first_year_fee_list.append(first_year_fee)
                print(f"{count}件目成功 : {name.text}")
                success+=1
            except Exception as e:
                print(f"{count}件目失敗 : {name.text}")
                print(e)
                fail+=1
            finally:
                # finallyは成功でもエラーでも必ず実行
                count+=1
# 次のページボタンがあればクリックなければ終了
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            print("最終ページです。終了します。")
            break
  

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
