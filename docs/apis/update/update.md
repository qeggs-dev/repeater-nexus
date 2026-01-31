# Update API

更新 Mexus 里指定项的 JSON 数据

- `/api/{pool:str}/files/{file_uuid:str}/update/json`
  - **Method**: `PUT`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
      - `file_uuid`: 文件 UUID
    - **json**:
      - `content` (Any): JSON 数据
      - `timeout` (int, float, null): 超时时间
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息