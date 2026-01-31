# Submit API

向 Mexus 提交 JSON 数据

- `/api/{pool:str}/submit/json`
  - **Method**: `POST`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
    - **json**:
      - `content` (Any): JSON 数据
      - `timeout` (int, float, null): 超时时间
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息
    - `file_uuid` (str): 文件 UUID