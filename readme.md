# 深大羽毛球场预订，成功后可以邮箱接受信息，可以完成支付
运行脚本需要安装chrome浏览器和下面的工具包
pip install selenium 

# 配置方法

## 方法1：使用前端配置页面（推荐）
1. 直接在浏览器中打开 `config_ui.html` 文件
2. 填写所有必填参数
3. 点击「保存配置」按钮，生成 `config.json` 文件
4. 将生成的 `config.json` 文件放在脚本同一目录下

## 方法2：自动更新chromedriver
update_chromedriver.py脚本可以根据本地Chrome浏览器版本自动更新chromedriver.exe
使用方法：
python update_chromedriver.py

## 方法3：手动配置
修改脚本中的CONFIG参数，或手动创建config.json文件

开启邮箱smtp功能可参考 ：https://laowangblog.com/qq-mail-smtp-service.html

# 运行脚本
python booking.py
