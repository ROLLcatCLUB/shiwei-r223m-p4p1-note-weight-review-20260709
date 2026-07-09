# R223M-P4-P1 页边注与注释减重策略

```text
stage_id=1013R_R223M_P4_P1_NOTE_WEIGHT_REDUCTION_AND_MARGINIZATION
default_teacher_view=continuous_lesson_text_first
review_view=full_note_ledger_available
```

## 默认教师稿

- 保留：环节标题、本环节在做什么、教师关注、连续教学过程、过渡语、下游影响。
- 降权：完整小教判断、完整控制点、组件触发、素材/组件确认。
- 不展示：核心/风险/建议/确认四项清单，不在每个环节前重复素材确认。

## 页边注化

“教师关注”和“下游影响”只作为轻提示，不改变教学过程的阅读主线。完整信息进入 `R223M_P4_P1_marginized_review_note_ledger.json`，供审核视图、开发视图或后续工作台折叠查看。

完整小教判断、完整控制点、组件触发和素材确认不压在教学过程正文前。
