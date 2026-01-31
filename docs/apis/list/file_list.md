# File List API

列出指定 Pool 中的文件列表

- `/api/{pool:str}/list`
  - **Method**: `GET`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
  - **Response:**
    - *\*File List* (list[str])