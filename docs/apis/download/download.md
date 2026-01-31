# Download API

下载 Mexus 里指定项的 JSON 数据

- `/api/{pool:str}/files/{file_uuid:str}/download/json`
  - **Method**: `GET`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
      - `file_uuid`: 文件 UUID
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息
    - `data` (Any): JSON 数据