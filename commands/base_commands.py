# 基础命令处理模块
from config import ADMIN_GROUP_ID, TEST_GROUP_ID

def is_announce_command(message_text):
    """检查是否为公告命令"""
    return message_text.startswith("=announce")


def is_feedback_command(message_text):
    """检查是否为反馈命令"""
    return message_text.startswith("=ref")


def is_mute_command(message_text):
    """检查是否为禁言命令（仅限管理员群或测试群）"""
    return message_text.startswith("=mute")


def is_report_command(message_text):
    """检查是否为举报命令"""
    return message_text.startswith("=report")


def is_help_command(message_text):
    """检查是否为帮助命令"""
    return message_text == "=?" or message_text.startswith("=help")


def is_modify_command(message_text):
    """检查是否为修改玩家数据命令"""
    return message_text.startswith("=modify")

def is_info_command(message_text):
    """检查是否为战绩查询指令"""
    return message_text.startswith("=info") or message_text.startswith("=i")

def is_reg_command(message_text):
    """检查是否为注册指令"""
    return message_text.startswith("=reg") or message_text.startswith("=r") or message_text.startswith("=register")

def is_freg_command(message_text):
    """检查是否为注册指令"""
    return message_text.startswith("=freg") or message_text.startswith("=fr")