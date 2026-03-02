# Main Config

用于指导 Nexus 启动与运行的一组配置项
格式为 JSON

``` json
{
    // 服务器配置
    "server": {

        // 服务器运行 IP
        "host": "127.0.0.1",

        // 运行端口
        "port": 8080,

        // 是否在发现文件变动时自动重启服务
        "reload": false,

        // 多进程模式运行指定进程数量
        "workers": null
    },

    // 日志配置
    "logger": {

        // 日志文件路径
        "file_path": "./logs/repeater-nexus-log-{time:YYYY-MM-DD_HH-mm-ss.SSS}.log",

        // 日志等级
        "level": "INFO",

        // 日志轮转间隔
        "rotation": "1 days",

        // 日志保留时长
        "retention": "7 days",

        // 控制台日志格式
        "console_format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> - <level>{message}</level>",

        // 文件日志格式
        "file_format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} - {message}",

        // 日志文件压缩格式
        // 可选项：
        // - gz
        // - bz2
        // - xz
        // - lzma
        // - tar
        // - tar.gz
        // - tar.bz2
        // - tar.xz
        // - zip
        "compression": "zip"
    },

    // 存储配置
    "storage": {

        // 存储路径
        "storage_path": "./workspace/storage",

        // 存储文件后缀
        "file_suffix": ".json",
        
        // Pool 白名单
        // 为空则不允许任何 Pool 访问
        "pool_whitelist": []
    }
}
```