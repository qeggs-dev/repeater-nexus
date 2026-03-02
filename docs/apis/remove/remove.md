# Remove API

移除 Mexus 里的指定项

- `/api/{pool:str}/resources/{resource_id:str}/remove/resource`
  - **Method**: `DELETE`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
      - `resource_id`: 资源 UUID
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息