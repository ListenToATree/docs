# 接口级回归用例清单

## 使用方式

1. 以《11-api-traceability-matrix》为主索引。
2. 按模块逐条执行本清单。
3. 每个用例记录：请求、响应、耗时、结果（Pass/Fail）、备注。

建议统一记录字段：
- `case_id`
- `env`
- `request`
- `response_status`
- `response_body_hash`
- `latency_ms`
- `result`
- `owner`
- `run_at`

## A. 账户与组织

### A-1 注册
- `case_id`: `USER-REGISTER-001`
- 接口: `POST /user/register`
- 关键断言:
  - HTTP 200
  - `code == 200`
  - 返回字段包含 `id/username/company_id`
  - 不返回明文密码

### A-2 登录
- `case_id`: `USER-LOGIN-001`
- 接口: `POST /user/login`
- 关键断言:
  - HTTP 200
  - `code == 200`
  - 返回 `token`

### A-3 公司 CRUD
- `case_id`: `COMPANY-CRUD-001..004`
- 接口: `GET/POST/PUT/DELETE /company`
- 关键断言:
  - 全链路可执行
  - 删除后查询不到

## B. 船舶与元数据

### B-1 船舶列表
- `case_id`: `VESSEL-LIST-001`
- 接口: `GET /vessel`
- 关键断言:
  - HTTP 200
  - 返回列表项包含 `latest_cii/cii_rating`

### B-2 船舶详情
- `case_id`: `VESSEL-DETAIL-001`
- 接口: `GET /vessel/{id}`
- 关键断言:
  - HTTP 200
  - 详情字段完整

### B-3 元数据
- `case_id`: `META-001..006`
- 接口:
  - `GET /meta/fuel_type`
  - `GET /meta/ship_type`
  - `GET /meta/time_zone`
  - `GET /meta/attributes`
  - `GET /meta/attribute_mapping`
  - `GET /meta/fuel_type_category`
- 关键断言:
  - 列表非空（业务环境）
  - 字段类型稳定

## C. 上传与统计

### C-1 上传标准数据
- `case_id`: `UPLOAD-STD-001`
- 接口: `POST /upload/vessel/{id}/standard`
- 输入: 合法 CSV 样例
- 关键断言:
  - HTTP 200
  - 上传历史可见
  - 统计与 CII 相关数据可查

### C-2 上传历史
- `case_id`: `UPLOAD-HISTORY-001`
- 接口: `GET /upload/vessel/{id}/history`
- 关键断言:
  - 返回分页结构可用

### C-3 统计接口
- `case_id`: `STAT-001..009`
- 接口:
  - `GET /statistic/attribute-frequencies`
  - `GET /statistic/attribute-values`
  - `GET /statistic/attribute-relation`
  - `GET /statistic/vessel/{id}/cii`
  - `GET /statistic/vessel/{id}/completeness`
  - `GET /statistic/vessel/{id}/date-range`
  - `GET /statistic/consumption/nmile`
  - `GET /statistic/consumption/total`
- 关键断言:
  - 时间筛选有效
  - 字段口径稳定
  - 数据为空时返回结构不变

## D. 优化与提醒

### D-1 航速优化
- `case_id`: `OPT-SPEED-001`
- 接口: `GET /optimization/optimize-speed/{id}`
- 关键断言:
  - 返回包含 baseline 行（`delta == 0`）
  - 返回 CII 和评级字段

### D-2 吃水差优化
- `case_id`: `OPT-TRIM-001`
- 接口:
  - `GET /optimization/optimize-trim/{id}`
  - `GET /optimization/trim-data/{id}`
- 关键断言:
  - 优化建议与图表数据均可用

### D-3 状态提醒
- `case_id`: `REMINDER-001..004`
- 接口:
  - `GET /reminder/{id}/values`
  - `GET /reminder/{id}/graph`
  - `GET /reminder/{id}/engine`
  - `GET /reminder/{id}/monthly-power-ranges-sfoc`
- 关键断言:
  - 返回结构可被前端直接消费

## E. 航线优化

### E-1 最短路径
- `case_id`: `ROUTE-SHORTEST-001`
- 接口: `POST /route-optimization/get-shortest-route`
- 关键断言:
  - 返回 route、statistics、segments
  - 路径首尾点与请求一致

### E-2 油耗优化路径
- `case_id`: `ROUTE-FUEL-001`
- 接口: `POST /route-optimization/ship-route-planner`
- 关键断言:
  - 返回 `fuel_optimal` 路径
  - 统计字段完整（距离、油耗、时间）

### E-3 全量规划与历史
- `case_id`: `ROUTE-PLANALL-001`, `ROUTE-HISTORY-001`
- 接口:
  - `POST /route-optimization/plan-all`
  - `POST /route-optimization/historical-routes`
- 关键断言:
  - 历史航次可回放
  - 输出结构与前端契合

## F. 计算器与预留接口

### F-1 CII 计算器
- `case_id`: `CALC-CII-001`
- 接口: `POST /calculate/cii`
- 关键断言:
  - 不依赖数据库也可计算
  - 输出评级稳定

### F-2 预留接口（缺口追踪）
- `case_id`: `GAP-ENERGY-EFF-001..003`
- 接口:
  - `/energy-efficiency/eeoi/compute`
  - `/energy-efficiency/dist/compute`
  - `/energy-efficiency/time/compute`
- 当前状态: 后端未实现
- 验收策略:
  - 未实现阶段：前端隐藏入口或返回明确提示
  - 实现后：补齐完整回归用例

## 兼容性专项

### X-1 `/api` 前缀兼容
- `case_id`: `COMPAT-API-PREFIX-001`
- 断言:
  - `GET /api/meta/ship_type` 与 `GET /meta/ship_type` 均可用

### X-2 历史 typo 路径兼容
- `case_id`: `COMPAT-OPTIMAZATION-001`
- 断言:
  - 前端旧路径在兼容窗口可用
  - 响应包含 deprecation 标识（建议）

## 性能回归门槛（建议）

1. 普通查询接口：P95 < 300ms
2. 统计接口：P95 < 800ms
3. 航线优化同步接口：P95 < 5s（过渡期）
4. 上传处理：给出处理时长分布和失败原因 TOP

## 自动化落地建议

1. 在 CI 增加 `contract-test` 作业
2. 按本清单生成 Postman/Newman 或 pytest API 套件
3. 每次发布自动输出“通过率 + 变化接口列表”
