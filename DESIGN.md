# DESIGN

## 前端设计

### 功能拆分

#### 功能性需求
1. 用户
- 用户登录
- 用户列表
- 修改用户上传权限信息

2. 文件管理
- 上传文件
- 文件列表 (文件类型过滤)
- 文件删除

3. 用户会话
- 会话列表
- 历史对话
- 聊天

#### 非功能性需求

### 技术选型
vue vite vuex vue-router axios element-plus

### 代码结构
src
- api
    - user
    - file
    - thread
    - conversation
- components
    - layout
    - user
    - file
    - thread
    - conversation
- pages
    - home
    - user
    - file
    - thread
    - conversation
- router
    - index
    - user
    - file
    - thread
    - conversation
- store
    - user
    - file
    - thread
    - conversation


## 后端系统设计

### 功能拆分

#### 功能性需求
1. 用户功能
- 用户管理
- 用户登录

2. 上传非结构数据
- 上传文件
- 分析各类型文件 (1. 文本, 2. PDF, Word, PPT, Excel, 2. 图片, 3. 视频, 4. 音频)
- 生成文本向量
- 写入到向量数据库

3. 根据用户的问题回答
- 根据用户提问在向量数据库查询
- 根据组合后的结果提交给 LLM

4. 用户提问上下文管理
- 问题重写(参考: docs/question_rewriteing.md)

#### 非功能性需求
1. 用户
- 密码加密

2. 文件
- 资源使用限制

3. LLM
- 免费LLM

#### 表设计
1. sql

- 用户
```SQL
CREATE TABLE IF NOT EXISTS users (
    id INT,
    username VARCHAR(64),
    password VARCHAR(64),
    role VARCHAR(256),
    created_at DATETIME,
    updated_at DATETIME,
    updated_uid INT
);
```

- 文件
```SQL
CREATE TABLE IF NOT EXISTS files (
    id INT,
    user_id INT,
    name VARCHAR(256),
    hash VARCHAR(32),
    file_path VARCHAR(512),
    created_at DATETIME,
    updated_at DATETIME,
    updated_uid INT
);
```

- 会话
```SQL
CREATE TABLE IF NOT EXISTS thread (
    id INT,
    user_id INT,
    title VARCHAR(128),
    summary VARCHAR(512),
    created_at DATETIME,
    updated_at DATETIME
);
```

```SQL
CREATE TABLE IF NOT EXISTS conversation (
    id INT,
    user_id INT,
    content VARCHAR(512),
    created_at DATETIME,
    updated_at DATETIME
);
```

2. chorma

- 文本集合
```JSON
{
    "id": "文件hash值",
    "embedding": ["生成的文档向量"],
    "metadata": {
        "id": "文件hash值",
        "name": "文件名称",
        "type": "文件类型",  // text, image, pdf, doc, xls, ppt, audio, video
        "content": "",
        "created_at": "创建时间",
    }
}
```

#### 接口设计

1. 用户
- 登录
- 用户列表
- 修改用户上传权限信息

2. 文件管理
- 通过后台程序进行分析
- 对于提取出的文本存入到向量数据库
- 文件列表 (文件类型过滤)
- 文件删除

3. 用户会话
- 会话列表
- 历史对话
- 聊天

4. 异步任务
- 文件分析
    - PDF
    - word
    - PPT
    - Excel
    - 图片
    - 视频
    - 音频
- 文件删除

#### 技术选型

Web 框架: FastAPI
Async task: Celery
ORM: SQLAlchemy
DB: DuckDB
Vector DB: ChormaDB


#### 代码结构 

api: API接口
- user
- file
- thread
- conversation

services: 业务逻辑
- user
- file
- thread
- conversation

utils: 工具
- file
- vector

models: 模型
- user
- file
- thread
- conversation
