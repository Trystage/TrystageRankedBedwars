#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试所有处理函数参数顺序的脚本
"""

import sys
import os
import inspect

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handlers.data_handler import handle_modify_command, handle_info_command, handle_reg_command, handle_freg_command
from handlers.help_handler import handle_help_command
from handlers.feedback_handler import handle_feedback_command
from handlers.report_handler import handle_report_command
from handlers.announcement_handler import handle_announce_command
from handlers.group_handler import handle_add_command


def check_function_signature(func):
    """检查函数签名，确保参数顺序正确"""
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    
    # 检查参数顺序是否为 [websocket, message_text, user_id, group_id] 或其子集
    expected_order = ['websocket', 'message_text', 'user_id', 'group_id']
    
    # 检查前几个参数是否符合预期顺序
    valid = True
    for i, expected_param in enumerate(expected_order):
        if i < len(params) and params[i] != expected_param:
            # 特殊情况：handle_announce_command 只有三个参数
            if func.__name__ == 'handle_announce_command' and params == ['websocket', 'message_text', 'group_id']:
                continue
            print(f"错误: {func.__name__} 函数的参数顺序不正确")
            print(f"  当前参数顺序: {params}")
            print(f"  期望参数顺序: {expected_order[:len(params)]}")
            valid = False
            break
    
    if valid:
        print(f"✓ {func.__name__} 参数顺序正确: {params}")
    return valid


def main():
    """主函数"""
    print("开始检查所有处理函数的参数顺序...")
    
    # 定义所有需要检查的处理函数
    functions_to_check = [
        handle_modify_command,
        handle_info_command,
        handle_reg_command,
        handle_freg_command,
        handle_help_command,
        handle_feedback_command,
        handle_report_command,
        handle_announce_command,
        handle_add_command,
    ]
    
    # 检查每个函数
    all_correct = True
    for func in functions_to_check:
        if not check_function_signature(func):
            all_correct = False
    
    if all_correct:
        print("\n✓ 所有处理函数的参数顺序都正确!")
    else:
        print("\n✗ 存在参数顺序不正确的函数，请检查并修正!")
        
    return all_correct


if __name__ == "__main__":
    main()