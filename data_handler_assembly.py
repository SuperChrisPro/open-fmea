import pandas as pd
import json
import sqlite3
from typing import List, Dict


def load_bom_excel(filename: str) -> List[Dict]:
    """
    从Excel文件加载BOM清单
    
    Args:
        filename: Excel文件名
        
    Returns:
        包含BOM信息的字典列表
    """
    try:
        df = pd.read_excel(filename)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading BOM from {filename}: {e}")
        return []


def load_process_excel(filename: str) -> List[Dict]:
    """
    从Excel文件加载工序清单
    
    Args:
        filename: Excel文件名
        
    Returns:
        包含工序信息的字典列表
    """
    try:
        df = pd.read_excel(filename)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading process from {filename}: {e}")
        return []


def save_pfmea_report(data: List[List], filename: str, format_type: str = "excel"):
    """
    保存PFMEA报告
    
    Args:
        data: PFMEA数据
        filename: 保存的文件名
        format_type: 文件格式 ("excel", "pdf", "json")
    """
    if format_type.lower() == "excel":
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_excel(filename, index=False)
    elif format_type.lower() == "json":
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    # PDF格式需要额外的库支持，这里只是占位符
    elif format_type.lower() == "pdf":
        print("PDF export functionality would be implemented here")


def load_sqlite_pfmea(filename: str) -> List[List]:
    """
    从SQLite数据库加载PFMEA数据
    
    Args:
        filename: SQLite数据库文件名
        
    Returns:
        PFMEA数据列表
    """
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        # 查询装配PFMEA表（需要先创建相应的表结构）
        cursor.execute("SELECT * FROM pfmea_assembly")
        data = cursor.fetchall()
        
        # 获取列名
        column_names = [description[0] for description in cursor.description]
        
        # 将列名作为第一行插入数据
        result = [column_names] + data
        
        conn.close()
        return result
    except Exception as e:
        print(f"Error loading PFMEA from SQLite database {filename}: {e}")
        return []


def save_sqlite_pfmea(data: List[List], filename: str):
    """
    保存PFMEA数据到SQLite数据库
    
    Args:
        data: PFMEA数据（第一行为列名）
        filename: SQLite数据库文件名
    """
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        # 删除现有表（如果存在）
        cursor.execute("DROP TABLE IF EXISTS pfmea_assembly")
        
        # 创建新表（使用第一行作为列名）
        columns = data[0]
        create_table_sql = f"CREATE TABLE pfmea_assembly ({', '.join([f'{col} TEXT' for col in columns])})"
        cursor.execute(create_table_sql)
        
        # 插入数据（跳过第一行标题）
        placeholders = ','.join(['?' for _ in columns])
        insert_sql = f"INSERT INTO pfmea_assembly VALUES ({placeholders})"
        cursor.executemany(insert_sql, data[1:])
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving PFMEA to SQLite database {filename}: {e}")


def create_pfmea_database_schema(filename: str):
    """
    创建PFMEA数据库表结构
    
    Args:
        filename: SQLite数据库文件名
    """
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        # 创建装配PFMEA表
        cursor.execute('''CREATE TABLE IF NOT EXISTS pfmea_assembly (
            line_number TEXT,
            station_number TEXT,
            sop_number TEXT,
            bom_version TEXT,
            assembly_equipment_id TEXT,
            assembly_function TEXT,
            failure_type TEXT,
            component_part_number TEXT,
            part_name TEXT,
            part_specification TEXT,
            assembly_tool_id TEXT,
            effect_of_failure TEXT,
            severity_s INTEGER,
            cause_of_failure TEXT,
            occurrence_o INTEGER,
            error_proofing_device TEXT,
            controls_prevention TEXT,
            controls_detection TEXT,
            detection_d INTEGER,
            rpn INTEGER,
            risk_level TEXT,
            recommended_action TEXT,
            responsibility TEXT,
            completion_date TEXT,
            actions_taken TEXT,
            severity_a INTEGER,
            occurrence_a INTEGER,
            detection_a INTEGER,
            rpn_a INTEGER,
            risk_level_a TEXT
        )''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating PFMEA database schema in {filename}: {e}")


def load_json_pfmea(filename: str) -> List[List]:
    """
    从JSON文件加载PFMEA数据
    
    Args:
        filename: JSON文件名
        
    Returns:
        PFMEA数据列表
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading PFMEA from JSON file {filename}: {e}")
        return []


def save_json_pfmea(data: List[List], filename: str):
    """
    保存PFMEA数据到JSON文件
    
    Args:
        data: PFMEA数据
        filename: JSON文件名
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving PFMEA to JSON file {filename}: {e}")