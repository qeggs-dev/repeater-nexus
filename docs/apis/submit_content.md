# Submit Content

提交内容格式为：

`dict[str, Any]`

```json
{
  "title": "Example",
  "url": "https://example.com",
  "description": "This is an example.",
  "dict_data": {
    "key": "value"
  },
  "list_data": [
    "value1",
    "value2"
  ]
}
```

其中键是分区名称
按照你的需求对数据进行分区
从而在加载某些数据时不需要载入额外不需要的内容

比如上面的那段请求就会变成:

- `*pool`
  - `*resources_id`
    - `b64_dGl0bGU=.json`
    - `b64_dXJs.json`
    - `b64_ZGVzY3JpcHRpb24=.json`
    - `b64_ZGljdF9kYXRh.json`
    - `b64_bGlzdF9kYXRh.json`

这样的目录结构