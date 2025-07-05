# AI Illustrate Project

## 项目包含

1. 多模态 RAG Demo.
- 支持文本, PDF, Word, Excel, PPT, 视频, 音频

2. Agent Demo.


## 

### 前端 

### 后端

按照以下步骤来运行项目：


1. 安装依赖:


   pip install -r requirements.txt



2. 启动 Redis:

    确保您已经安装并运行了 Redis 服务器，Celery 需要它作为消息代理。


3. 启动 Celery Worker:

    在您的项目根目录打开一个终端并运行：

   celery -A tasks worker --loglevel=info



4. 启动 FastAPI 应用:
      在您的项目根目录打开另一个终端并运行：

   uvicorn main:app --reload

