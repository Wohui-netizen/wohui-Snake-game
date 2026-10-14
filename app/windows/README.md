# 贪吃蛇 v0.1.0 — Windows 版

一个原生窗口（Edge WebView2）里跑的是**技能里那份同样的单文件游戏**，不是另写一份。

```text
app/windows/
├── main.py            # 应用本体：起一个本地服务，用 WebView2 窗口打开游戏
├── build.ps1          # 一键打包脚本 → dist\贪吃蛇 v0.1.0.exe
├── version.txt        # Windows 版本资源：ProductName=贪吃蛇, version 0.1.0
├── requirements.txt   # pywebview + pyinstaller
└── snake-game.html    # 构建时从技能资产复制（已被 .gitignore 忽略）
```

## 自己构建

需要先装 Python 3.9 或更高版本，然后：

```powershell
cd app\windows
powershell -ExecutionPolicy Bypass -File build.ps1
```

脚本会：建一个本地 `.venv` → 装依赖 → **从 `skills/snake-game/assets/snake-game.html` 复制游戏页** → 用 PyInstaller 打成单个 exe → 自动跑一次自检。

产物：`app\windows\dist\贪吃蛇 v0.1.0.exe`（约 20–40 MB，免安装，双击即开）。

## 直接运行源码

```powershell
python main.py             # 打开窗口
python main.py --selftest  # 只检查打包内容，不开窗口
python main.py --version   # 打印版本
```

## 为什么用本地服务而不是直接读文件

浏览器的 `file://` 页面**不允许使用 localStorage**，而最高分和界面语言正是存在那里的。所以应用启动时会在 `127.0.0.1` 上随机取一个空闲端口起一个只读的迷你静态服务，窗口指向它——最高分和语言选择才能正常保存。服务只绑定本机回环地址，无需联网、无外部请求。

## 已验证 / 未验证

- 已验证：`--selftest` 通过（页面能正常提供、游戏引擎与五语言层都在包里、无任何外部资源引用）。
- 未验证：本机没有图形桌面会话，因此**没有实际用鼠标点开窗口玩过**。你双击 exe 后如果窗口空白或报错，把报错信息发我。
