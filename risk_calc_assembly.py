def get_severity_score(failure_type: str, impact: str) -> int:
    """
    根据装配失效类型和影响返回严重度S
    
    Args:
        failure_type: 失效类型
        impact: 影响描述
        
    Returns:
        严重度评分 (1-10)
    """
    severity_map = {
        "Insufficient Torque": {
            "Safety Accident": 10,
            "Equipment Failure": 8,
            "Performance Degradation": 6,
            "No Impact": 1
        },
        "Missing Part": {
            "Complete Rework": 9,
            "Partial Rework": 7,
            "No Impact": 3
        },
        "Wrong Part": {
            "Complete Rework": 9,
            "Partial Rework": 7,
            "No Impact": 3
        },
        "Reversed Part": {
            "Complete Rework": 9,
            "Partial Rework": 7,
            "No Impact": 3
        },
        "Part Damage": {
            "Safety Risk": 9,
            "Functional Failure": 7,
            "Cosmetic Issue": 4
        },
        "Over Torque": {
            "Thread Damage": 8,
            "Component Cracking": 9,
            "Fastener Failure": 10
        }
    }
    
    # 默认评分
    default_severity = 5
    
    if failure_type in severity_map:
        if impact in severity_map[failure_type]:
            return severity_map[failure_type][impact]
        else:
            # 如果没有找到具体的impact，则返回该失效类型的最高评分
            return max(severity_map[failure_type].values()) if severity_map[failure_type] else default_severity
    else:
        return default_severity


def get_occurrence_score(occurrence_desc: str) -> int:
    """
    根据发生频率描述返回评分
    
    Args:
        occurrence_desc: 发生频率描述
        
    Returns:
        发生频率评分 (1-10)
    """
    occurrence_mapping = {
        "Very High (>50%)": 10,
        "High (20-50%)": 8,
        "Medium (5-20%)": 6,
        "Low (1-5%)": 4,
        "Very Low (<1%)": 2,
        "Extremely Low (Remote)": 1
    }
    
    return occurrence_mapping.get(occurrence_desc, 5)


def get_detection_score(detection_desc: str) -> int:
    """
    根据探测度描述返回评分
    
    Args:
        detection_desc: 探测度描述
        
    Returns:
        探测度评分 (1-10)
    """
    detection_mapping = {
        "Almost Impossible": 10,
        "Very Remote": 9,
        "Remote": 8,
        "Very Low": 7,
        "Low": 6,
        "Moderate": 5,
        "High": 4,
        "Very High": 3,
        "Certain": 1
    }
    
    # 特殊情况：如果有防错装置，降低探测难度
    if "error-proofing" in detection_desc.lower():
        base_score = detection_mapping.get(detection_desc.replace(" with error-proofing", ""), 5)
        return max(1, base_score - 3)  # 最多降低3分，最低为1
    
    return detection_mapping.get(detection_desc, 5)


def calculate_rpn_assembly(failure_type: str, impact: str, occurrence_desc: str, detection_desc: str) -> tuple:
    """
    装配场景专用RPN计算，输入描述自动匹配评分
    
    Args:
        failure_type: 失效类型
        impact: 影响描述
        occurrence_desc: 发生频率描述
        detection_desc: 探测度描述
        
    Returns:
        (S, O, D, RPN, 风险等级) 元组
    """
    s = get_severity_score(failure_type, impact)
    o = get_occurrence_score(occurrence_desc)
    d = get_detection_score(detection_desc)
    rpn = s * o * d
    
    # 根据装配行业的标准确定风险等级
    if rpn >= 100:
        risk_level = "High Risk"
    elif rpn >= 60:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"
    
    return s, o, d, rpn, risk_level


def get_rpn_color(rpn: int) -> str:
    """
    根据RPN值返回颜色标识
    
    Args:
        rpn: RPN值
        
    Returns:
        颜色标识字符串
    """
    if rpn >= 100:
        return "red"
    elif rpn >= 60:
        return "yellow"
    else:
        return "green"


def get_severity_descriptions():
    """
    获取严重度描述列表
    
    Returns:
        严重度描述列表
    """
    return [
        "Safety Accident",
        "Equipment Failure", 
        "Performance Degradation",
        "Complete Rework",
        "Partial Rework",
        "No Impact",
        "Safety Risk",
        "Functional Failure",
        "Cosmetic Issue",
        "Thread Damage",
        "Component Cracking",
        "Fastener Failure"
    ]


def get_occurrence_descriptions():
    """
    获取发生频率描述列表
    
    Returns:
        发生频率描述列表
    """
    return [
        "Very High (>50%)",
        "High (20-50%)",
        "Medium (5-20%)",
        "Low (1-5%)",
        "Very Low (<1%)",
        "Extremely Low (Remote)"
    ]


def get_detection_descriptions():
    """
    获取探测度描述列表
    
    Returns:
        探测度描述列表
    """
    return [
        "Almost Impossible",
        "Very Remote",
        "Remote",
        "Very Low",
        "Low",
        "Moderate",
        "High",
        "Very High",
        "Certain"
    ]