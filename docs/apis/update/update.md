# Update API

更新 Mexus 里指定项的 JSON 数据

- `/api/{pool:str}/resources/{resource_id:str}/update`
  - **Method**: `PUT`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
      - `resource_id`: 资源 UUID
    - **json**:
      - `content` (dict[str, Any]): JSON 数据
      - `timeout` (int, float, null): 超时时间
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息