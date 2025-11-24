import json
import os


class AssemblyKnowledgeBase:
    """
    装备装配知识库类
    管理常见的失效模式、起因和控制措施
    """
    
    def __init__(self, json_file="res/failure_lib.json"):
        # 初始化常见失效模式库
        self.failure_library = {
            "Part Assembly": [
                {
                    "failure_mode": "Missing Part",
                    "effects": ["Incomplete product", "Functional failure", "Safety hazard"],
                    "causes": ["Operator forgetfulness", "Inadequate poka-yoke", "Poor work instruction"],
                    "controls": ["Part presence sensors", "Checklists", "Visual aids"],
                    "actions": ["Implement part sensors", "Improve training", "Add visual indicators"]
                },
                {
                    "failure_mode": "Wrong Part",
                    "effects": ["Functional failure", "Performance issues", "Rework required"],
                    "causes": ["Similar parts confusion", "Inadequate labeling", "Operator error"],
                    "controls": ["Part identification labels", "Barcode scanning", "First-article inspection"],
                    "actions": ["Improve part labeling", "Implement barcode verification", "Enhance operator training"]
                },
                {
                    "failure_mode": "Reversed Part",
                    "effects": ["Functional failure", "Assembly interference", "Performance issues"],
                    "causes": ["Asymmetric parts", "Inadequate work instruction", "Operator error"],
                    "controls": ["Orientation guides", "Poka-yoke fixtures", "Visual aids"],
                    "actions": ["Design orientation aids", "Implement poka-yoke devices", "Improve work instructions"]
                },
                {
                    "failure_mode": "Part Damage",
                    "effects": ["Functional failure", "Safety hazard", "Performance degradation"],
                    "causes": ["Improper handling", "Inadequate packaging", "Tool misuse"],
                    "controls": ["Proper handling procedures", "Protective packaging", "Tooling design"],
                    "actions": ["Improve handling training", "Enhance packaging", "Review tooling design"]
                }
            ],
            "Bolt Fastening": [
                {
                    "failure_mode": "Insufficient Torque",
                    "effects": ["Loose joint", "Vibration-induced failure", "Safety hazard"],
                    "causes": ["Incorrect torque setting", "Tool calibration issue", "Operator error"],
                    "controls": ["Torque-controlled tools", "Regular calibration", "Torque monitoring"],
                    "actions": ["Implement torque monitoring", "Improve calibration program", "Enhance operator training"]
                },
                {
                    "failure_mode": "Over Torque",
                    "effects": ["Thread damage", "Component cracking", "Fastener failure"],
                    "causes": ["Incorrect torque setting", "Tool malfunction", "Lack of monitoring"],
                    "controls": ["Torque limits", "Tool maintenance", "Process monitoring"],
                    "actions": ["Set torque limits", "Improve tool maintenance", "Add process monitoring"]
                },
                {
                    "failure_mode": "Missing Fastener",
                    "effects": ["Joint integrity compromised", "Vibration issues", "Safety hazard"],
                    "causes": ["Operator forgetfulness", "Inadequate poka-yoke", "Poor work sequence"],
                    "controls": ["Fastener tracking", "Poka-yoke devices", "Final inspection"],
                    "actions": ["Implement fastener tracking", "Add poka-yoke solutions", "Improve inspection methods"]
                }
            ],
            "Press-fit/Riveting": [
                {
                    "failure_mode": "Insufficient Press-fit Force",
                    "effects": ["Loose fit", "Functional failure", "Vibration issues"],
                    "causes": ["Incorrect force setting", "Equipment calibration", "Material variation"],
                    "controls": ["Force monitoring", "Calibration program", "Material inspection"],
                    "actions": ["Implement force monitoring", "Improve calibration", "Add material inspection"]
                }
            ],
            "Inspection/Debugging": [
                {
                    "failure_mode": "Missing Critical Dimension Inspection",
                    "effects": ["Defective product escape", "Customer complaints", "Safety issues"],
                    "causes": ["Inadequate inspection plan", "Operator error", "Time pressure"],
                    "controls": ["Inspection checklist", "Automated inspection", "First-article verification"],
                    "actions": ["Improve inspection planning", "Implement automated inspection", "Strengthen quality culture"]
                }
            ]
        }
        
        # 尝试从JSON文件加载知识库
        self.load_from_file(json_file)

    def get_failure_modes_by_type(self, assembly_type: str) -> list:
        """
        根据装配类型获取相关的失效模式
        
        Args:
            assembly_type: 装配类型
            
        Returns:
            相关的失效模式列表
        """
        return self.failure_library.get(assembly_type, [])

    def get_all_failure_modes(self) -> dict:
        """
        获取所有失效模式
        
        Returns:
            所有失效模式的字典
        """
        return self.failure_library

    def add_failure_mode(self, assembly_type: str, failure_mode_data: dict):
        """
        添加新的失效模式到知识库
        
        Args:
            assembly_type: 装配类型
            failure_mode_data: 失效模式数据
        """
        if assembly_type not in self.failure_library:
            self.failure_library[assembly_type] = []
        
        self.failure_library[assembly_type].append(failure_mode_data)

    def save_to_file(self, filename: str):
        """
        将知识库保存到文件
        
        Args:
            filename: 保存的文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.failure_library, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving knowledge base to {filename}: {e}")

    def load_from_file(self, filename: str):
        """
        从文件加载知识库
        
        Args:
            filename: 加载的文件名
        """
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    self.failure_library = json.load(f)
            else:
                print(f"Knowledge base file {filename} not found. Using default library.")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in {filename}. Using default library.")
        except Exception as e:
            print(f"Error loading knowledge base from {filename}: {e}")


# 创建全局知识库实例
knowledge_base = AssemblyKnowledgeBase()


def get_knowledge_base():
    """
    获取知识库实例
    
    Returns:
        AssemblyKnowledgeBase实例
    """
    return knowledge_base