# Data List API

列出指定 Pool 中的指定资源的数据列表

- `/api/{pool:str}/resources/{resource_id:str}/datas`
  - **Method**: `GET`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
      - `resource_id`: 资源 ID
  - **Response:**
    - *\*Data Name List* (list[str])