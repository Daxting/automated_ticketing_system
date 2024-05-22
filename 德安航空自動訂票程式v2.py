#import library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from selenium.webdriver.chrome.options import Options
import datetime
import time
# configure the webdriver
def main():
    options = Options()
    # 添加此行以防止關閉瀏覽器窗口
    options.add_experimental_option("detach", True)
    # set the url
    url ='https://www.dailyair.com.tw/Dailyair/Page/'
    # 印出路線種類
    print('路線種類:')
    print('1. 高雄（KHH） - 望安（WOT）')
    print('2. 高雄（KHH） - 七美（CMJ）')
    print('3. 澎湖（MZG） - 七美（CMJ）')
    print('4. 台東（TTT） - 蘭嶼（KYD）')
    print('5. 台東（TTT） - 綠島（GNI）')
    print('6. 望安（WOT） - 高雄（KHH）')
    print('7. 七美（CMJ） - 高雄（KHH）')
    print('8. 七美（CMJ） - 澎湖（MZG）')
    print('9. 蘭嶼（KYD） - 台東（TTT）')
    print('10. 綠島（GNI） - 台東（TTT）')
    print('-'*30, flush=True)
    # user input
    # 選擇路線
    airline = input('請選擇路線(輸入數字, 例如4): ')
    # 選擇人數
    NumPeople = input('請選擇人數(至多4人, 例如4): ')
    # 印出目前可訂的最新日期兩個月後的日期
    today = datetime.date.today()
    latest_date = today + datetime.timedelta(days=61)
    print('今日可訂的最新日期: ', latest_date.strftime("%Y/%m/%d"), flush=True)
    # 設定日期
    desired_date = input(f'請輸入日期(格式:yyyy/mm/dd, 例如 {latest_date.strftime("%Y/%m/%d")}): ')
    # 印出班次、離場時間、到達時間
    if airline == '4':
        print('-' * 30)
        print('路線: 台東（TTT） - 蘭嶼（KYD）')
        print('班次	   離場時間	  到達時間')
        print('7501	   07：50	  08：20')
        print('7503	   09：00	  09：30')
        print('7505	   09：50	  10：20')
        print('7515	   10：55	  11：25')
        print('7507	   11：50	  12：20')
        print('7517	   13：50	  14：20')
        print('7509	   14：25	  14：55')
        print('7511	   15：50	  16：20')
        print('-'*30, flush=True)
    elif airline == '9':
        print('-'*30)
        print('路線: 蘭嶼（KYD） - 台東（TTT）')
        print('班次	   離場時間	  到達時間')
        print('7502	   08：50	  09：20')
        print('7504	   09：55	  10：25')
        print('7506	   10：50	  11：20')
        print('7516	   11：50	  12：20')
        print('7508	   12：50	  13：20')
        print('7518	   14：50	  15：20')
        print('7510	   15：20	  15：50')
        print('7512	   16：45	  17：15')
        print('-'*30, flush=True)
    # 設定航班
    desired_section = input('請輸入航班: ')
    # 是否立即訂票
    ticket_now = input('是否進入等待搶票模式(y/n): ')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # set the max wait time
    wait = WebDriverWait(driver, 5)
    # open the website
    driver.get(url)


    # 定位到航班查询的下拉框并选择
    select_element = wait.until(EC.element_to_be_clickable((By.ID, 'BodyContent_ctl03_wowp_sel_Airline')))
    select = Select(select_element)
    select.select_by_value(airline)
    passengers_select_element = wait.until(EC.element_to_be_clickable((By.ID, 'BodyContent_ctl03_wowp_sel_Passengers')))
    # 初始化 Select 类并选择人数
    select = Select(passengers_select_element)
    select.select_by_value(NumPeople)
    # 使用 JavaScript 直接设置日期
    js_set_date = """
    var dateInput = document.getElementById('BodyContent_ctl03_wowp_hid_GoTripDate');
    var dateDisplay = document.getElementById('GoTripDate');
    dateInput.value = arguments[0];
    dateDisplay.textContent = arguments[0];
    """
    driver.execute_script(js_set_date, desired_date)
    # 定位到同意隱私權政策的 checkbox 并勾选
    driver.execute_script("document.getElementById('BodyContent_ctl03_wowp_cb_notice').checked = true;")


    if ticket_now == 'y':
        # 設定搶票時間參數
        print('每天官網開放訂票時間: 08:00:00', flush=True)
        now = datetime.datetime.now()
        target_time = datetime.datetime.combine(now.date(), datetime.time(8, 0, 0))
        print('Please wait for the ticket grabbing time...')
        # Calculate the wait time between the current time and the target time
        wait_time = (target_time - now).total_seconds()
        if wait_time > 3:
            time.sleep(wait_time - 3)
        # Loop until the current time is less than the target time+1s
        while datetime.datetime.now() < target_time + datetime.timedelta(seconds=1):
            continue

    # 定位到航班查询按钮并点击
    flight_search_button = wait.until(EC.element_to_be_clickable((By.ID, 'BodyContent_WebOrderWebPay')))
    flight_search_button.click()
    #若無法選取航班，則重新選取航班
    try:
        # 定位到航班的“选取”按钮并点击
        select_button_xpath = "//td[contains(text(), "+desired_section+")]/following-sibling::td/a[contains(@onclick, "+desired_section+")]"
        select_button = wait.until(EC.element_to_be_clickable((By.XPATH, select_button_xpath)))
        select_button.click()
        # 確認送出
        flight_search_button = wait.until(EC.element_to_be_clickable((By.ID, "BodyContent_FlightSelected")))
        flight_search_button.click()
        print('訂票成功！')
        print('請確認訂票完畢後才可以關閉CMD視窗')        
    except:
        print('指定航班已無足夠位置，請重新選擇航班。')

if __name__ == '__main__':
    main()