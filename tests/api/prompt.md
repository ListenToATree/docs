你是一个资深全栈工程师和技术文档专家。请对当前工作区的 IASNE（前端）和 backend（后端）项目进行一次完整的代码审计与重构文档编制，并生成可执行的 API 回归测试骨架。所有产出物放在工作区根目录下新建的 docs/ 目录中，最终推送到 git@github.com:ListenToATree/docs.git。

---

### 一、项目背景

- 产品名称：IASNE — 船舶能效数据分析智能平台
- 前端路径：IASNE/（Vue 3 + Vite + Element Plus + ECharts + Vuex + Vue Router + vue-i18n）
- 后端路径：backend/（FastAPI + SQLModel + MySQL + Redis + networkx/scipy/xarray/numba/XGBoost）
- 后端服务端口：18000；前端开发端口：8001（Vite 代理 /api 到后端）
- 参考文档：PRD.md（根目录）、backend/PRD.md、IASNE/PRD.md

---

### 二、产出物 1：MkDocs 重构文档站（12 页）

在 docs/ 目录下创建基于 MkDocs + Material for MkDocs 主题的文档站点，语言设为中文（zh），文档源码目录为 site_docs/。

#### 导航结构（nav）：

1. **首页 (index.md)** — 文档目标、核心结论、代码盘点快照、阅读路径
2. **现状分析 (01-current-product-analysis.md)** — 业务功能全貌、技术栈现状、前后端各模块职责、已知技术债
3. **功能保留矩阵 (02-feature-preservation-matrix.md)** — 按模块列出所有现有功能，标注"必须保留/可优化/可下线"，给出重构时的保护策略
4. **现有架构 (03-current-architecture.md)** — 前端目录结构与组件关系、后端分层架构、数据库 ER 关系、中间件链路、外部依赖（OpenMeteo、GEBCO）
5. **重构目标与原则 (04-refactor-goals.md)** — 性能提升目标（P95 延迟、首屏加载）、透明度提升目标（可观测性、契约追踪）、"兼容优先 + 渐进替换"原则
6. **性能重构方案 (05-performance-plan.md)** — 前端：请求层合并/缓存、图表虚拟滚动/懒加载、Bundle 拆分；后端：查询优化、缓存策略升级、航线优化异步化、numba/并行加速
7. **透明度重构方案 (06-transparency-plan.md)** — OpenTelemetry + 结构化日志、统一 Correlation ID（X-ID）透传、Prometheus 指标强化、API 契约 diff 自动化
8. **迁移路线图 (07-migration-roadmap.md)** — Phase 0 基线建立 → Phase 1 兼容层与观测先行 → Phase 2 性能核心改造 → Phase 3 收口与下线；每阶段含产出物和里程碑门禁
9. **验收与回归 (08-acceptance-regression.md)** — 功能回归清单、性能回归指标、验收标准定义
10. **风险与治理 (09-risk-governance.md)** — 技术风险矩阵、组织风险、缓解措施、治理机制
11. **部署说明 (10-deployment.md)** — Docker 部署流程、环境变量清单、CI/CD 流水线说明
12. **接口级追踪矩阵 (11-api-traceability-matrix.md)** — 完整映射：前端 API 函数（apis.js）→ 后端路由端点 → Service/Repository → 数据库表/外部数据源。按域分组（账户/组织、船舶/元数据、上传/统计、优化/提醒、航线优化、计算器），标注已知问题（如 optimazation 拼写兼容、重复函数、缺失后端实现的端点）
13. **接口级回归用例 (12-api-regression-test-cases.md)** — 结构化回归用例清单，含用例 ID、所属接口、请求方法/路径、断言条件、性能阈值

#### 文档生成要求：

- 所有内容必须基于代码实际阅读，不得臆造
- 需要阅读的关键代码文件（不限于）：
  - 前端：IASNE/src/fetch/apis.js、IASNE/src/router/index.js、IASNE/src/store/modules/*.js、IASNE/src/views/**/*.vue、IASNE/package.json、IASNE/vite.config.js
  - 后端：backend/app/main.py、backend/app/modules/*/router.py、backend/app/services/*.py、backend/app/core/*.py、backend/app/models/*.py、backend/app/config.py、backend/app/db.py、backend/pyproject.toml
- 创建 mkdocs.yml 配置文件
- 本地执行 mkdocs build 验证构建通过

---

### 三、产出物 2：GitHub Actions 部署工作流

在 docs/.github/workflows/deploy.yml 创建工作流：
- 触发条件：push to main + workflow_dispatch
- 使用 Python 3.12，安装 mkdocs/mkdocs-material/pymdown-extensions
- 执行 mkdocs build，部署到 GitHub Pages

---

### 四、产出物 3：pytest API 回归测试骨架

在 docs/tests/ 目录下创建可执行的 pytest 测试套件：

#### 目录结构：

```
tests/
├── __init__.py
├── requirements-test.txt        # pytest==8.4.1, requests==2.32.3
└── api/
    ├── __init__.py
    ├── conftest.py              # session 级 fixtures：api_base_url、front_base_url、session、maybe_token
    ├── helpers.py               # assert_ok_response 工具函数
    ├── test_01_smoke_meta.py    # 后端根路径、元数据接口（ship_type、time_zone 等）、/api 前缀兼容
    ├── test_02_org_vessel.py    # 公司列表、船舶列表、用户列表（认证感知）
    ├── test_03_stat_reminder_calc.py  # CII 统计、完整率、提醒值、CII 计算器
    ├── test_04_route_optimization.py  # 航线优化 plan-all（90s 超时）
    └── test_05_front_proxy.py   # 前端 Vite 代理连通（需 RUN_FRONT_PROXY_TESTS=1 开启）
```

#### 配置要求：
- API_BASE_URL 环境变量（默认 http://127.0.0.1:18000）
- FRONT_BASE_URL 环境变量（默认 http://127.0.0.1:5173）
- API_TEST_USERNAME / API_TEST_PASSWORD 可选（控制认证模式）
- API_TEST_VESSEL_ID 可选（默认 1）
- time_zone 等不稳定端点遇非 200 时 skip 而非 fail
- 前端代理测试通过环境变量 RUN_FRONT_PROXY_TESTS 门控

#### 验证要求：
- 本地安装依赖并执行 pytest，确认测试通过（允许在无后端时 skip）

---

### 五、产出物 4：GitHub Actions API 回归测试工作流

在 docs/.github/workflows/api-regression.yml 创建工作流：
- 支持两种模式：
  1. 指向远程测试环境（通过 GitHub Secrets 配置 API_BASE_URL）
  2. 在 runner 中本地启动后端服务再跑测试
- 通过 workflow_dispatch 手动触发，可传入 API_BASE_URL 参数

---

### 六、版本控制与推送

- 在 docs/ 目录添加 .gitignore（排除 __pycache__/、*.pyc、site/、.pytest_cache/）
- git init → git add → git commit → git push 到 git@github.com:ListenToATree/docs.git 的 main 分支
- 确保无 __pycache__ 等临时文件被提交

---

### 注意事项

1. 前端 API 存在 `optimazation`（拼写错误）路径，后端已做兼容处理，文档须标注
2. 后端存在 vesselCii / shipCii 重复函数，须在追踪矩阵中标注
3. 部分能效端点（如 3 个 energy-efficiency 相关接口）前端有调用但后端无实现，须标注
4. 后端中间件含：CORS、X-ID Correlation ID、Prometheus、/api 前缀 strip 兼容层
5. 所有文档内容必须来自代码实际阅读，确保准确性