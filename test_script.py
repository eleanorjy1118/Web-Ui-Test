from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pytest

def test_google_search():
    # 指定 ChromeDriver 的路径
    driver_path = r"D:\chromedriver-win64\chromedriver.exe"  # 替换成你的实际路径
    
    options = Options()

    # 1. 让 navigator.webdriver = False
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 2. 禁用 Selenium 扩展
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 启动 WebDriver
    driver = webdriver.Chrome(options=options)

    # 3. 运行 JavaScript 代码隐藏 Selenium 特征（必须在访问目标网站之前执行）
    driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        WebGLRenderingContext.prototype.getParameter = function() { return "fake_value"; };
    """)

    # 使用 Service 类指定驱动路径
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service,options=options)
    
    try:
        # 打开 Google
        driver.get("https://www.google.com")
        time.sleep(2)  # 等待页面加载
        #截屏1
        driver.save_screenshot("google_homepage.png") 
        
        # 找到搜索框并输入 "Selenium Python"
        search_box = driver.find_element(By.NAME, "q") # searchbox目前使用textarea标签（以前使用input）, textarea标签支持多行输入
        search_box.send_keys("Selenium Python") #模拟手动输出关键字
        search_box.send_keys(Keys.RETURN)   #模拟回车键
        
        time.sleep(2)  # 等待搜索结果加载
        
        driver.save_screenshot("google_keyreturn.png")  #截屏
        # 验证搜索结果是否包含 "Selenium"
        assert "Selenium" in driver.page_source
        print("Test Passed: Found 'Selenium' in search results")
    
    finally:
        driver.quit()
'''
if __name__ == "__main__":
    # pytest.main(["-v", "test_script.py"])  #测试脚本
    # pytest.main(["-v", "--html=report.html", "test_script.py"]) # 生成html格式的报告
    # 多个pytest
    pytest.main(["-v", 
                 "--html=report.html",
                 "test_script.py"
                 ])

    # pytest.main(["-v", 
    #         "--html=report.html",
    #         "--self-contained-html",
    #         "test_script.py"
    #         ])
'''