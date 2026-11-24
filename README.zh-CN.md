# diagram-driven-coding

[English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

一个给 AI 写代码用的 skill：每个组件文件夹内都有自己的 `ARCHITECTURE.md`（class／sequence diagram、职责、数据契约）先行，配合 TDD 与 interface 分层，把 AI 改代码的影响范围收窄。

> 注意：`SKILL.md` 与 demo 文档以英文撰写；README 提供三种语言。

## 解决什么问题

> 想先看成品：[demo/ARCHITECTURE.md](demo/ARCHITECTURE.md) 是 root 组件地图，顺着链接可以看到组件与子组件的文档。

让 AI 改一个功能，它顺手改了三个不相关的文件；改 A 坏 B；出错之后还得逐行 debug，省不了时间。

这个 skill 不是叫 AI“更小心”，而是让它没有机会乱改：

- **边界清楚**：每个组件一个文件夹，只通过 interface 对外，private helper 外部不得碰。
- **先改图、再写 test、后实现**：图是 AI 与人都看得懂的导航图，也是 review 的重点。
- **测对外承诺，不测内部结构**：避免 AI 用大量结构测试制造虚假的 coverage 安全感。
- **改 interface 要经人批准**：AI 会先评估有没有“与当前工作无关”的其他使用者，再主动询问你是否批准。
- **坏了可以整个 class 换掉**：多个实现共用同一套行为 contract test。

更多做法见最后的“核心原则详解”。

## 内容

| 路径 | 内容 |
| --- | --- |
| `SKILL.md` | skill 本体，单一文件（核心做法、进阶选项、ARCHITECTURE.md 模板） |
| `demo/` | 一个小型 Python 示范项目（root、组件、子组件各有 `ARCHITECTURE.md`），三个场景演示 skill 如何运作，详见 `demo/DEMO.md`。想快速看成品：[demo/ARCHITECTURE.md](demo/ARCHITECTURE.md)（root 组件地图）→ [demo/pricing/ARCHITECTURE.md](demo/pricing/ARCHITECTURE.md)（组件）→ [demo/pricing/rules/ARCHITECTURE.md](demo/pricing/rules/ARCHITECTURE.md)（子组件） |

## 使用方式

- **Claude Code**：将 `SKILL.md` 放入 `.claude/skills/diagram-driven-coding/SKILL.md`。
- **ChatGPT／Codex**：
  - ChatGPT：若账号有 Skills 功能，到 Plugins → Skills → Create → Upload from your computer 上传；没有的话，将 `SKILL.md` 粘贴到 Project 的 instructions，或以文件上传。
  - Codex：放入项目的 `.agents/skills/diagram-driven-coding/SKILL.md`（想在所有项目使用，放在 `~/.agents/skills/`），输入 `$diagram-driven-coding` 即可明确调用。不需要另外写 `AGENTS.md`。
- **其他 AI 工具**：放入该工具的 skills 目录，或将内容并入项目的指引文件（例如 `.cursorrules`）。

适用于中型以上、AI 会长期参与维护的项目。小脚本或一次性项目不需使用。

## 状态

核心做法来自多个真实项目的长期使用经验；“进阶”部分（自动强制检查、commit hash、分级批准等）尚未验证，请当作建议。

## 试跑 demo 的测试

```bash
cd demo
python3 -m unittest discover -v
```

只需 Python 3.9 以上，没有外部依赖。

## 运行类型检查（可选）

Interface 签名的兼容性由类型检查器强制（见 skill 的“签名兼容”原则）。Demo 已附配置文件：

```bash
pip install mypy pyright
cd demo
mypy       # 读取 mypy.ini（strict）
pyright    # 读取 pyrightconfig.json（standard）
```

两者都应该是 0 error。

## 核心原则详解

### 文档分层

- **root `ARCHITECTURE.md`**：只画组件地图（谁依赖谁）与跨组件的主要流程，不写实现细节。
- **组件 `ARCHITECTURE.md`**：每个组件一份，写职责、class／sequence diagram、数据契约与“不负责什么”。
- **子组件**：只有符合开 interface 条件（跨文件夹使用、有多个可替换实现、接外部系统）才拆出来，同样有自己的 `ARCHITECTURE.md`；在父层的图中只当作一个 participant。层数控制在 2–3 层。
- 示例：[root](demo/ARCHITECTURE.md)、[组件](demo/pricing/ARCHITECTURE.md)、[子组件](demo/pricing/rules/ARCHITECTURE.md)。

### 数据形状要写明

- 返回值若是固定 key 的结构，用 `TypedDict`，放在组件的 `data_types.py`，并由 `__init__.py` 导出。不用裸 `dict`（看不出里面有什么），也不为了包装而硬做 class（多了隐藏逻辑，使用麻烦）。
- 值只能是几个固定字符串时，用 `Literal`（例如 `CustomerTier`）。
- DataFrame 的 column 与 dtype 也是数据契约：column 清单只定义一次，文档与校验共用；在组件边界校验输入与输出（可考虑 `pandera`）。
- 每个公开函数、class 都要有 Google style docstring（`Args:`、`Returns:`、`Raises:`、`Not responsible for:` 等）。

### 签名兼容交给类型检查器

- 原则：实现的签名与 interface 兼容：参数名称、顺序、kind 一致；类型按类型检查器的规则（参数可放宽、return 可收窄）。
- 注意工具保证的是“兼容”，不是“文字上完全相同”。
- 不靠 AI 自觉，靠工具把关：Python 用 pyright 或 mypy，TypeScript 用 `tsc --strict`，Java／C# 由 compiler 负责。
- Demo 附有 `demo/mypy.ini` 与 `demo/pyrightconfig.json`，见上面“运行类型检查”。

### 要做 DIP，但别让 interface 变乱（YAGNI）

- 实现 class 的 constructor 可以接收 interface 类型的依赖，但这些参数只是组件内部的事。
- 组装放在组件 `__init__.py` 的工厂函数（例如 `default_pricer()`）；对外只导出 interface、`TypedDict` 与工厂函数；实现 class 不放入 `__all__`，约定其他文件夹只使用工厂函数与 interface。Python 不会强制，要强制就用依赖检查。
- 没有 interface 的内部小 class（校验、小计等）由实现自己创建，不需注入。
- AI 若为了“将来可能替换”而新增公开参数或导出实现 class，必须说明是哪个具体需求；答不出来就不加。
- Demo 对应：`demo/pricing/__init__.py` 与 `demo/pricing/standard_pricer.py`。

### 测试规则

- 测对外承诺（行为），不锁死内部结构。检查标准：这个 test 失败时，下游会不会真的坏？下游依赖的 import 路径、关键字参数名称也算契约，可以测。
- 多个实现共用同一套 contract test，所以整个 class 换掉时，行为保证仍在。

### 改 interface 要经人批准

- 默认所有 interface 改动都要批准。
- AI 会先评估有没有“与当前工作无关”的其他使用者（其他文件夹有没有引用），向你说明影响范围，再主动询问是否批准。

### 接手旧项目

- 非 OOP 项目不要一次重写：先在现有代码加一层薄薄的 caller（最少改动），并先写 characterization test 锁住现有行为。
- 再在新文件夹用 OOP 写核心逻辑，与旧逻辑并行（shadow run）比对结果，满意再切换，并保留回退。
- 核心逻辑很大时，逐件搬，root 图用 `<<legacy>>` participant 表示尚未搬的部分。

### 诚实汇报

- AI 汇报时要分清楚：`PASSED`、`FAILED`、`NOT RUN`、`BLOCKED`，不可将没跑过的 test 说成通过。

### 进阶（可选，尚未验证）

自动强制检查、commit hash、test plan／notebook、分级批准，详见 `SKILL.md` 的“进阶”部分。

## 许可证

MIT，见 [LICENSE](LICENSE)。
