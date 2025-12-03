import re

class UUIDUtils:
    """UUID工具类，用于处理UUID格式统一"""
    
    @staticmethod
    def format_uuid(uuid_str: str) -> str:
        """
        将UUID格式化为带连字符的标准格式
        支持32位不带连字符和36位带连字符的UUID
        
        Args:
            uuid_str (str): 原始UUID字符串
            
        Returns:
            str: 带连字符的标准UUID格式
        """
        # 移除可能存在的连字符
        clean_uuid = uuid_str.replace('-', '')
        
        # 验证是否为有效的32位UUID
        if len(clean_uuid) != 32:
            raise ValueError(f"无效的UUID长度: {len(clean_uuid)}, 应该是32位")
        
        # 验证是否只包含十六进制字符
        if not re.match(r'^[0-9a-fA-F]+$', clean_uuid):
            raise ValueError("UUID包含非十六进制字符")
        
        # 格式化为标准的带连字符UUID
        formatted_uuid = f"{clean_uuid[0:8]}-{clean_uuid[8:12]}-{clean_uuid[12:16]}-{clean_uuid[16:20]}-{clean_uuid[20:32]}"
        return formatted_uuid.lower()
    
    @staticmethod
    def is_valid_uuid(uuid_str: str) -> bool:
        """
        验证UUID是否为有效格式
        
        Args:
            uuid_str (str): UUID字符串
            
        Returns:
            bool: 是否为有效UUID
        """
        try:
            UUIDUtils.format_uuid(uuid_str)
            return True
        except ValueError:
            return False