# 在导出 PDF 时需要忽略的 Markdown 文件或目录 每行填写一个相对于仓库根目录的路径；支持注释与空行

README.md
AGENTS.md
tools
_*.md
Glossary.md
docs\VALIDATION_REPORT.md
docs\Glossary.md
docs\README.md
CONTRIBUTING.md

# 排除所有索引文件

*index.md
*index-*.md

# 排除所有导览文件

*Guide.md
*-Guide.md

# 排除报表

docs/entries/Multidimensional-Inventory-of-Dissociation-MID-60.md
docs/entries/Dissociative-Experiences-Scale-DES-II.md
docs/entries/Dissociative-Experiences-Scale-DES-II.md
docs/entries/Somatoform-Dissociation-Questionnaire-SDQ-20.md

# 不导出前言（用户要求，2026-10-31）
docs/Preface.md

# 交互式量表词条：正文是 HTML 控件（滑块/按钮/表格 UI），PDF 里只剩不可读的长串
docs/entries/DND-Alignment-Test.md
docs/entries/Experiences-in-Close-Relationships-ECR-Chinese.md
docs/entries/Generalized-Anxiety-Disorder-7-GAD-7.md
docs/entries/Patient-Health-Questionnaire-9-PHQ-9.md
docs/entries/Self-Rating-Anxiety-Scale-SAS.md
docs/entries/Self-Rating-Depression-Scale-SDS.md
docs/entries/Symptom-Checklist-90-SCL-90.md
