# Book System

本项目是一个本地书籍知识库和学习记录 CLI，供人或 AI 自动读取书籍、记录阅读、安排 FSRS 复习。

## 项目框架

```text
AI Skills
  |
  +--> book-user    --> books list/show/chapter --> Catalog
  |                                                   |
  |                                                   v
  |                                          .booksys/content/books
  |
  +--> book-coach   --> learn status/complete --+
  |                                             |
  +--> book-trainer --> learn status/due/review-+--> Learning Service
                                                  |            |
                                                  v            v
                                             Validation      FSRS
                                                  |
                                                  v
                                   .booksys/runtime/learning/events.jsonl

  +--> book-reader  --> packages import --> Validate --> Immutable Catalog
```

Catalog 是书籍内容的权威来源；`events.jsonl` 是学习历史的权威来源；阅读状态、掌握度和到期任务按需从事件流重建，不单独保存派生状态文件。

## 给 AI 的安装流程

在项目根目录执行：

```powershell
python -m pip install .
booksys --version
booksys doctor
```

要求 Python 3.11+；`pyproject.toml` 会安装固定依赖 `fsrs==6.3.2`。

如果只想从源码运行：

```powershell
.\booksys.bat doctor
```

`doctor` 是只读检查。如果提示 catalog 缺失，表示当前项目还没有导入书籍，不是安装失败。

## 最短使用路径

```powershell
booksys books list
booksys books show <book-id>
booksys books chapter <book-id> <chapter-id>
booksys learn status
booksys learn due
```

AI 应按这个顺序工作：

1. `books list` 获取稳定的 `book_id` 和 `chapter_id`。
2. `books show` 读取书籍声明和章节地图。
3. `books chapter` 获取该章的 `source.md`、`guide.md`、`concepts.json` 路径。
4. 读取这些文件后再回答问题，并区分书中材料、外部事实和推断。

运行时只接受稳定 ID，不按标题、别名或语义猜测对象。不要手写或猜测 ID，始终先读取 `book.json`。

## 记录学习

以下命令会追加事件：

```powershell
booksys learn complete <book-id> <chapter-id>
booksys learn review <concept-id> '<json-payload>'
```

复习 payload 必须包含：`question_kind`、`target_level`（1–5）、`emt_expectations`、`misconceptions`、`emt_hits`、`emt_score`（0–1）、`objective_pass`（布尔值）、`confidence`（0–1）和 `user_rating`（`hard`/`good`/`easy`）。客观失败时最终调度评级为 `again`。

网络重试同一个请求时复用幂等键；有意重读或重新测验时使用新键或省略键：

```powershell
booksys learn complete <book-id> <chapter-id> --idempotency-key <retry-key>
```

## 导入书籍

知识包至少包含：

```text
my-book/
  book.json
  book.md
  chapters/
    01-intro/
      source.md
      guide.md
      concepts.json
```

导入并校验：

```powershell
booksys packages import D:\prepared-books\my-book
booksys doctor
```

导入会严格校验并发布到 `.booksys/content/books`。已发布包不可覆盖；修订内容时准备新的包。制作清单见 [book-reader 技能](skills/book-reader/SKILL.md)。

## 数据位置和配置

默认位置：

```text
.booksys/content/books/                 # 已发布知识包
.booksys/runtime/learning/events.jsonl  # 只追加的阅读/复习事件
```

指定外部书库或学习数据：

```powershell
booksys --system-root D:\book-library --data-root D:\private-learning learn status
```

也可以在 `.booksys/config.json` 中设置 `system_root` 和 `data_root`；命令行参数优先。

## 安全边界

- 只读：`books list`、`books show`、`books chapter`、`learn status`、`learn due`、`doctor`。
- 写入：`learn complete`、`learn review` 只追加事件；`packages import` 发布不可覆盖的包。
- 不要手动编辑或删除 `events.jsonl`。发现异常时先运行 `booksys doctor`。
- `learn status` 和 `learn due` 遇到不合规历史会报错，不会返回部分状态。

## 验证和 AI 技能

```powershell
booksys doctor
python -m unittest discover -s tests -v
```

- [book-user](skills/book-user/SKILL.md)：基于书籍框架回答问题。
- [book-coach](skills/book-coach/SKILL.md)：陪读并记录章节完成。
- [book-trainer](skills/book-trainer/SKILL.md)：出题、评估并记录复习。
- [book-reader](skills/book-reader/SKILL.md)：制作并发布知识包。

更多运行时约束见 [RUNTIME.md](RUNTIME.md)，正式规格见 `openspec/specs/`。
