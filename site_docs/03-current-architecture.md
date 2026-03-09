# 现有架构

## 一、前端架构（IASNE）

### 1. 分层

1. 展示层：`src/views/**`
2. 组件层：`src/components/**`
3. 网络层：`src/fetch/http.js`、`src/fetch/index.js`、`src/fetch/apis.js`
4. 状态层：`src/store/index.js`
5. 路由层：`src/router/index.js`

### 2. 关键特征

- Hash 路由
- Vuex 持久化到 sessionStorage
- 图表逻辑集中在页面组件和 `utils/tools.js`
- 请求封装存在业务逻辑与错误处理耦合

## 二、后端架构（backend）

### 1. 入口与生命周期

- 入口：`backend/app/main.py`
- 生命周期中做：
  - SQLModel `create_all`
  - Redis 缓存初始化（不可用时降级内存缓存）
  - 航线图后台预热线程

### 2. 模块化组织

- `modules/<domain>/router.py`
- `modules/<domain>/service.py`
- `modules/<domain>/repository.py`

当前主模块：
- meta/company/user/vessel/upload/statistic/optimization/reminder/calculate/route_optimization

### 3. 中间件与横切能力

- CORS
- Correlation ID (`X-ID`)
- Prometheus 指标
- `/api` 前缀兼容中间件

## 三、架构问题总结

1. 前后端契约管理未产品化
- 路径兼容、字段演进主要靠代码层“临时兜底”。

2. 可观测链路不完整
- 已有 metrics 与 request id，但缺日志结构化规范、关键业务事件埋点、SLO 看板。

3. 性能治理机制未体系化
- 缓存、并发、预热都在做，但缺容量评估、基线、压测门禁和自动回归。
