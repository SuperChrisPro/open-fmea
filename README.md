# Open-FMEA (Beta v0.1)

## 项目介绍

Open-FMEA 是一个开源的 FMEA（失效模式与影响分析）工具，旨在简化传统 FMEA 流程中繁琐的手动计算与文档管理。该工具提供自动化 RPN 计算、多格式数据存储和跨屏分析能力，帮助工程团队在产品设计和制造过程中更好地进行风险识别与控制。

## 功能特性

- 动态屏幕管理：支持在不同 FMEA 分析表之间切换
- 顶部应用栏操作：集成首页、打开文件、另存为、撤销/重做、前后屏导航等功能按钮
- 可编辑表格：支持对严重度(S)、发生频度(O)、探测度(D)及行动计划等字段直接编辑
- 自动 RPN 计算：自动计算风险优先数（RPN = S × O × D），并以颜色标识高风险项
- 文件操作：支持文本、JSON、XML 和 SQL 格式的数据导入导出
- 数据库连接：具备与数据库对接的能力，便于长期数据存储与检索

## 安装与运行

### 环境要求

- Python 3.6 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆项目：
   ```bash
   git clone https://github.com/Dromation/FMEAApp.git
   cd FMEAApp
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用：
   ```bash
   python fmea_app.py
   ```

## 构建可执行文件

使用 PyInstaller 可将应用打包为独立的可执行文件：

```bash
python build.py
```

## 设备装配工厂PFMEA系统

本项目还包含一个专门针对设备装配工厂的PFMEA系统，具有以下特点：

### 核心功能

- 专为设备装配生产线设计的过程失效分析
- 适配装配工序（如零部件组装、紧固、检测、调试）的核心痛点
- 贴合一线操作、符合AIAG-VDA标准、轻量化易上手
- 满足工厂生产、质量、设备部门的协同分析需求

### 模板文件

为了方便导入数据，系统提供了两个Excel模板文件：

1. **BOM模板** (`res/bom_template.xlsx`)：用于导入零部件清单信息
   - 包含生产线编号、工位编号、工序步骤、装配功能等字段

2. **工序模板** (`res/process_template.xlsx`)：用于导入工序相关信息
   - 包含SOP编号、BOM版本号、装配设备编号、操作员资质要求等字段

使用时，请按照模板格式准备数据，确保列名一致，以保证数据能正确导入系统。

### 安装与运行（装配专用版）

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行装配专用PFMEA系统：
   ```bash
   python gui_assembly.py
   ```

或者使用一键安装脚本：
```bash
install.bat
```

## 项目结构

```
.
├── screens/                 # 屏幕管理模块
├── data/                    # 数据存储目录
├── res/                     # 资源文件目录
│   ├── icons/               # 图标资源
│   ├── bom_template.xlsx    # BOM导入模板
│   ├── process_template.xlsx # 工序导入模板
│   ├── report_template.xlsx # 报告导出模板
│   └── failure_lib.json     # 装配失效模式库
├── fmea_app.py             # 主应用文件
├── table_contents.py       # 表格内容定义
├── data_handler.py         # 数据处理模块
├── menu_contents.py        # 菜单内容定义
├── logger.py               # 日志记录器
├── build.py                # 构建脚本
├── open_fmea.sql           # SQL数据库结构
└── requirements.txt        # 依赖列表
```

## 技术架构

- 前端: Tkinter（Python标准GUI库）
- 后端逻辑: Python 3.6+
- 数据处理: 内置字典结构 + JSON/XML原生支持 + SQLite
- 图像处理: PIL (Pillow) 用于图标加载
- 打包工具: PyInstaller

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

本项目采用 MIT 许可证。