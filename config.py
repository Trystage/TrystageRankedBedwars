# 项目配置文件
from pathlib import Path

# WebSocket服务器配置
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 20002

# 群组ID配置
ADMIN_GROUP_ID = 458136700
TARGET_GROUP_ID = 649523125
BACKUP_GROUP_ID = 171357599
TEST_GROUP_ID = 695789887

PROJECT_ROOT = Path(__file__).parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
# 资源目录
RESOURCE_DIR = str(PROJECT_ROOT / "resource")

# 资源文件路径
FONT_FILE = str(PROJECT_ROOT / "resource" / "SourceHanSansSC-VF.ttf")

# 缓存目录
CACHE_DIR = str(PROJECT_ROOT / "cache")

# 日志目录
LOGS_DIR = str(PROJECT_ROOT / "logs")


# 延迟加载群组ID配置，避免循环导入
def get_rbw_group_ids():
    from utils.file_utils import FileUtils
    return FileUtils.get_rbw_group_ids()
    
def get_admins():
    from utils.file_utils import FileUtils
    return FileUtils.get_admins()

# 将ADMINS和GROUP_IDS改为属性，延迟加载
class _LazyConfig:
    @property
    def ADMINS(self):
        return get_admins()
        
    @property
    def GROUP_IDS(self):
        return get_rbw_group_ids()

# 创建配置实例
CONFIG = _LazyConfig()