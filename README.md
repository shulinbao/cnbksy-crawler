# cnbksy-crawler
这是一个用于自动化下载“全国报刊索引”文献图片并将其转换为 PDF 文件的 Python 脚本。该脚本使用了 Selenium 浏览器自动化工具，从指定的网页下载图片并最终将这些图片合成一个 PDF 文件。用户可以灵活设置下载目录和输出的 PDF 文件名。

## 依赖的 Python 库

该脚本依赖以下 Python 库，请在运行脚本前确保已安装这些库：

1. **requests**：用于处理 HTTP 请求。
2. **Pillow (PIL)**：用于处理和操作图像文件。
3. **FPDF**：用于生成 PDF 文件。
4. **selenium**：用于浏览器自动化操作。
5. **selenium-wire**：用于捕捉和监控网络请求。
6. **json**：用于解析和处理 JSON 数据。
7. **pickle**：用于保存和加载浏览器 cookies 数据。

### 安装依赖

你可以使用 `pip` 来安装这些依赖，运行以下命令：

```bash
pip install requests pillow fpdf selenium selenium-wire
```

### 其他要求

1. **GeckoDriver**：该脚本使用 Selenium 启动 Firefox 浏览器，因此需要安装 GeckoDriver。请根据你操作系统的版本下载合适的 [GeckoDriver](https://github.com/mozilla/geckodriver/releases)，并设置正确的路径。
2. **Firefox 浏览器**：脚本需要安装 Firefox 浏览器，并且需要设置 Firefox 的路径。

## 脚本功能

1. **自动化登录**：脚本能够加载并保存登录所需的 cookies，避免每次都需要手动登录。
2. **下载文献图片**：通过 Selenium 监听页面的网络请求，提取文献图片的下载链接，自动下载图片并保存在指定的文件夹中。
3. **合成 PDF**：下载的图片将被转换成 PDF 文件，用户可以指定输出的 PDF 文件名。如果没有指定文件名，脚本将自动为文件添加 `.pdf` 后缀。
4. **删除图片文件**：在成功生成 PDF 后，脚本会删除所有下载的图片文件。

## 使用方法

### 1. 设置工作目录

运行脚本时，用户需要指定图片下载的工作目录。用户可以输入目录路径或文件夹名。如果没有输入，脚本将默认创建一个 `test` 文件夹并作为下载目录。

### 2. 登录并保存 Cookies

如果脚本检测到已有的 cookies 文件，它将自动加载并跳转到目标页面。如果没有 cookies 文件，脚本会引导用户在浏览器中完成登录操作，然后保存 cookies，以便下次使用。

### 3. 开始下载文献图片

在浏览器加载目标页面后，用户按下回车开始下载图片。脚本会自动提取图片的下载链接并进行下载，下载过程会显示进度。

### 4. 保存为 PDF

下载完成后，脚本会提示用户输入 PDF 文件名，并将所有下载的图片合成 PDF 文件。生成的 PDF 文件将保存在指定的目录中。

### 5. 继续或退出

在完成下载和保存 PDF 后，脚本会询问用户是否继续下载。如果输入 `exit`，脚本将退出。

## 重要配置

- **GeckoDriver 路径**：你需要替换 `geckodriver_path` 为你本地安装的 GeckoDriver 的路径。
- **Firefox 浏览器路径**：你需要替换 `firefox_binary_path` 为你本地安装的 Firefox 浏览器的路径。
  
### 示例：

```python
geckodriver_path = r"D:\ai\geckodriver-v0.35.0-win32\geckodriver.exe"  # 替换为实际路径
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # 替换为实际路径
```

## 脚本工作流程

1. 用户输入工作目录路径。
2. 脚本检查并加载已有的 cookies（如果有）。
3. 用户登录网站后，脚本获取文献图片的下载链接。
4. 图片被自动下载并保存到指定目录。
5. 图片转换为 PDF 格式并保存。
6. 如果选择继续，脚本重复下载过程；如果选择退出，脚本结束。

## 注意事项

1. **浏览器设置**：确保你已经正确设置了 Firefox 浏览器的路径，并且已经下载并配置了 GeckoDriver。
2. **cookies 文件**：如果 cookies 文件过期，用户需要重新登录并保存新的 cookies。
3. **下载限制**：脚本中已设置最大重试次数以避免下载失败时无限重试。

## 许可协议

本项目遵循 MIT 许可证，详情请参阅 [LICENSE](./LICENSE) 文件。

---

如果你有任何问题或需要进一步的帮助，请随时联系我！
