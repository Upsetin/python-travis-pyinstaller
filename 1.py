from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import os
import time


# import pymysql


def get_number():
    with open('已检测.txt', 'a', encoding='gbk') as f:
        f.write('')
    with open('已检测.txt', 'r', encoding='gbk') as f:
        aleady_nums = [i.replace('\n', '') for i in f.readlines()]
    with open('未检测.txt', 'r', encoding='gbk') as f:
        numbers = [i.replace('\n', '') for i in f.readlines()]

    for i in numbers:
        if i in aleady_nums:
            # print(f"{i}已检测,跳过...")
            continue
        elif not i:
            continue
        else:
            return i


def get_track(distance):  # distance为传入的总距离
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 1

    while current < distance:
        if current < mid:
            # 加速度为2
            a = 4
        else:
            # 加速度为-2
            a = -3
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track


def write_down(number: str, status: str) -> None:
    with open('已注册.txt', 'a', encoding='gbk') as f:
        f.write(f'{number}\n')
    print(f"已成功写入数据: {number} {status}")


def main():
    # chrome_options = Options()
    # chrome_options.add_argument(
    #     'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument('--no-sandbox')
    # # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # # driver_option.add_argument(
    # #     'user-agent=Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) '
    # #     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36')
    # file_list = os.listdir()
    # file_name = False
    # for i in file_list:
    #     if 'chromedriver' in i:
    #         file_name = i
    #         root = os.getcwd()
    #         driver_path = os.path.join(root, file_name)
    #         print(driver_path)
    # if not file_name:
    #     input("\r异常，没有chromedriver!                       ")
    #     return None
    # driver = webdriver.Chrome(driver_path, options=chrome_options)
    # with open('./stealth.min.js') as f:
    #     js = f.read()

    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": js
    # })
    driver.set_page_load_timeout(10)

    # 获取号码
    number = get_number()
    while True:
        if not number:
            input("号码已检测完毕,回车退出!")
            break
        print(f"当前号码:{number}")
        '''获取验证码'''
        try:
            driver.get('https://www.huobi.co.ma/zh-cn/reset-password/?backUrl=%2Fzh-cn%2F')
        except:
            print('打开网页失败,正在重试...')
            # time.sleep(1)
            continue
        # click phone type
        driver.find_elements_by_xpath('//*[@id="__layout"]/section/section/div[1]/form/div[1]/div[1]/a[2]')[-1].click()
        # time.sleep(0.1)
        # change region
        # click select div
        driver.find_element_by_xpath('//*[@id="__layout"]/section/section/div[1]/form/div[1]/div[2]/dl/dt/p').click()
        time.sleep(0.1)
        # select region
        driver.find_element_by_xpath('//*[@id="__layout"]/section/section/div[1]/form/div[1]/div[2]/dl/dd/div[2]/dl[1]/dd/ul/li[3]').click()
        time.sleep(0.1)
        # 填写number
        driver.find_element_by_xpath('//*[@id="account"]').send_keys(number)
        time.sleep(0.1)
        # click
        driver.find_element_by_xpath('//*[@id="__layout"]/section/section/div[1]/form/div[2]/div/button').click()
        time.sleep(1)
        print('正在尝试进行滑块...')
        # time.sleep(1000)
        # 选择验证码类型 & 滑块
        try_time = 0
        while True:
            if try_time >= 5:
                break
            try:
                style = driver.find_element_by_xpath('//div[@id="alicaptcha-1"]').get_attribute('style')
            except:
                try_time += 1
                time.sleep(0.1)
                continue
            if style:
                print('当前不是滑动验证码，正在尝试更换...')
                driver.find_elements_by_xpath('//*[@id="modals-container"]/div/div/div[2]/div/div[2]/div[5]/a/span')[-1].click()
                time.sleep(0.1)
            else:
                break
        if try_time >= 5:
            continue
        # 滑块
        print('正在滑块...')
        slider = driver.find_element_by_xpath('//span[@id="nc_1_n1z"]')
        ActionChains(driver).click_and_hold(slider).perform()
        # for x in get_track(500):
        #     ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        ActionChains(driver).move_by_offset(xoffset=480, yoffset=0).perform()
        time.sleep(0.1)
        ActionChains(driver).release().perform()
        time.sleep(0.1)
        waiting_times = 0
        while waiting_times <= 10:
            # 已注册
            if '获取验证码' in driver.page_source:
                print(f'当前用户{number}已注册...')
                write_down(number, '已注册')
                print("已写入数据库!")
                with open('已检测.txt', 'a', encoding='gbk') as f:
                    f.write(f'{number}\n')
                number = get_number()
                break
            # msg = driver.find_elements_by_xpath('//div[@class="toast-erro"]')
            if '未注册' in driver.page_source:
                # print(f'提示信息：未注册')
                print('当前用户未注册...')
                with open('已检测.txt', 'a', encoding='gbk') as f:
                    f.write(f'{number}\n')
                number = get_number()
                break
            waiting_times += 1
            time.sleep(0.5)


if __name__ == '__main__':
    while True:
        try:
            driver.quit()
        except:
            pass
        chrome_options = Options()
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        file_list = os.listdir()
        file_name = False
        for i in file_list:
            if 'chromedriver' in i:
                file_name = i
                root = os.getcwd()
                driver_path = os.path.join(root, file_name)
                # print(driver_path)
        if not file_name:
            input("\r异常，没有chromedriver!                       ")
        driver = webdriver.Chrome(driver_path, options=chrome_options)
        driver.set_page_load_timeout(10)

        # time.sleep(100)
        try:
            main()
            break
        except:
            driver.quit()
    input("程序已成功运行结束，回车退出！")
