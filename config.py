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

# 资源目录
RESOURCE_DIR = "resource"

# 资源文件路径
FONT_FILE = "1.ttf"
# 缓存目录
CACHE_DIR = "cache"

# 日志目录
LOGS_DIR = "logs"


# 延迟加载群组ID配置，避免循环导入
def get_rbw_group_ids():
    from utils.file_utils import FileUtils
    return FileUtils.get_rbw_group_ids()
def get_admins():
    from utils.file_utils import FileUtils
    return FileUtils.get_admins()

ADMINS = get_admins()
GROUP_IDS = get_rbw_group_ids()