# PKU BikeTracer 云托管服务器程序
[![GitHub license](https://img.shields.io/github/license/WeixinCloud/wxcloudrun-express)](https://github.com/WeixinCloud/wxcloudrun-express)![GitHub package.json dependency version (prod)](https://img.shields.io/badge/python-3.7.3-green)

基于微信云托管 Python Django 框架模版进行开发。本仓库作为整个[系统](https://github.com/UnnamedOrange/laughing-fortnight)的一个组件，维护核心业务逻辑。


## 目录结构说明
~~~
.
├── Dockerfile                  dockerfile
├── README.md                   README.md文件
├── container.config.json       模板部署「服务设置」初始化配置（二次开发，可以忽略）
├── manage.py                   django项目管理文件 与项目进行交互的命令行工具集的入口
├── requirements.txt            依赖包文件
└── wxcloudrun                  app目录
    ├── __init__.py             python项目必带  模块化思想
    ├── apps.py                 自动生成文件apps.py
    ├── asgi.py                 自动生成文件asgi.py, 异步服务网关接口
    ├── migrations              数据移植（迁移）模块
    ├── models.py               数据模块
    ├── settings.py             项目的总配置文件  里面包含数据库 web应用 日志等各种配置
    ├── templates               模版目录,包含主页index.html文件
    ├── urls.py                 URL配置文件  Django项目中所有地址的分发器
    ├── views.py                执行响应的代码所在模块，代码逻辑处理主要地点，项目大部分代码在此编写
    └── wsgi.py                 自动生成文件wsgi.py, Web服务网关接口
~~~

## 服务 API 文档

参考https://app.swaggerhub.com/apis/Honour-Van/EESYS/2.0中给出的API，出于便捷考虑，文档中的responses只包括实际API返回值的data部分，示意如下：

```javascript
JsonResponse = {
	"code": 0,
    "data": responses
}
```


## License

[MIT](./LICENSE)
