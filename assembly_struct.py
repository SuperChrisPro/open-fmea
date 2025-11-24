import tkinter as tk
from tkinter import ttk


class AssemblyStructure:
    """
    装配工厂PFMEA结构管理类
    结构层次：工厂→车间→生产线→装配工位→工序步骤→装配功能
    """

    def __init__(self):
        # 定义装配工厂的结构层次
        self.structure_levels = [
            "Factory",
            "Workshop", 
            "Production Line",
            "Assembly Station",
            "Process Step",
            "Assembly Function"
        ]
        
        # 装配专用字段定义
        self.assembly_fields = {
            "Basic Info": [
                "Line Number",
                "Station Number", 
                "SOP Number",
                "BOM Version",
                "Assembly Equipment ID"
            ],
            "Failure Info": [
                "Failure Type",
                "Component Part Number",
                "Assembly Tool ID"
            ],
            "Risk Assessment": [
                "Severity (S)",
                "Occurrence (O)", 
                "Detection (D)",
                "RPN"
            ],
            "Control Measures": [
                "Error-proofing Device",
                "Work Instruction Version",
                "Operator Qualification"
            ],
            "Improvement Tracking": [
                "Fixture Optimization",
                "Equipment Parameter Adjustment",
                "Revalidation Batch Number"
            ]
        }
        
        # 装配失效类型定义
        self.failure_types = [
            "Missing Part",
            "Wrong Part",
            "Reversed Part",
            "Part Damage",
            "Insufficient Torque",
            "Over Torque",
            "Missing Fastener",
            "Thread Galling",
            "Incorrect Fastener Length",
            "Missing Lock Washer",
            "Insufficient Press-fit Force",
            "Over Press-fit Force",
            "Insufficient Press-fit Depth",
            "Deformed Rivet Point",
            "Workpiece Positioning Deviation",
            "Missing Critical Dimension Inspection",
            "Uncalibrated Inspection Tool",
            "Parameter Setting Error",
            "Missing Debugging Step",
            "Interlock Function Failure"
        ]
        
        # 装配工具类型定义
        self.assembly_tools = [
            "Torque Wrench",
            "Electric Screwdriver",
            "Pneumatic Screwdriver",
            "Hydraulic Press",
            "Manual Press",
            "Rivet Gun",
            "Snap Gauge",
            "Micrometer",
            "Caliper",
            "Vision System"
        ]


def create_assembly_tree(app):
    """
    创建装配结构树视图
    """
    tree_frame = tk.Frame(app)
    tree_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
    
    label = tk.Label(tree_frame, text="Assembly Structure", font=("Arial", 12, "bold"))
    label.pack(pady=5)
    
    tree = ttk.Treeview(tree_frame)
    tree.heading("#0", text="Factory Hierarchy")
    tree.pack(fill=tk.BOTH, expand=True)
    
    # 添加滚动条
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    return tree


def get_assembly_columns():
    """
    获取装配PFMEA表格列定义
    """
    columns = [
        # 基本信息
        "Line Number", "Station Number", "SOP Number", "BOM Version", "Assembly Equipment ID",
        
        # 功能描述
        "Assembly Function",
        
        # 失效信息
        "Failure Type", "Component Part Number", "Part Name", "Part Specification", "Assembly Tool ID",
        
        # 失效影响
        "Effect of Failure", "Severity (S)",
        
        # 失效起因
        "Cause of Failure", "Occurrence (O)",
        
        # 现有控制措施
        "Error-proofing Device", "Controls Prevention", "Controls Detection", "Detection (D)",
        
        # 风险评估
        "RPN", "Risk Level",
        
        # 改进行动
        "Recommended Action", "Responsibility", "Completion Date", "Actions Taken",
        
        # 改进后评估
        "Severity (A)", "Occurrence (A)", "Detection (A)", "RPN (A)", "Risk Level (A)"
    ]
    
    return columns


def get_risk_level_color(risk_level):
    """
    根据风险等级返回颜色
    
    Args:
        risk_level: 风险等级字符串
        
    Returns:
        对应的颜色
    """
    color_map = {
        "High Risk": "red",
        "Medium Risk": "yellow", 
        "Low Risk": "green"
    }
    return color_map.get(risk_level, "white")


def validate_required_fields(row_data):
    """
    验证必填字段
    
    Args:
        row_data: 行数据列表
        
    Returns:
        (是否有效, 错误信息)
    """
    # 定义必填字段索引（根据get_assembly_columns的顺序）
    required_indices = [6, 7, 12, 16]  # Assembly Function, Failure Type, Cause of Failure, Controls Prevention
    
    for idx in required_indices:
        if idx < len(row_data) and not row_data[idx]:
            columns = get_assembly_columns()
            return False, f"字段 '{columns[idx]}' 为必填项"
            
    return True, ""