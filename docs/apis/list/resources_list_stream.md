# Resources List API

列出指定 Pool 中的资源列表

- `/api/{pool:str}/resources_list/stream`
  - **Method**: `GET`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
  - **Response:**
    - *\*JSONL Resources UUID List* (Stream[str])