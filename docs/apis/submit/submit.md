# Submit API

向 Mexus 提交 JSON 数据

- `/api/{pool:str}/submit`
  - **Method**: `POST`
  - **Request:**
    - **path_params**:
      - `pool`: mexus 池名称
    - **json**:
      - `content` (dict[str, Any]): 提交内容
      - `timeout` (int, float, null): 超时时间
  - **Response:**
    - `status` (str): 状态
    - `message` (str): 状态信息
    - `file_uuid` (str): 文件 UUID

提交数据的格式参考：[提交内容](./../submit_content.md)