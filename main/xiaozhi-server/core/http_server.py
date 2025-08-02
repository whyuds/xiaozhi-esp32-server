import asyncio
import json
from aiohttp import web
from config.logger import setup_logging
from core.api.ota_handler import OTAHandler
from core.api.vision_handler import VisionHandler

TAG = __name__


class SimpleHttpServer:
    def __init__(self, config: dict, ws_server):
        self.config = config
        self.ws_server = ws_server  # 引用WebSocketServer以便访问活动连接
        self.logger = setup_logging()
        self.ota_handler = OTAHandler(config)
        self.vision_handler = VisionHandler(config)

    def _get_websocket_url(self, local_ip: str, port: int) -> str:
        """获取websocket地址

        Args:
            local_ip: 本地IP地址
            port: 端口号

        Returns:
            str: websocket地址
        """
        server_config = self.config["server"]
        websocket_config = server_config.get("websocket")

        if websocket_config and "你" not in websocket_config:
            return websocket_config
        else:
            return f"ws://{local_ip}:{port}/xiaozhi/v1/"

    async def start(self):
        server_config = self.config["server"]
        host = server_config.get("ip", "0.0.0.0")
        port = int(server_config.get("http_port", 8003))

        if port:
            app = web.Application()

            read_config_from_api = server_config.get("read_config_from_api", False)

            if not read_config_from_api:
                # 如果没有开启智控台，只是单模块运行，就需要再添加简单OTA接口，用于下发websocket接口
                app.add_routes(
                    [
                        web.get("/xiaozhi/ota/", self.ota_handler.handle_get),
                        web.post("/xiaozhi/ota/", self.ota_handler.handle_post),
                        web.options("/xiaozhi/ota/", self.ota_handler.handle_post),
                    ]
                )
            # 添加路由
            app.add_routes(
                [
                    web.get("/mcp/vision/explain", self.vision_handler.handle_get),
                    web.post("/mcp/vision/explain", self.vision_handler.handle_post),
                    web.options("/mcp/vision/explain", self.vision_handler.handle_post),
                ]
            )
            # 新增system_chat接口
            app.add_routes([
                web.post("/mcp/system_chat", self.handle_system_chat),
            ])

            # 运行服务
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host, port)
            await site.start()

            # 保持服务运行
            while True:
                await asyncio.sleep(3600)  # 每隔 1 小时检查一次

    async def handle_system_chat(self, request):
        """通过HTTP接口以system身份向指定设备发送消息并触发LLM回复"""
        try:
            data = await request.json()
        except Exception:
            return web.json_response({"error": "Invalid JSON"}, status=400)

        device_id = data.get("device_id")
        if not device_id:
            return web.json_response({"error": "device_id required"}, status=400)

        system_prompt = data.get("system_prompt")
        message = data.get("message")

        # 查找对应的连接
        target_conn = None
        for handler in self.ws_server.active_connections:
            if getattr(handler, "device_id", None) == device_id:
                target_conn = handler
                break

        if target_conn is None:
            return web.json_response({"error": "device not connected"}, status=404)

        # 仅支持openai类型的LLM
        if "openai" not in target_conn.llm.__class__.__module__:
            return web.json_response({"error": "LLM provider not supported"}, status=400)

        # 更新system prompt
        if system_prompt:
            target_conn.change_system_prompt(system_prompt)

        # 发送对话内容
        if message:
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, target_conn.chat, message)

        return web.json_response({"result": "ok"})
