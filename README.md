# Skill Q版人物拓展图

一个 Claude / Codex Skill：把**一张动画角色图片**或**一张真人照片**，转换成一整套保留角色一致性的 **Q 版人物「动作 × 表情」透明背景 PNG 分镜库**，适合用来做贴图、表情包、素材库等。

- 🎨 **动画图片输入**：抠出主角，保留原本造型、配色、比例，只生成不同动作与表情。
- 📷 **真人照片输入**：先抠出人物并制作成 Q 版角色（保留脸型、发型、肤色等特征），再生成不同动作与表情。
- 🖼️ **所有正式成果**必须是**透明背景 PNG**，不可带白底、黑底、场景或地板。
- 🔞 **内建未成年人保护机制**：未成年人、看起来年幼的角色、年龄无法确认的人物，一律禁止性感化、暴露化、暗示性姿势等成人向表现。

## 仓库结构

```text
.
├─ Skill/character-storyboard-generator/   # Skill 本体（供 Claude / Codex 使用）
│  ├─ SKILL.md                             # Skill 说明与工作流程
│  ├─ references/                          # 动作表、表情表、命名规则、Prompt/QA 规则
│  ├─ assets/project-template.json         # 项目配置模板
│  ├─ scripts/                             # build_manifest.py / audit_outputs.py
│  └─ agents/openai.yaml                   # 代理入口配置
├─ Sample/                                 # 教学与范例成果
│  ├─ 教学.md
│  ├─ 原图.png                              # 范例真人原图
│  └─ 成果/                                 # 依「情绪-表情」分类的范例 PNG
├─ happy.png                                # 范例原图（与 Sample/原图.png 相同）
└─ 待办事项.md                              # 尚未完成的工作清单
```

## 使用方法

1. 准备一张人物清楚、遮挡较少的图片。
2. 告诉 Claude / Codex：`使用 $character-storyboard-generator，把这张图制作成透明背景的动作表情分镜。`
3. Skill 会先判断输入是动画还是真人照片。
4. 先制作少量校准图，确认人物脸型、发型、服装、颜色和 Q 版比例一致。
5. 再生成动作 × 表情组合，并依照情绪归类。
6. 最后检查透明背景、人物完整度、命名和资料夹位置。

## 未成年人保护

未成年人、看起来年幼的角色，以及年龄无法确认的人物，一律启用未成年人保护：

- 禁止性感、诱惑、恋爱成人化或恋物化表现。
- 禁止暴露服装、身体部位强化、挑逗视角与暗示性姿势。
- "迷人"只能解释为亲切、自信或闪亮可爱；"性感"组合直接停用。
- 趴着、躺着、哭泣等动作只能表现为日常、休息或搞笑情境。

## 固定命名

```text
角色__动作ID-动作__表情ID-表情__版本序号__v1.0.png
```

例如：

```text
xiaomai__P06-wave-goodbye__E01-joy__v01__v1.0.png
```

## 透明背景要求

正式成果必须同时符合：

- PNG 文件含 Alpha 透明通道。
- 图片四角为透明像素。
- 人物边缘没有绿色、白色或黑色残边。
- 没有背景、地板、阴影、文字、水印或对话框。
- 头发、手、脚和贴地动作不可被裁切。

> 某些看图软件会用黑色、白色或棋盘格显示透明区域；这只是预览方式，不代表图片真的有背景。

## 范例原图

<img src="Sample/原图.png" alt="范例原图" width="240" />

## 范例成果预览

| 分类 | 预览 | 文件 |
| --- | --- | --- |
| 喜－开心 · 自然站立 | <img src="Sample/成果/喜-开心/xiaomai__P01-standing-neutral__E01-joy__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E01-joy__v01__v1.0.png` |
| 喜－开心 · 挥手掰掰 | <img src="Sample/成果/喜-开心/xiaomai__P06-wave-goodbye__E01-joy__v01__v1.0.png" width="160" /> | `xiaomai__P06-wave-goodbye__E01-joy__v01__v1.0.png` |
| 乐－开怀大笑 | <img src="Sample/成果/乐-开怀大笑/xiaomai__P01-standing-neutral__E04-laughter__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E04-laughter__v01__v1.0.png` |
| 乐－强忍笑意 | <img src="Sample/成果/乐-强忍笑意/xiaomai__P01-standing-neutral__E14-suppress-laugh__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E14-suppress-laugh__v01__v1.0.png` |
| 乐－古灵精怪 | <img src="Sample/成果/乐-古灵精怪/xiaomai__P01-standing-neutral__E16-mischievous__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E16-mischievous__v01__v1.0.png` |
| 怒－愤怒 | <img src="Sample/成果/怒-愤怒/xiaomai__P01-standing-neutral__E02-anger__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E02-anger__v01__v1.0.png` |
| 怒－生气带笑 | <img src="Sample/成果/怒-生气带笑/xiaomai__P01-standing-neutral__E11-angry-smile__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E11-angry-smile__v01__v1.0.png` |
| 哀－哀伤 | <img src="Sample/成果/哀-哀伤/xiaomai__P01-standing-neutral__E03-sadness__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E03-sadness__v01__v1.0.png` |
| 哀－哭泣（自然站立） | <img src="Sample/成果/哀-哭泣/xiaomai__P01-standing-neutral__E09-crying__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E09-crying__v01__v1.0.png` |
| 哀－哭泣（五体投地） | <img src="Sample/成果/哀-哭泣/xiaomai__P25-dogeza-prostrate__E09-crying__v01__v1.0.png" width="160" /> | `xiaomai__P25-dogeza-prostrate__E09-crying__v01__v1.0.png` |
| 哀－委屈 | <img src="Sample/成果/哀-委屈/xiaomai__P01-standing-neutral__E07-aggrieved__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E07-aggrieved__v01__v1.0.png` |
| 惊－惊吓 | <img src="Sample/成果/惊-惊吓/xiaomai__P01-standing-neutral__E06-fright__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E06-fright__v01__v1.0.png` |
| 惊－震惊 | <img src="Sample/成果/惊-震惊/xiaomai__P01-standing-neutral__E05-surprise__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E05-surprise__v01__v1.0.png` |
| 静－困倦（躺着） | <img src="Sample/成果/静-困倦/xiaomai__P22-lying-supine__E30-sleepy__v01__v1.0.png" width="160" /> | `xiaomai__P22-lying-supine__E30-sleepy__v01__v1.0.png` |
| 静－平静（盘坐） | <img src="Sample/成果/静-平静/xiaomai__P17-cross-legged__E23-calm__v01__v1.0.png" width="160" /> | `xiaomai__P17-cross-legged__E23-calm__v01__v1.0.png` |
| 静－无语（自然站立） | <img src="Sample/成果/静-无语/xiaomai__P01-standing-neutral__E22-speechless__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E22-speechless__v01__v1.0.png` |
| 静－无语（懒趴） | <img src="Sample/成果/静-无语/xiaomai__P20-lazy-prone__E22-speechless__v01__v1.0.png" width="160" /> | `xiaomai__P20-lazy-prone__E22-speechless__v01__v1.0.png` |
| 静－疑惑 | <img src="Sample/成果/静-疑惑/xiaomai__P01-standing-neutral__E29-confused__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E29-confused__v01__v1.0.png` |
| 静－面无表情 | <img src="Sample/成果/静-面无表情/xiaomai__P01-standing-neutral__E21-neutral__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E21-neutral__v01__v1.0.png` |
| 厌－嫌弃 | <img src="Sample/成果/厌-嫌弃/xiaomai__P01-standing-neutral__E18-disgust__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E18-disgust__v01__v1.0.png` |
| 怒－面无表情地生气 | <img src="Sample/成果/怒-面无表情地生气/xiaomai__P01-standing-neutral__E24-silent-anger__v01__v1.0.png" width="160" /> | `xiaomai__P01-standing-neutral__E24-silent-anger__v01__v1.0.png` |

更多教学细节请见 [Sample/教学.md](Sample/教学.md)，Skill 完整规则请见 [Skill/character-storyboard-generator/SKILL.md](Skill/character-storyboard-generator/SKILL.md)。

## 待办事项

尚未完成的工作请见 [待办事项.md](待办事项.md)。
