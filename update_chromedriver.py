import os
import subprocess
import re
import requests
import zipfile
import io
import platform

def get_chrome_version():
    """获取本地Chrome浏览器版本"""
    try:
        if platform.system() == "Windows":
            # Windows系统获取Chrome版本
            result = subprocess.run(
                ["reg", "query", "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon", "/v", "version"],
                capture_output=True,
                text=True
            )
            version_match = re.search(r"version\s+REG_SZ\s+(\d+\.\d+\.\d+\.\d+)", result.stdout)
        elif platform.system() == "Darwin":
            # macOS系统获取Chrome版本
            result = subprocess.run(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                capture_output=True,
                text=True
            )
            version_match = re.search(r"Google Chrome (\d+\.\d+\.\d+\.\d+)", result.stdout)
        else:
            # Linux系统获取Chrome版本
            result = subprocess.run(
                ["google-chrome", "--version"],
                capture_output=True,
                text=True
            )
            version_match = re.search(r"Google Chrome (\d+\.\d+\.\d+\.\d+)", result.stdout)
        
        if version_match:
            return version_match.group(1)
        else:
            raise Exception("无法获取Chrome版本")
    except Exception as e:
        print(f"获取Chrome版本失败: {e}")
        return None

def get_chromedriver_url(chrome_version):
    """根据Chrome版本获取对应的chromedriver下载链接"""
    try:
        # 提取主版本号
        main_version = chrome_version.split(".")[0]
        
        # 获取最新的chromedriver版本信息
        release_url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{main_version}"
        response = requests.get(release_url)
        response.raise_for_status()
        chromedriver_version = response.text.strip()
        
        # 构建下载URL
        system = platform.system().lower()
        if system == "windows":
            platform_name = "win64"
            filename = f"chromedriver-win64.zip"
        elif system == "darwin":
            if platform.machine() == "arm64":
                platform_name = "mac-arm64"
            else:
                platform_name = "mac-x64"
            filename = f"chromedriver-mac-{platform_name}.zip"
        else:
            platform_name = "linux64"
            filename = f"chromedriver-linux64.zip"
        
        download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chromedriver_version}/{platform_name}/{filename}"
        return download_url, chromedriver_version, filename
    except Exception as e:
        print(f"获取chromedriver下载链接失败: {e}")
        return None, None, None

def download_and_extract_chromedriver(url, filename):
    """下载并解压chromedriver"""
    try:
        print(f"正在下载chromedriver: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # 解压zip文件
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # 查找chromedriver.exe文件
            for file in zip_ref.namelist():
                if file.endswith("chromedriver.exe") or file.endswith("chromedriver"):
                    # 提取文件
                    chromedriver_data = zip_ref.read(file)
                    return chromedriver_data
        
        raise Exception("在zip文件中未找到chromedriver.exe")
    except Exception as e:
        print(f"下载或解压chromedriver失败: {e}")
        return None

def update_chromedriver():
    """更新chromedriver.exe"""
    print("开始更新chromedriver...")
    
    # 获取Chrome版本
    chrome_version = get_chrome_version()
    if not chrome_version:
        return False
    print(f"本地Chrome版本: {chrome_version}")
    
    # 获取chromedriver下载链接
    download_url, chromedriver_version, filename = get_chromedriver_url(chrome_version)
    if not download_url:
        return False
    print(f"最新chromedriver版本: {chromedriver_version}")
    
    # 下载并解压chromedriver
    chromedriver_data = download_and_extract_chromedriver(download_url, filename)
    if not chromedriver_data:
        return False
    
    # 保存chromedriver.exe到当前目录
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    try:
        with open(chromedriver_path, "wb") as f:
            f.write(chromedriver_data)
        
        # 设置执行权限（针对非Windows系统）
        if platform.system() != "Windows":
            os.chmod(chromedriver_path, 0o755)
        
        print(f"chromedriver.exe更新成功，版本: {chromedriver_version}")
        return True
    except Exception as e:
        print(f"保存chromedriver.exe失败: {e}")
        return False

if __name__ == "__main__":
    update_chromedriver()