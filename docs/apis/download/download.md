# Download API

下载 Mexus 里指定项的 JSON 数据

- `/api/{pool:str}/resources/{resources_id:str}/download/{data_id:str}`
  - **Method**: `GET`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
      - `resources_id`: 资源 UUID
      - `data_id`: 数据 ID
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息
    - `data` (Any): JSON 数据