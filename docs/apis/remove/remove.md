# Remove API

移除 Mexus 里的指定项

- `/api/{pool:str}/files/{file_uuid:str}/remove`
  - **Method**: `DELETE`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
      - `file_uuid`: 文件 UUID
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息