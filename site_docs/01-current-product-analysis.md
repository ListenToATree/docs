# 现状分析

## 一、产品能力现状

基于前端路由 `IASNE/src/router/index.js` 与 API 调用 `IASNE/src/fetch/apis.js`，当前产品模块如下：

1. 账户与组织
- 登录/注册
- 用户管理
- 公司管理
- 船舶管理

2. 数据接入与质量
- 船舶标准数据上传（CSV）
- 上传历史
- 数据完整度展示

3. 分析与统计
- 属性频次分布
- 属性时序
- 属性关系
- 油耗统计（总油耗、每海里）
- CII 历史与评级

4. 优化与建议
- 航速优化
- 吃水差优化
- 船体及螺旋桨状态提醒
- 发动机状态

5. 航线优化
- 最短路径
- 油耗优化路径
- 一次性规划（plan-all）
- 历史航迹查询

6. 独立计算器
- CII 计算器（无需依赖历史数据库数据）

## 二、技术实现现状

### 前端（IASNE）

- 技术栈：Vue 3 + Vuex + Vue Router + Element Plus + ECharts + Vite
- 网络层：`src/fetch/http.js` + `src/fetch/index.js` 封装
- 状态：Vuex + sessionStorage 持久化
- 特点：页面与图表逻辑较重，接口调用集中在 `src/fetch/apis.js`

主要技术债：

1. 错误处理与状态流不统一
- `httpService` 中大量 Promise 手工封装，错误分支使用 `resolve(null/err)`，容易导致调用方判定分叉复杂。

2. 接口命名历史兼容包袱
- 前端仍存在 `optimazation` 历史路径调用；后端已规范为 `optimization`，依赖兼容层维持运行。

3. 渲染性能隐患
- 大量页面默认拉取后直接图表渲染；缺少分层缓存、虚拟化、按需加载与流式骨架策略。

### 后端（backend）

- 技术栈：FastAPI + SQLModel + PyMySQL + Redis + networkx/scipy/xarray/numba 等
- 架构：模块化 `router/service/repository`，入口在 `app/main.py`
- 可观测基础：Prometheus 中间件 + X-ID 请求相关性

主要技术债：

1. 接口层与数据库连接鲁棒性不足
- 从历史运行现象看，DB 连接中断会直接放大为 500，重试、熔断与降级策略不完整。

2. 重型算法与请求通道耦合
- 航线优化图构建和天气数据拉取较重，虽有缓存，但可预测性和可观测性仍需增强。

3. 兼容逻辑散落
- 例如 `/api` 前缀兼容中间件、旧路径兼容等，缺少统一“契约版本策略”。

## 三、结论

系统已具备可用业务闭环，但要进入“稳定可扩展阶段”，需要从“可跑”转向“可测、可观测、可解释、可演进”。
