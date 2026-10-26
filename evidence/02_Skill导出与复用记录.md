# Skill 导出与复用记录（telecom-weekly-analysis）

记录编号：EVIDENCE-02｜记录日期：2026-10-26｜范围：本次实际加载并使用的个人 Skill 源文件导出、逐字节校验、真实复用情况、审核发现与限制。

## 一、导出方式与范围

- **源目录**（本机已安装的个人 Skill）：
  `本机已安装的个人 Skill telecom-weekly-analysis（绝对路径已隐去）`
- **导出目标**：本工作空间 `skill/telecom-weekly-analysis/`
- **方式**：整目录文件级复制（`cp -R`），**未改写、未重排、未凭记忆重建**任何内容；复制后仅删除安装元数据文件，其余保持逐字节原样。
- **排除项**：`_meta.json`（安装元数据，内容仅为 `{"category":"data","status":"approved"}`，不含用户信息）。本次导出未包含任何用户身份、账号、路径外的环境信息。
- **校验脚本**：`scripts/verify_skill_export.py`（只读比对源与导出的 SHA256、字节数、文件清单）；保留校验结果、隐去本机路径的发布副本存 `evidence/02_skill_export_sha256.txt`。

## 二、SHA256 校验结果

| 文件 | 字节 | SHA256（源＝导出） | 结果 |
| --- | --- | --- | --- |
| SKILL.md | 8137 | `c8da586705775b7aee0cce21556380687a20b53c1f2f4454d92df1785b2bbd3e` | 一致 |
| evals/evals.json | 129 | `8c01bd8cae7a566009af5a3a1afd8ac8b46efefbbc44db42ce43e98fef7c7483` | 一致 |
| references/eval-cases.yaml | 227 | `dd7e5ef72bd63ae3cd2aed184b8202a713f2341c115f04a9e1aa94a1ec5c7451` | 一致 |
| references/governance-boundaries.md | 571 | `b5156ece38fe404a51e0e0dac427a691ce8e4d9e260c6600459f36dd1360eb7b` | 一致 |
| references/input-contract.md | 829 | `a8d8b2b241bc3c056b33a69a19317f8d38187a05f7a75ccd1f0eb0e463179271` | 一致 |
| references/kstar-evolution.md | 585 | `4c9e73e8d3e80186b0eb1c51dad9fc1af94a36dea295c9aed37183b188504acd` | 一致 |
| references/ontology-mapping.md | 308 | `688b876c00f19849349b7ea1ed65df025968c5db4a1b9fe7e6d00fce07e17b51` | 一致 |
| references/output-contract.md | 419 | `74ab2d215baa37aa8bd63757eae1110ad67723c49680075adb360adcfbf968dd` | 一致 |
| references/skill-spec.yaml | 624 | `4d5a3e2eb40a0c2866f1d8f48a27afcfc87c0677282a25a51aecfa660d2a96fa` | 一致 |
| references/validation-contract.md | 560 | `abe420ae2ecdebf988ae0c854971a62fea1a3e37339da2592baf170d28e8e7e8` | 一致 |

- 源文件数（排除 `_meta.json`）：10；导出文件数：10；缺失：无；多余：无。
- **整体结论：10 个文件全部逐字节一致**，可复算（`python3 scripts/verify_skill_export.py <本机已安装Skill目录>`）。

## 三、真实复用情况

| 项 | 记录 |
| --- | --- |
| 复用场景 | 第二周经营分析（`samples/week-b.json` ＋ `materials/业务说明与办理规范.md`） |
| 产物 | `outputs/03_第二周经营分析.md`（首版，保留不动）、`outputs/04_第二周经营分析_核验简版.md`（审核修正版） |
| 调用方式 | 会话内加载 SKILL.md 并按其中步骤、校验清单与输出模板执行；**非程序化/脚本化执行**（Skill 本身不依赖脚本） |
| 复用性质 | 一次跨周复用（第一周为 `week-a.json` 的 `outputs/01`/`02`，第二周换数据、换周次重跑同一方法） |
| 未读取 | 第一周成品报告未作为第二周的输入依据（首版 03 编写时的约束） |

按 SKILL.md 要求实际执行到的部分：两周漏斗字段与分母定义、非负整数与逐级倒挂校验、零分母检查、绝对差（百分点）与相对变化分开表述、事实与原因假设分离、建议不超过 3 项并写明角色/时限/验证方式/未落地条件、不做客户触达与人员调度、不编造资费。

## 四、本轮审核发现（含对 Skill 使用的修正）

1. **表述不准确**：首版 03 写成"其后两级比例的升降都以触达率（有效沟通）为分母基础"。事实是预约率分母＝有效沟通，办理率分母＝预约，只有预约率以触达结果为分母。已在 04 更正。
2. **字段数量错误**：首版 03 把费用解释卡字段写成"六项"。BIZ-RULES-01 实际为 **5 组**：月费、一次性费用、优惠生效条件与期限、到期变化、退订/变更条件。已在 04 更正。
3. **跨周跟进边界缺失**：首版 03 的补触达建议未要求单建原队列台账，也未区分验收队列，存在把旧队列补触达混入次周新线索同周漏斗、用次周触达率误评旧队列的风险。已在 04 明确：单建原队列跟进台账、不入任何一周同周漏斗、不用次周新线索触达率验收，并逐条标明验收队列。
4. **Skill 自身待完善（作者未填的实例化内容）**：`references/` 下 `input-contract.md`、`validation-contract.md`、`output-contract.md`、`ontology-mapping.md`、`eval-cases.yaml` 仍为通用模板占位（如 `<field_a>`、`<input A>`、`<Entity>`），未实例化为电信经营场景；`evals/evals.json` 的 `cases` 为空数组，仅有作者备注。**结论：复用依赖的是 SKILL.md 的正文流程，不依赖这些占位文件**；这些文件本次按原样导出，未修改。

## 五、限制与不宣称事项

- **未通过教师评价**：本 Skill 及其产物未提交任何教师评审、课程评分或 EduSeed 平台评审流程，本记录不构成"已通过教师评价"。
- **不宣称全场景验证**：实际验证仅覆盖教学样例的单一数据形状（4 字段同周漏斗、单网格、社区宽带）；多产品/多网格/分渠道明细、含跨周生命周期口径、真实资费金额等场景**未验证**。
- **无用例回归**：`evals/evals.json` 无实际用例，本次未新增或执行正/负例回归，未做边界（如零线索、倒挂、缺字段）自动化测试。
- **发布级别**：Skill 自带治理声明为 `promotion_ceiling: staged`、`production_release_allowed: false`。本记录只主张"已加载、已按流程使用、产物已人工审核修正"，**不主张可生产上线或已获准发布**。
- **样本量**：跨周复用仅 1 次（week-b），单样本，不足以说明方法在其他周次或团队稳定有效。
- **数据性质**：`week-a.json`、`week-b.json` 均为人工编写的教学样例，非真实客户经营数据；结论不适用于任何真实网格。
