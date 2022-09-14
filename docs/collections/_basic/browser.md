---
title: 网络和浏览器服务
nav_order: 2
---

# 网络和浏览器服务
本章主要简述 Moment 使用的网络和浏览器服务使用到的相关依赖、库。



## 1. 网络服务

Moment 使用异步请求库 `aiohttp` 来解决大部分网络访问需求。由于往往在 `frontend` 就需要从 url 下载图片数据等，`aiohttp` 作为 Moment 的一个基本依赖。



## 2. 浏览器服务

Moment 使用 playwright 的 chromium 无头浏览器作为自己浏览器服务的基础。

提供浏览器服务的基础插件是 `Browser`，也就是说其是一切浏览器相关插件的依赖。playwright 库作为 `Browser` 插件的依赖出现，也就是说它是一种可选依赖（只要不使用 `Browser` 就可以不装）。