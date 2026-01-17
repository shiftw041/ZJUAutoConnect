import time
import socket
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
# import sys
# # 错误日志记录
# sys.stdout = open('log.txt', 'a')
# sys.stderr = open('log_error.txt', 'a')

# ================= 配置区域 =================
# 校园网登录页地址
LOGIN_URL = "http://172.16.10.10/srun_portal_pc?ac_id=1&theme=pro"

# 检测间隔
CHECK_GAP = 30

# 账号密码
USERNAME = "12345678" 
PASSWORD = "123456"

# test ip 用于检测是否断网
TEST_IP = "baidu.com"
# ===========================================

def check_internet():
    """检测网络连通性 (ping)"""
    # Windows 下 ping 1次，超时 1秒
    ret = os.system(f"ping -n 1 -w 1000 {TEST_IP} >nul 2>&1")
    return ret == 0

def login_srun():
    print(">>> 启动浏览器进行登录...")
    
    # 默认使用 Edge 浏览器 (Windows自带)
    # 如果想用 Chrome，切换下面的注释
    try:
        # --- Edge 配置 ---
        options = webdriver.EdgeOptions()
        # 无头模式：不显示浏览器窗口，后台运行
        # 第一次运行时最好注释掉，手动检查哪里卡住了
        options.add_argument("--headless") 
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        # --- Chrome 配置 (如果用Chrome) ---
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # service = ChromeService(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service, options=options)

        # 1. 打开登录页
        driver.get(LOGIN_URL)
        
        # 2. 等待输入框加载出来 (最多等10秒)
        wait = WebDriverWait(driver, 10)
        user_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        pwd_input = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.ID, "login-account") # 深澜通常ID是 login-account 或 login

        # 3. 清空并输入账号密码
        user_input.clear()
        user_input.send_keys(USERNAME)
        pwd_input.clear()
        pwd_input.send_keys(PASSWORD)

        # 4. 点击登录
        print(">>> 正在点击登录按钮...")
        login_btn.click()
        
        # 5. 等待一会儿，让请求发送出去
        time.sleep(3)
        print(">>> 登录操作完成，关闭浏览器。")
        driver.quit()
        return True

    except Exception as e:
        print(f"!!! 登录过程出错: {e}")
        try:
            driver.quit()
        except:
            pass
        return False

def main():
    print(f"[{time.strftime('%H:%M:%S')}] 脚本启动，开始监控网络...")
    while True:
        if not check_internet():
            print(f"[{time.strftime('%H:%M:%S')}] 网络已断开，准备重连...")
            login_srun()
            
            # 登录后再次检测
            time.sleep(5)
            if check_internet():
                print(f"[{time.strftime('%H:%M:%S')}] 网络已恢复！")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] 重连似乎未生效，等待下一次尝试。")
        
        # 循环检查
        time.sleep(CHECK_GAP)

if __name__ == "__main__":
    main()
