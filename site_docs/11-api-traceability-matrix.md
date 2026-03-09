# 接口级功能追踪矩阵

## 目的

这份矩阵用于在重构期间保证“功能不丢、链路可查、问题可定位”。

追踪维度：
- 前端入口（页面/组件）
- 前端 API 函数（`IASNE/src/fetch/apis.js`）
- 后端端点（`backend/app/modules/*/router.py`）
- Service / Repository
- 主要数据源（表/文件/外部服务）
- 兼容状态

## 全局说明

1. 前端统一前缀为 `api/...`，本地联调通过 Vite 代理转发。
2. 后端目前有 `/api` 前缀兼容中间件（`backend/app/core/middleware.py`）。
3. 路径历史兼容重点：前端仍有 `optimazation` 拼写，后端标准化为 `/optimization`。

## A. 账户与组织域

| 前端函数 | 页面入口 | 后端端点 | Router/Service/Repo | 主要数据源 | 状态 |
|---|---|---|---|---|---|
| `register` | `Login/Register` | `POST /user/register` | user router -> `UserService` -> `UserRepository` | `user` | 已对齐 |
| `login` | `Login` | `POST /user/login` | user router -> `UserService` -> `UserRepository` | `user` | 已对齐 |
| `getCompany` | 首页/管理相关 | `GET /company` | company router -> `CompanyService` -> `CompanyRepository` | `company` | 已对齐 |
| `setCompany` | 公司创建 | `POST /company` | 同上 | `company` | 已对齐 |
| `getCompanyInfo` | 公司详情 | `GET /company/{company_id}` | 同上 | `company` | 已对齐 |
| `putCompanyInfo` | 公司编辑 | `PUT /company/{company_id}` | 同上 | `company` | 已对齐 |
| `delCompanyInfo` | 公司删除 | `DELETE /company/{company_id}` | 同上 | `company` | 已对齐 |
| `getCompanyShip` | 公司-船舶列表 | `GET /vessel`（当前前端实现） | vessel router -> `VesselService` -> `VesselRepository` | `vessel` + 统计衍生 | 可用，建议改为 `/company/{id}/vessels` 更语义化 |

## B. 船舶与元数据域

| 前端函数 | 页面入口 | 后端端点 | Router/Service/Repo | 主要数据源 | 状态 |
|---|---|---|---|---|---|
| `getVessel` | 首页船舶列表 | `GET /vessel` | vessel router -> `VesselService` -> `VesselRepository` | `vessel`, `vessel_data_per_day` | 已对齐 |
| `postVessel` | 新增船舶 | `POST /vessel` | 同上 | `vessel`, `equipment*`, `curve*` | 已对齐 |
| `getVesselInfo` | 船舶详情 | `GET /vessel/{vessel_id}` | 同上 | 同上 | 已对齐 |
| `putVesselInfo` | 船舶编辑 | `PUT /vessel/{vessel_id}` | 同上 | 同上 | 已对齐 |
| `delVesselInfo` | 删除船舶 | `DELETE /vessel/{vessel_id}` | 同上 | 同上 | 已对齐 |
| `getFueType` | 新增船舶弹窗 | `GET /meta/fuel_type` | meta router -> `MetaService` -> `MetaRepository` | `fuel_type` | 函数名拼写建议修复为 `getFuelType` |
| `getShipType` | 新增船舶弹窗 | `GET /meta/ship_type` | 同上 | `ship_type` | 已对齐 |
| `getTimeZone` | 新增船舶弹窗 | `GET /meta/time_zone` | 同上 | `time_zone` | 已对齐 |
| `getAttributes` | 数据分析页面 | `GET /meta/attributes` | meta router -> `MetaService` | 代码内静态枚举 | 已对齐（非 DB） |
| `getAttributeMapping` | 多角度页面 | `GET /meta/attribute_mapping` | meta router -> `MetaService` | 代码内静态枚举 | 已对齐（非 DB） |
| `getFuelTypeCategory` | 能耗统计页 | `GET /meta/fuel_type_category` | meta router -> `MetaService` | 代码内静态枚举 | 已对齐（非 DB） |

## C. 上传与统计域

| 前端函数 | 页面入口 | 后端端点 | Router/Service/Repo | 主要数据源 | 状态 |
|---|---|---|---|---|---|
| `uploadData` | 首页上传弹窗 | `POST /upload/vessel/{vessel_id}/standard` | upload router -> `UploadService` -> `UploadRepository` | 文件系统 + `vessel_*` 系列表 | 已对齐 |
| `getUploadHistory` | 上传历史弹窗 | `GET /upload/vessel/{vessel_id}/history` | 同上 | `vessel_data_upload` | 已对齐 |
| `getVesselData` | 首页/优化页面 | `GET /statistic/vessel/{vessel_id}/date-range` | statistic router -> `StatisticService` -> `StatisticRepository` | `vessel_standard_data` | 已对齐 |
| `attributeFrequencies` | 数据分析 | `GET /statistic/attribute-frequencies` | 同上 | `vessel_data_per_day` | 已对齐 |
| `attributeValues` | 数据分析 | `GET /statistic/attribute-values` | 同上 | `vessel_data_per_day` | 已对齐 |
| `attributeRelation` | 能效分析 | `GET /statistic/attribute-relation` | 同上 | `vessel_data_per_day` | 已对齐 |
| `vesselAverage` | 首页卡片 | `GET /statistic/vessel/{id}/average` | 同上 | `vessel_data_per_day` | 与后端端点一致（按 path 参数） |
| `vesselCii` / `shipCii` | 首页/CII | `GET /statistic/vessel/{id}/cii` | 同上 | `vessel_data_per_day` | 存在重复函数，可合并 |
| `vesselCompleteness` | 上传历史热力 | `GET /statistic/vessel/{id}/completeness` | 同上 | `vessel_data_per_day` | 已对齐 |
| `consumptionNmile` | 能耗统计 | `GET /statistic/consumption/nmile` | 同上 | `vessel_data_per_day` + `fuel_type` | 已对齐 |
| `consumptionTotal` | 能耗统计 | `GET /statistic/consumption/total` | 同上 | 同上 | 已对齐 |

## D. 优化与状态提醒域

| 前端函数 | 页面入口 | 后端端点 | Router/Service/Repo | 主要数据源 | 状态 |
|---|---|---|---|---|---|
| `optimizationValues` | 航速优化页 | 期望 `/optimization/optimize-speed/{id}` | optimization router -> `OptimizationService` -> `OptimizationRepository` | `vessel_data_per_day`, `vessel`, `ship_type` | 前端仍写 `optimazation`，依赖兼容层 |
| `optimizeTrim` | 吃水差优化页 | 期望 `/optimization/optimize-trim/{id}` | 同上 | 同上 | 同上 |
| `getTrimData` | 吃水差优化页 | 期望 `/optimization/trim-data/{id}` | 同上 | `vessel_standard_data` | 同上 |
| `optimizationFigure` | 航速优化图表 | `GET /statistic/vessel/{id}/optimization-figure` | statistic router/service | 统计聚合数据 | 需要核对后端是否保留同名端点 |
| `reminderValues` | 状态提醒 | `GET /reminder/{id}/values` | reminder router -> `ReminderService` -> `ReminderRepository` | `vessel`, `vessel_data_per_day` | 已对齐 |
| `reminderFigure` | 状态提醒 | `GET /reminder/{id}/graph` | 同上 | `vessel_standard_data`, `curve_data` | 已对齐 |
| `getEngineStatus` | 发动机状态 | `GET /reminder/{id}/engine` | 同上 | `vessel_standard_data`, `vessel` | 已对齐 |
| `getMonthlyPowerRangesSfoc` | 发动机状态 | `GET /reminder/{id}/monthly-power-ranges-sfoc` | 同上 | `vessel_standard_data` | 已对齐 |

## E. 航线优化域

| 前端函数 | 页面入口 | 后端端点 | Router/Service/Repo | 主要数据源 | 状态 |
|---|---|---|---|---|---|
| `getoptimizeRoute` | 航线推荐 | `POST /route-optimization/ship-route-planner` | route_optimization router -> `RouteOptimizationService` -> `RouteOptimizationRepository` | `vessel_standard_data`, `vessel_historical_voyage`, GEBCO 文件, 气象外部 API | 已对齐 |
| `getShortestRoute` | 航线推荐 | `POST /route-optimization/get-shortest-route` | 同上 | 同上 | 已对齐 |
| `planAllRoutes` | 航线推荐 | `POST /route-optimization/plan-all` | 同上 | 同上 | 已对齐 |
| `getHistoricalRoutes` | 航线推荐 | `POST /route-optimization/historical-routes` | 同上 | `vessel_historical_voyage`, `vessel_standard_data` | 已对齐 |

## F. 计算器域

| 前端函数 | 页面入口 | 后端端点 | Router/Service/Repo | 主要数据源 | 状态 |
|---|---|---|---|---|---|
| `doCIICompute` | CII计算器 | `POST /calculate/cii` | calculate router -> `CalculateService` | 纯计算（无需 DB） | 已对齐 |
| `doEEOICompute` | 预留 | 期望 `/energy-efficiency/eeoi/compute` | 当前代码库未发现对应 router | - | 缺口 |
| `doDISTCompute` | 预留 | 期望 `/energy-efficiency/dist/compute` | 同上 | - | 缺口 |
| `doTIMECompute` | 预留 | 期望 `/energy-efficiency/time/compute` | 同上 | - | 缺口 |

## 重构期必须处理的不一致

1. 路径拼写不一致
- `optimazation` -> `optimization`
- 策略：保留兼容 1-2 个版本周期，并输出 deprecation 头/日志。

2. 重复 API 函数
- `vesselCii` 与 `shipCii` 语义重复。
- 策略：统一函数名并保留别名过渡。

3. 预留接口未落地
- `energy-efficiency/*` 三个端点当前无后端实现。
- 策略：
  - 方案 A：补后端端点并定义契约。
  - 方案 B：前端隐藏入口并在文档标注未上线。

## 建议新增的自动化检查

1. Frontend API -> OpenAPI 对照检查（CI）
2. 兼容接口调用量看板（逐周下降）
3. 接口级回归用例（基于本矩阵分层覆盖）
