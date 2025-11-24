# 装备装配工厂PFMEA系统使用操作文档

## 系统概述

装备装配工厂PFMEA系统是一个专门为设备装配生产线设计的PFMEA（过程失效模式与影响分析）工具。该系统贴合一線操作需求，符合AIAG-VDA FMEA标准，可以帮助工厂的质量工程师、工艺工程师和生产管理人员进行有效的过程风险分析和管控。

## 系统安装

### 环境要求

- Windows 7及以上操作系统
- Python 3.6或更高版本（如需从源代码运行）
- 如使用可执行文件版本，则无需额外安装Python

### 安装步骤

1. 使用一键安装脚本：
   ```
   install.bat
   ```

2. 或者手动安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 系统启动

### 方法一：使用Python运行
```
python gui_assembly.py
```

### 方法二：使用可执行文件（如果已构建）
双击运行生成的可执行文件。

## 界面介绍

系统界面主要分为两个部分：

### 1. 左侧装配结构树
显示工厂层级结构：
- 工厂
- 车间
- 生产线
- 装配工位
- 工序步骤
- 装配功能

### 2. 右侧数据编辑区域
包含两个选项卡：
- **PFMEA数据录入**：主要的数据录入和编辑界面
- **风险评估**：风险矩阵和评估结果展示区域

### 3. 顶部工具栏
提供常用功能按钮：
- 导入BOM
- 导入工序
- 生成报告
- 备份数据
- 添加失效模式

## 功能详解

### 1. 数据录入

#### 手动录入
1. 在右侧"PFMEA数据录入"选项卡中，双击任意单元格即可直接在单元格中编辑
2. 编辑完成后按回车键或点击其他地方保存

#### 字段说明
数据表包含以下主要字段分类：

##### 基本信息
- Line Number（生产线编号）
- Station Number（工位编号）
- SOP Number（SOP编号）
- BOM Version（BOM版本号）
- Assembly Equipment ID（装配设备编号）

##### 功能描述
- Assembly Function（装配功能）

##### 失效信息
- Failure Type（失效类型）
- Component Part Number（零部件编号）
- Part Name（零件名称）
- Part Specification（零件规格）
- Assembly Tool ID（装配工具编号）

##### 失效影响
- Effect of Failure（失效影响）
- Severity (S)（严重度）

##### 失效起因
- Cause of Failure（失效起因）
- Occurrence (O)（发生度）

##### 现有控制措施
- Error-proofing Device（防错装置）
- Controls Prevention（预防控制）