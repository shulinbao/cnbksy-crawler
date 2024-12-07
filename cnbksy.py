import os
import pickle
import time
import re
import requests
import json
from PIL import Image
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from seleniumwire import webdriver as wire_webdriver

# 设置 GeckoDriver 路径
geckodriver_path = r"替换为你的实际路径"  # 替换为你的实际路径
# 设置 Firefox 浏览器路径
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # 替换为你安装的 Firefox 路径

# 设置 Firefox 配置
options = Options()
options.set_preference("network.http.redirection-limit", 20)  # 允许较多的重定向
options.binary_location = firefox_binary_path

# 获取用户指定的下载目录
def get_download_dir():
    # 提示用户输入文件夹路径或名称
    download_dir_input = input("【请输入】请指定工作目录（如果仅输入文件夹名，默认会在脚本所在目录创建该文件夹；直接按回车使用默认的 'test' 文件夹）：")
    
    if not download_dir_input:  # 如果用户没有输入任何内容，使用默认的 'test' 文件夹
        download_dir = os.path.join(os.getcwd(), 'test')
    elif os.path.isabs(download_dir_input):  # 如果用户输入的是绝对路径
        download_dir = download_dir_input
    else:  # 如果用户输入的是文件夹名，基于当前工作目录创建
        download_dir = os.path.join(os.getcwd(), download_dir_input)

    # 如果文件夹不存在，则创建它
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    return download_dir

# 获取用户指定的下载目录
download_dir = get_download_dir()

# 打印当前的下载目录
print(f"工作目录设置为: {download_dir}，临时下载的图片和转换后的 pdf 将储存在这里")

# 设置 Firefox 下载配置
options.set_preference("browser.download.dir", download_dir)  # 设置下载目录
options.set_preference("browser.download.folderList", 2)  # 2 表示自定义下载文件夹
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg,image/png,image/gif")  # 禁用保存对话框，自动保存为图片格式



# 启动 Firefox 浏览器，使用 selenium-wire
service = Service(geckodriver_path)
driver = wire_webdriver.Firefox(service=service, options=options)

# cookies 文件路径
cookies_file = "cookies.pkl"

# 访问登录页面的 URL
url = "https://login.openathens.net/saml/2/sso/_/c/proxy.openathens.net?SAMLRequest=jZLBbtswEER%2FheBdokiLikJYDtwYRQ2krRErPfRS0NQ6FiAvVS6Vxn9f2Y6BBEiD3ndnBvNmevO879gTBGo9VlymGWeAzjctPlb8of6clJxRtNjYziNUHD2%2FmU3J7rvezIe4w3v4PQBFNieCEEeVW4807CGsITy1Dh7u7yq%2Bi7EnI0TnH1tM%2B%2BCfD6nvAW3cAVKKEMVRUihhHQmpJoWURZlAMymTXBXbpGzySVI4WSqnM3flFGeL0bUdFU7B3xq8L03kxS%2FhxHv2nC0XFbfuGqTOtN7kWX59BaUs5CZvtNtqnVu5Ha%2BIBljisZFYcZWpPJEqyXQtM6OV0TrNtfrJ2Sr46J3vPrV4rnIIaLyllgzaPZCJzqznX%2B%2BMSjOzOR%2BR%2BVLXq2T1fV1z9uOCRB2RjJCQzKn1j6X6F19%2BZmROecOr%2F4%2Ff7QUin10a%2FTcswNjGw3%2FRmopXaS7z%2BTbaLxcr37XuwOZd5%2F%2FcBrBxHJnkYnZ%2BeTuy2V8%3D&RelayState=https%3A%2F%2Fwww-cnbksy-com.proxy.openathens.net%2F&status=Success"

# 新的目标页面 URL
new_url = "https://www-cnbksy-com.eu1.proxy.openathens.net/v2/literature/navigation"

# 检查是否存在 cookies 文件
if os.path.exists(cookies_file):
    print("检测到已有 cookies，正在加载...")
    # 加载 cookies
    with open(cookies_file, 'rb') as f:
        cookies = pickle.load(f)
        driver.get(url)  # 先访问登录 URL 以设置 cookies 的域
        for cookie in cookies:
            driver.add_cookie(cookie)
    # 访问新的目标页面
    print("正在跳转：全国报刊索引...")
    driver.get(new_url)
else:
    print("未检测到 cookies，等待用户登录并保存 cookies。")
    driver.get(url)  # 访问指定 URL

    # 等待用户手动登录或完成必要的操作
    input("【请输入】请在浏览器中完成登录操作，登录后请在显示“Please wait while we transfer you to National Newspaper Index (CNBKSY)”时按回车键保存 cookies：")

    # 保存 cookies
    cookies = driver.get_cookies()
    with open(cookies_file, 'wb') as f:
        pickle.dump(cookies, f)
    print("Cookies 已保存到脚本目录中！如果 Cookies 过期，请删除并重新获取")

    # 访问新的目标页面
    print("正在跳转：全国报刊索引...")
    driver.get(new_url)


while True:
    # 等待用户准备好开始下载
    input("【请输入】请进入您要下载的文献的“整本浏览”页面，在页面加载完成后，按回车开始下载图片：")


    # 检查并切换到最新的窗口（包括新打开的标签页）
    def switch_to_latest_window():
        try:
            # 获取当前所有窗口句柄
            all_windows = driver.window_handles
            # 切换到最后一个窗口（通常是新打开的标签页）
            driver.switch_to.window(all_windows[-1])
            print(f"成功切换到最新的窗口: {driver.current_window_handle}")
        except Exception as e:
            print(f"切换到最新窗口时出错: {e}")

    # 调用切换到最新窗口的函数
    switch_to_latest_window()


    # 然后继续执行后续操作，例如点击按钮
    try:
        driver.find_element(By.CSS_SELECTOR, "span.anticon.anticon-right").click()
        print("开始监控网络请求并提取链接...")
    except Exception as e:
        print(f"点击按钮时出错，请检查打开的页面是否正确，否则无法提取下载链接: {e}")


    # 等待请求加载
    time.sleep(5)

    # 监听网络请求，查找包含 "periodImage" 的请求
    period_image_id = None
    some_id = None

    for request in driver.requests:
        if 'periodImage' in request.url:
            # 打印出请求的 URL 以便调试

            # 提取图片下载 URL
            match = re.match(r"https://www-cnbksy-com.eu1.proxy.openathens.net/api/v2/literature/periodImage/([^/]+)/([^/]+)/(\d+)\?file=(\d+)", request.url)
            if match:
                period_image_id = match.group(1)
                some_id = match.group(2)
                print(f"提取到的 periodImageId: {period_image_id}, someId: {some_id}")
                break  # 找到后退出循环

    # 下载图片
    i = 0  # 初始化图片索引

    max_attempts = 5  # 最大尝试次数
    attempts = 0  # 当前尝试次数
    
    while True:
        try:
            # 构建图片下载 URL
            file_url = f"https://www-cnbksy-com.eu1.proxy.openathens.net/api/v2/literature/periodImage/{period_image_id}/{some_id}/{i+1}?file={str(i).zfill(4)}"
            downloaded_file = os.path.join(download_dir, f"{str(i).zfill(4)}.jpg")

            # 如果图片已经下载过，就跳过
            if os.path.exists(downloaded_file):
                print(f"【第{i+1}页】已下载")
                i += 1  # 图片已存在，跳过
                continue  # 跳过当前图片，开始下载下一张

            # 使用 Selenium 执行脚本并获取响应
            print(f"【第{i+1}页】正在检查图片格式：{file_url}")


            while True:
                try:
                    # 尝试执行图片请求的脚本
                    response_text = driver.execute_script("""
                        var xhr = new XMLHttpRequest();
                        xhr.open('GET', arguments[0], false);  // 同步请求
                        xhr.send();
                        return xhr.responseText;  // 返回响应的文本数据
                    """, file_url)

                    # 如果请求成功，跳出重试循环
                    break
        
                except Exception as e:
                    # 如果发生异常（比如网络问题），输出错误信息并重试
                    print(f"【第{i+1}页】检查格式时出错: {e}，正在重试...")
                    time.sleep(5)  # 等待5秒再试


            # 尝试解析返回的文本为 JSON
            try:
                response_json = json.loads(response_text)  # 尝试将文本解析为 JSON
                # 检查返回的 JSON 数据中的 code 和 data
                if response_json.get("code") == 404:
                    print(f"【第{i+1}页】不存在，结束下载。返回信息：{response_json.get('errorMsg')}")
                    break  # 如果遇到 404 错误，结束下载
            except json.JSONDecodeError:
                print(f"【第{i+1}页】链接解析完毕，可能是图片内容，开始下载...")

                driver.execute_script(f"window.location.href = '{file_url}'")

                # 等待图片加载
                time.sleep(15)

                # 检查图片是否下载成功
                while not os.path.exists(downloaded_file) and attempts < max_attempts:
                    print(downloaded_file)
                    print(f"【第{i+1}页】等待图片下载完成...")
                    time.sleep(10)  # 等待 10 秒
                    attempts += 1  # 增加尝试次数
                    if os.path.exists(downloaded_file):
                        print(f"【第{i+1}页】图片已成功下载！")
                        i += 1
                        attempts = 0
                        break  # 图片成功下载，退出循环

                attempts = 0           

        except Exception as e:
            print(f"下载过程出现错误: {e}")
            break

    # 获取用户输入的 PDF 文件名
    def get_pdf_filename(download_dir):
        user_input = input("【请输入】请输入保存的 PDF 文件名（如果没有后缀会自动添加 .pdf）：")
    
        # 检查用户输入的文件名是否以 .pdf 结尾
        if not user_input.lower().endswith('.pdf'):
            user_input += '.pdf'  # 如果没有 .pdf 后缀，自动添加

        # 返回完整的文件路径
        return os.path.join(download_dir, user_input)

    # 下载完成后，保存为 PDF 的函数
    def save_images_as_pdf(image_folder, pdf_filename):
        # 获取文件夹中所有 jpg 图片的路径
        images = []
        for filename in sorted(os.listdir(image_folder)):
            if filename.endswith(".jpg"):
                image_path = os.path.join(image_folder, filename)
                images.append(image_path)

        if not images:
            print("没有找到图片文件")
            return

        # 创建 PDF 对象
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
    
        # 遍历所有图片并添加到 PDF
        for image_path in images:
            # 打开图片
            image = Image.open(image_path)
        
            # 将图片转换为 RGB（如果它是 RGBA 或其他模式）
            if image.mode != 'RGB':
                image = image.convert('RGB')
        
            # 获取图片的尺寸（单位：毫米）
            width, height = image.size
            aspect_ratio = width / height
            pdf_width = 210  # A4 纸宽度 (mm)
            pdf_height = pdf_width / aspect_ratio  # 根据宽高比调整高度

            # 如果图片过大，调整大小
            if pdf_height > 297:
                pdf_height = 297
                pdf_width = pdf_height * aspect_ratio
        
            # 添加一页并插入图片
            pdf.add_page()
            pdf.image(image_path, x=0, y=0, w=pdf_width, h=pdf_height)
    
            # 显式关闭图片文件
            image.close()


        # 保存最终的 PDF
        pdf.output(pdf_filename)
        print(f"PDF 文件保存为 {pdf_filename}")

        # 删除所有 jpg 图片
        for image_path in images:
            try:
                os.remove(image_path)
                print(f"已删除图片文件: {image_path}")
            except Exception as e:
                print(f"删除文件 {image_path} 时出错: {e}")


    # 获取保存路径
    pdf_filename = get_pdf_filename(download_dir)

    # 下载完成后，调用该函数将所有图片保存为 PDF
    save_images_as_pdf(download_dir, pdf_filename)

    # 询问用户是否继续
    user_input = input("【请输入】下载完成！是否继续下载？按回车继续，输入 'exit' 退出：")
    if user_input.lower() == 'exit':
        print("退出程序")
        break  # 退出整个循环
    




