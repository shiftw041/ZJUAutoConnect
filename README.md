# ZJUAutoConnect
自动化脚本检测网络状态并重连

## 环境准备
pip install selenium webdriver-manager

## 初始运行
1. 替换main.py中的YOUR_USERNAME和YOUR_PASSWORD为自己的账密（必要时还需更改LOGIN_URL）
2. 默认使用edge（可通过切换注释的方式自行切换到chrome）

## 调试
1. 检查元素ID(By.ID)：
  1. 深澜系统(Srun)初始ID：
     * 账号输入框：username
     * 密码输入框：password
     *登录按钮：login-account
  2. 如果跑不通，请打开登录页面，按 F12，用左上角的小箭头点击输入框和登录按钮，查看它们的 id="..." 是什么，修改代码里 By.ID 后面的字符串。
2. 无头模式 (--headless)：
   1. 代码里有一行 options.add_argument("--headless")，意味着浏览器会在后台静默运行，用户不会看到弹窗。
   2. 调试建议：第一次运行如果报错，先把这行代码注释掉，这样可以查看浏览器自动弹出来填表单的过程，方便找出是哪一步卡住了。
