import asyncio
import json

import websockets

from commands.base_commands import is_announce_command, is_feedback_command, is_mute_command, is_report_command, \
    is_help_command
from handlers.announcement_handler import handle_announce_command
from handlers.feedback_handler import handle_feedback_command
from handlers.help_handler import handle_help_command
from handlers.report_handler import handle_report_command
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
                    await handle_announce_command(message_text, group_id, websocket)

                # 处理反馈命令
                elif is_feedback_command(message_text):
                    await handle_feedback_command(message_text, user_id, group_id, websocket)

                # 处理举报命令
                elif is_report_command(message_text):
                    await handle_report_command(message_text, user_id, group_id, websocket)

                # 处理帮助命令
                elif is_help_command(message_text):
                    response_message = await handle_help_command(message_text, user_id, group_id, websocket)

                # 发送响应消息（如果有的话）
                if response_message:
                    response_json = json.dumps(response_message)
                    await websocket.send(response_json)

        except Exception as e:
            print(f"处理消息时出错: {e}")
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
start_server = websockets.serve(on_connect, "0.0.0.0", 12001)
print("WebSocket 服务器已启动")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
