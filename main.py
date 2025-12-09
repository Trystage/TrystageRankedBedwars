import asyncio
import json
import traceback

import websockets

from commands.base_commands import *
from config import WEBSOCKET_HOST, WEBSOCKET_PORT
from handlers.announcement_handler import handle_announce_command
from handlers.feedback_handler import handle_feedback_command
from handlers.help_handler import handle_help_command
from handlers.report_handler import handle_report_command
from handlers.data_handler import handle_modify_command, handle_info_command, handle_freg_command, handle_reg_command
from utils.file_utils import FileUtils
from utils.misc_utils import truncate_error_message
from utils.websocket_utils import send_message


async def handle_message(websocket):
    print("运行在ws://0.0.0.0:12001/ws")
    print("等待消息...")
    async for message in websocket:
        try:
            data = json.loads(message)
            if "post_type" in data and data["post_type"] == "message":
                user_id = data["user_id"]
                message_text = data["message"]
                message_type = data["message_type"]
                group_id = data.get("group_id", None)

                response_message = None

                # 处理公告命令
                if is_announce_command(message_text):
                    await handle_announce_command(websocket, message_text, user_id, group_id)

                # 处理反馈命令
                elif is_feedback_command(message_text):
                    await handle_feedback_command(websocket, message_text, user_id, group_id)

                # 处理举报命令
                elif is_report_command(message_text):
                    await handle_report_command(websocket, message_text, user_id, group_id)

                # 处理帮助命令
                elif is_help_command(message_text):
                    response_message = await handle_help_command(websocket, message_text, user_id, group_id)

                # 处理查询命令
                elif is_info_command(message_text):
                    response_message = await handle_info_command(websocket, message_text, user_id, group_id)

                # 处理修改玩家数据命令
                elif is_modify_command(message_text):
                    await handle_modify_command(websocket, message_text, user_id, group_id)

                # 处理强制注册命令
                elif is_freg_command(message_text):
                    await handle_freg_command(websocket, message_text, user_id, group_id)

                # 处理注册命令
                elif is_reg_command(message_text):
                    await handle_reg_command(websocket, message_text, user_id, group_id)

                # 发送响应消息（如果有的话）
                if response_message:
                    response_json = json.dumps(response_message)
                    await websocket.send(response_json)

        except Exception as e:
            error_msg = truncate_error_message(str(e))
            print(f"处理消息时出错: {error_msg}")
            traceback.print_exc()
            # 如果是消息类型，发送错误响应
            if "post_type" in data and data["post_type"] == "message":
                user_id = data.get("user_id")
                group_id = data.get("group_id", None)
                await send_message(websocket, f"处理消息时出错: {e}", user_id, group_id)


async def on_connect(websocket, path):
    print("连接建立")
    try:
        await handle_message(websocket)
    except Exception as e:
        print(f"处理消息时出错: {e}")
    finally:
        print("连接断开")


# 启动服务器
async def main():
    # 初始化数据文件
    FileUtils.initialize_data_files()

    start_server = await websockets.serve(on_connect, WEBSOCKET_HOST, WEBSOCKET_PORT)
    print("WebSocket 服务器已启动")
    print(f"运行在ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}/ws")
    await start_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
