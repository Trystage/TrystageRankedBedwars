import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.uuid_utils import UUIDUtils

def test_uuid_formatting():
    """测试UUID格式化功能"""
    print("测试UUID格式化功能...")
    
    # 测试用例
    test_cases = [
        # (输入, 期望输出)
        ("d4f0c8c97bde4fbba8d98d8e9f0a1b2c", "d4f0c8c9-7bde-4fbb-a8d9-8d8e9f0a1b2c"),  # 不带连字符
        ("D4F0C8C97BDE4FBBA8D98D8E9F0A1B2C", "d4f0c8c9-7bde-4fbb-a8d9-8d8e9f0a1b2c"),  # 大写不带连字符
        ("d4f0c8c9-7bde-4fbb-a8d9-8d8e9f0a1b2c", "d4f0c8c9-7bde-4fbb-a8d9-8d8e9f0a1b2c"),  # 已经是正确格式
        ("D4F0C8C9-7BDE-4FBB-A8D9-8D8E9F0A1B2C", "d4f0c8c9-7bde-4fbb-a8d9-8d8e9f0a1b2c"),  # 大写带连字符
    ]
    
    print("\n测试正常情况:")
    for i, (input_uuid, expected) in enumerate(test_cases, 1):
        try:
            result = UUIDUtils.format_uuid(input_uuid)
            if result == expected:
                print(f"  测试 {i}: 通过 - '{input_uuid}' -> '{result}'")
            else:
                print(f"  测试 {i}: 失败 - '{input_uuid}' -> '{result}' (期望: '{expected}')")
        except Exception as e:
            print(f"  测试 {i}: 异常 - '{input_uuid}' -> 错误: {e}")
    
    # 测试异常情况
    print("\n测试异常情况:")
    invalid_cases = [
        "invalid-uuid",  # 包含非十六进制字符
        "d4f0c8c97bde4fbba8d98d8e9f0a1b2",  # 长度不足
        "d4f0c8c97bde4fbba8d98d8e9f0a1b2c1",  # 长度过长
        "",  # 空字符串
    ]
    
    for i, invalid_uuid in enumerate(invalid_cases, 1):
        try:
            result = UUIDUtils.format_uuid(invalid_uuid)
            print(f"  异常测试 {i}: 失败 - '{invalid_uuid}' 应该抛出异常但返回了 '{result}'")
        except ValueError as e:
            print(f"  异常测试 {i}: 通过 - '{invalid_uuid}' 正确抛出异常: {e}")
        except Exception as e:
            print(f"  异常测试 {i}: 意外异常 - '{invalid_uuid}' -> 错误: {e}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_uuid_formatting()