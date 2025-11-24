import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import assembly_struct
import risk_calc_assembly
import knowledge_base
import data_handler_assembly
import pandas as pd
import json


class AssemblyFMEAApp:
    """
    装配专用PFMEA应用程序主类
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("设备装配工厂PFMEA系统")
        self.root.geometry("1200x800")
        
        # 初始化知识库
        self.kb = knowledge_base.get_knowledge_base()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """
        创建主界面组件
        """
        # 创建顶部工具栏
        self.create_toolbar()
        
        # 创建主框架（左右布局）
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧结构树框架
        left_frame = ttk.Frame(main_frame)
        main_frame.add(left_frame, weight=1)
        
        # 右侧数据编辑区域
        right_frame = ttk.Frame(main_frame)
        main_frame.add(right_frame, weight=3)
        
        # 创建结构树
        self.create_structure_tree(left_frame)
        
        # 创建数据编辑区域
        self.create_data_area(right_frame)
        
    def create_toolbar(self):
        """
        创建顶部工具栏
        """
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # 工具栏按钮
        buttons = [
            ("导入BOM", self.import_bom),
            ("导入工序", self.import_process),
            ("生成报告", self.generate_report),
            ("备份数据", self.backup_data),
            ("添加失效模式", self.add_failure_mode)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(toolbar, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=2)
            
    def create_structure_tree(self, parent):
        """
        创建左侧装配结构树
        """
        label = ttk.Label(parent, text="装配结构", font=("Arial", 12, "bold"))
        label.pack(pady=5)
        
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame)
        self.tree.heading("#0", text="工厂层级结构")
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # 绑定选择事件
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # 添加示例数据
        self.populate_sample_structure()
        
    def create_data_area(self, parent):
        """
        创建右侧数据编辑区域
        """
        # 创建选项卡控件
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # PFMEA数据录入选项卡
        pfmea_frame = ttk.Frame(notebook)
        notebook.add(pfmea_frame, text="PFMEA数据录入")
        
        # 创建数据表格
        self.create_data_table(pfmea_frame)
        
        # 风险评估选项卡
        risk_frame = ttk.Frame(notebook)
        notebook.add(risk_frame, text="风险评估")
        
        # 风险矩阵展示（占位符）
        risk_label = ttk.Label(risk_frame, text="风险矩阵展示区域")
        risk_label.pack(pady=20)
        
    def create_data_table(self, parent):
        """
        创建数据表格
        """
        # 创建带滚动条的表格
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 定义列
        columns = assembly_struct.get_assembly_columns()
        
        # 创建表格
        self.data_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题和宽度
        for col in columns:
            self.data_table.heading(col, text=col)
            self.data_table.column(col, width=100)
            
        # 滚动条
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.data_table.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.data_table.xview)
        self.data_table.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 布局
        self.data_table.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # 绑定双击事件进行编辑
        self.data_table.bind("<Double-1>", self.on_cell_double_click)
        
        # 添加示例行
        self.add_sample_data()
        
        # 初始化编辑控件引用
        self.entry_edit = None
        self.combo_edit = None
        
    def populate_sample_structure(self):
        """
        添加示例结构树数据
        """
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 添加工厂节点
        factory = self.tree.insert("", "end", text="XX设备厂", open=True)
        
        # 添加车间节点
        workshop = self.tree.insert(factory, "end", text="总装车间", open=True)
        
        # 添加生产线节点
        line = self.tree.insert(workshop, "end", text="机器人手臂装配线", open=True)
        
        # 添加工位节点
        station = self.tree.insert(line, "end", text="03工位（螺栓紧固）", open=True)
        
        # 添加工序节点
        process = self.tree.insert(station, "end", text="03-01工序（底座螺栓紧固）")
        
        # 强制刷新界面
        self.tree.update_idletasks()
        
    def add_sample_data(self):
        """
        添加示例数据行
        """
        # 示例数据
        sample_data = [
            "机器人装配线01",
            "03工位",
            "SOP-A-2024-001",
            "BOM-V2.1",
            "拧紧机#TL-001",
            "4颗M12螺栓紧固，力矩45N·m",
            "力矩不足",
            "BOLT-M12-001",
            "螺栓M12",
            "M12×40",
            "电动扳手#DW-01",
            "设备运行中松动，引发安全事故",
            "8",
            "未使用扭矩控制工具",
            "7",
            "力矩监控装置",
            "首件检查",
            "过程巡检",
            "8",
            "448",
            "高风险",
            "增加扭矩监控装置并联网",
            "设备部",
            "2024-12-31",
            "已安装扭矩监控装置",
            "6",
            "3",
            "4",
            "72",
            "中风险"
        ]
        
        self.data_table.insert("", "end", values=sample_data)
        
    def on_tree_select(self, event):
        """
        处理树形结构选择事件
        """
        selected_items = self.tree.selection()
        if selected_items:
            # selection()返回一个元组，取第一个元素作为选中的项目
            selected_item = selected_items[0]
            item_text = self.tree.item(selected_item, "text")
            print(f"Selected: {item_text}")

            # 根据选中的节点更新右侧数据表格
            self.update_data_table_for_selection(item_text)
            
    def update_data_table_for_selection(self, selection_text):
        """
        根据选中的结构树节点更新数据表格内容
        """
        # 清空当前表格内容
        for item in self.data_table.get_children():
            self.data_table.delete(item)

        # 这里应该根据selection_text过滤数据并显示
        # 目前使用示例数据演示功能
        if "工位" in selection_text or "工序" in selection_text:
            # 添加与选中节点相关的数据行
            # 在实际应用中，这些数据应该来自数据库或数据文件
            sample_data = [
                "机器人装配线01",
                "03工位",
                "SOP-A-2024-001",
                "BOM-V2.1",
                "拧紧机#TL-001",
                "4颗M12螺栓紧固，力矩45N·m",
                "力矩不足",
                "BOLT-M12-001",
                "螺栓M12",
                "M12×40",
                "电动扳手#DW-01",
                "设备运行中松动，引发安全事故",
                "8",
                "未使用扭矩控制工具",
                "7",
                "力矩监控装置",
                "首件检查",
                "过程巡检",
                "8",
                "448",
                "高风险",
                "增加扭矩监控装置并联网",
                "设备部",
                "2024-12-31",
                "已安装扭矩监控装置",
                "6",
                "3",
                "4",
                "72",
                "中风险"
            ]

            self.data_table.insert("", "end", values=sample_data)
        elif "生产线" in selection_text:
            # 可以添加不同的示例数据来模拟不同层级的选择
            sample_data = [
                "机器人装配线01",
                "02工位",
                "SOP-A-2024-002",
                "BOM-V2.1",
                "压装机#YZ-001",
                "轴承压装至指定深度",
                "压装不到位",
                "BEARING-6204",
                "深沟球轴承",
                "6204",
                "液压压机#YY-01",
                "轴承受力不均，产生异响",
                "7",
                "定位销磨损",
                "6",
                "压力传感器",
                "首件检查",
                "过程巡检",
                "7",
                "294",
                "中风险",
                "更换定位销并校准",
                "设备部",
                "2024-12-31",
                "已完成更换",
                "5",
                "4",
                "5",
                "100",
                "低风险"
            ]

            self.data_table.insert("", "end", values=sample_data)
        else:
            # 默认显示一些示例数据
            self.add_sample_data()

    def on_cell_double_click(self, event):
        """
        处理单元格双击事件，实现原地编辑
        """
        # 如果已有编辑控件存在，先销毁它
        if self.entry_edit:
            self.entry_edit.destroy()
            self.entry_edit = None
        if self.combo_edit:
            self.combo_edit.destroy()
            self.combo_edit = None
            
        # 获取点击区域
        region = self.data_table.identify("region", event.x, event.y)
        if region != "cell":
            return

        # 获取选中的项和列
        row_id = self.data_table.identify_row(event.y)
        column = self.data_table.identify_column(event.x)
        
        # 获取单元格边界框和当前值
        try:
            x, y, width, height = self.data_table.bbox(row_id, column)
        except ValueError:
            # 如果无法获取边界框，则返回
            return
            
        value = self.data_table.set(row_id, column)
        
        # 判断是否为数值列（需要下拉框的列）
        numerical_columns = ["Severity (S)", "Occurrence (O)", "Detection (D)", 
                           "Severity (A)", "Occurrence (A)", "Detection (A)"]
        column_heading = self.data_table.heading(column)['text']
        
        if column_heading in numerical_columns:
            # 对于数值列，使用Combobox
            self.combo_edit = ttk.Combobox(self.data_table, values=[str(i) for i in range(1, 11)], state='readonly')
            self.combo_edit.place(x=x, y=y, width=width, height=height)
            self.combo_edit.set(value)
            self.combo_edit.focus()

            def save_edit(event):
                if self.combo_edit is not None:
                    self.data_table.set(row_id, column, self.combo_edit.get())
                    self.combo_edit.destroy()
                    self.combo_edit = None
                # 更新RPN值
                self.update_rpn(row_id)

            self.combo_edit.bind('<<ComboboxSelected>>', save_edit)
            self.combo_edit.bind('<FocusOut>', lambda e: save_edit(None))
        else:
            # 对于其他列，使用Entry
            self.entry_edit = tk.Entry(self.data_table)
            self.entry_edit.place(x=x, y=y, width=width, height=height)
            self.entry_edit.insert(0, value)
            self.entry_edit.focus()
            self.entry_edit.select_range(0, tk.END)

            def save_edit(event):
                if self.entry_edit is not None:
                    self.data_table.set(row_id, column, self.entry_edit.get())
                    self.entry_edit.destroy()
                    self.entry_edit = None
                # 更新RPN值
                self.update_rpn(row_id)

            self.entry_edit.bind('<Return>', save_edit)
            self.entry_edit.bind('<FocusOut>', lambda e: save_edit(None))
        
    def create_edit_window(self, item, column, current_value):
        """
        创建单元格编辑窗口
        """
        # 创建顶层窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑单元格")
        edit_window.geometry("300x150")
        
        # 获取列标题
        col_id = int(column[1:]) - 1  # 转换为0索引
        col_name = self.data_table["columns"][col_id]
        
        # 标签
        label = ttk.Label(edit_window, text=f"编辑 {col_name}:")
        label.pack(pady=5)
        
        # 输入框
        entry = ttk.Entry(edit_window, width=30)
        entry.insert(0, current_value)
        entry.pack(pady=5)
        entry.focus()
        
        # 保存按钮
        def save_edit():
            new_value = entry.get()
            self.data_table.set(item, column, new_value)
            edit_window.destroy()
            
        save_btn = ttk.Button(edit_window, text="保存", command=save_edit)
        save_btn.pack(pady=5)
        
        # 绑定回车键保存
        entry.bind("<Return>", lambda e: save_edit())
        
    def import_bom(self):
        """
        导入BOM功能
        """
        file_path = filedialog.askopenfilename(
            title="选择BOM文件",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                bom_data = data_handler_assembly.load_bom_excel(file_path)
                messagebox.showinfo("成功", f"BOM数据导入成功，共导入 {len(bom_data)} 条记录")
                self.update_structure_tree_with_bom(bom_data)
            except Exception as e:
                messagebox.showerror("错误", f"BOM数据导入失败: {str(e)}")
        
    def import_process(self):
        """
        导入工序功能
        """
        file_path = filedialog.askopenfilename(
            title="选择工序文件",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                process_data = data_handler_assembly.load_process_excel(file_path)
                messagebox.showinfo("成功", f"工序数据导入成功，共导入 {len(process_data)} 条记录")
            except Exception as e:
                messagebox.showerror("错误", f"工序数据导入失败: {str(e)}")
        
    def generate_report(self):
        """
        生成报告功能
        """
        # 获取表格数据
        data = []
        # 添加表头
        data.append(self.data_table["columns"])
        # 添加数据行
        for item in self.data_table.get_children():
            data.append(self.data_table.item(item)["values"])
            
        file_path = filedialog.asksaveasfilename(
            title="保存报告",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith(".xlsx"):
                    data_handler_assembly.save_pfmea_report(data, file_path, "excel")
                elif file_path.endswith(".json"):
                    data_handler_assembly.save_pfmea_report(data, file_path, "json")
                messagebox.showinfo("成功", "报告生成成功")
            except Exception as e:
                messagebox.showerror("错误", f"报告生成失败: {str(e)}")
        
    def backup_data(self):
        """
        备份数据功能
        """
        # 获取表格数据
        data = []
        # 添加表头
        data.append(self.data_table["columns"])
        # 添加数据行
        for item in self.data_table.get_children():
            data.append(self.data_table.item(item)["values"])
            
        file_path = filedialog.asksaveasfilename(
            title="备份数据",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("SQLite files", "*.db"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith(".json"):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                elif file_path.endswith(".db"):
                    data_handler_assembly.save_sqlite_pfmea(data, file_path)
                messagebox.showinfo("成功", "数据备份成功")
            except Exception as e:
                messagebox.showerror("错误", f"数据备份失败: {str(e)}")
        
    def add_failure_mode(self):
        """
        添加失效模式功能
        """
        # 创建添加失效模式窗口
        self.create_add_failure_mode_window()
        
    def update_structure_tree_with_bom(self, bom_data):
        """
        根据导入的BOM数据更新左侧结构树
        """
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 添加工厂节点
        factory = self.tree.insert("", "end", text="XX设备厂", open=True)
        
        # 添加车间节点
        workshop = self.tree.insert(factory, "end", text="总装车间", open=True)
        
        # 从BOM数据中提取生产线信息
        lines = {}
        stations = {}
        
        for item in bom_data:
            # 提取生产线和工位信息（使用BOM模板中的中文列名）
            line_number = item.get("生产线编号", "未知生产线")
            station_number = item.get("工位编号", "未知工位")
            process_step = item.get("工序步骤", "未知工序")
            assembly_function = item.get("装配功能", "未知装配功能")
            
            # 创建生产线节点（如果不存在）
            if line_number not in lines:
                lines[line_number] = self.tree.insert(workshop, "end", text=line_number, open=True)
                
            # 创建工位节点（如果不存在）
            station_key = f"{line_number}-{station_number}"
            if station_key not in stations:
                stations[station_key] = self.tree.insert(lines[line_number], "end", text=station_number, open=True)
                
            # 创建工序步骤节点
            process_key = f"{station_key}-{process_step}"
            process_node = self.tree.insert(stations[station_key], "end", text=process_step, open=True)
            
            # 创建装配功能节点
            self.tree.insert(process_node, "end", text=assembly_function, open=True)
        
        # 强制刷新界面
        self.tree.update_idletasks()
        
    def update_rpn(self, row_id):
        """
        更新RPN值
        """
        try:
            severity = int(self.data_table.set(row_id, "Severity (S)")) if self.data_table.set(row_id, "Severity (S)").isdigit() else 0
            occurrence = int(self.data_table.set(row_id, "Occurrence (O)")) if self.data_table.set(row_id, "Occurrence (O)").isdigit() else 0
            detection = int(self.data_table.set(row_id, "Detection (D)")) if self.data_table.set(row_id, "Detection (D)").isdigit() else 0
            rpn = severity * occurrence * detection
            self.data_table.set(row_id, "RPN", str(rpn))
        except (ValueError, tk.TclError):
            self.data_table.set(row_id, "RPN", "")
            
        try:
            severity_a = int(self.data_table.set(row_id, "Severity (A)")) if self.data_table.set(row_id, "Severity (A)").isdigit() else 0
            occurrence_a = int(self.data_table.set(row_id, "Occurrence (A)")) if self.data_table.set(row_id, "Occurrence (A)").isdigit() else 0
            detection_a = int(self.data_table.set(row_id, "Detection (A)")) if self.data_table.set(row_id, "Detection (A)").isdigit() else 0
            rpn_a = severity_a * occurrence_a * detection_a
            self.data_table.set(row_id, "RPN (A)", str(rpn_a))
        except (ValueError, tk.TclError):
            self.data_table.set(row_id, "RPN (A)", "")


    def create_add_failure_mode_window(self):
        """
        创建添加失效模式窗口
        """
        add_window = tk.Toplevel(self.root)
        add_window.title("添加失效模式")
        add_window.geometry("500x400")

        # 选择装配类型
        type_label = ttk.Label(add_window, text="装配类型:")
        type_label.pack(pady=5)
        
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(add_window, textvariable=type_var, 
                                 values=["Part Assembly", "Bolt Fastening", "Press-fit/Riveting", "Inspection/Debugging"])
        type_combo.pack(pady=5)
        type_combo.current(0)
        
        # 失效模式输入
        mode_label = ttk.Label(add_window, text="失效模式:")
        mode_label.pack(pady=5)
        
        mode_entry = ttk.Entry(add_window, width=50)
        mode_entry.pack(pady=5)
        
        # 从知识库添加按钮
        def add_from_knowledge_base():
            selected_type = type_var.get()
            failure_modes = self.kb.get_failure_modes_by_type(selected_type)
            
            if failure_modes:
                # 显示可用的失效模式
                mode_list = [mode["failure_mode"] for mode in failure_modes]
                mode_entry["values"] = mode_list
                messagebox.showinfo("提示", f"从知识库加载了 {len(failure_modes)} 个 {selected_type} 类型的失效模式")
            else:
                messagebox.showinfo("提示", f"知识库中没有找到 {selected_type} 类型的失效模式")
                
        kb_btn = ttk.Button(add_window, text="从知识库加载", command=add_from_knowledge_base)
        kb_btn.pack(pady=5)


def main():
    """
    主函数
    """
    root = tk.Tk()
    app = AssemblyFMEAApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()