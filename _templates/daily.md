---

type: daily
date: <% tp.file.title %>
week: <% tp.date.now("YYYY-[W]ww") %>
---
<%*
const weekNumber = tp.date.now("YYYY-[W]ww", 0, tp.file.title, "YYYY-MM-DD");
const dayName = tp.date.now("dddd", 0, tp.file.title, "YYYY-MM-DD");
const yesterdayDate = tp.date.now("YYYY-MM-DD", -1, tp.file.title, "YYYY-MM-DD");
const tomorrowDate = tp.date.now("YYYY-MM-DD", 1, tp.file.title, "YYYY-MM-DD");
%>

# <% tp.file.title %> (<% dayName %>)

## 📚 메모

---
### 네비게이션
- 이번 주: [[<% weekNumber %>]]
- 어제: [[<% yesterdayDate %>]]
- 내일: [[<% tomorrowDate %>]]

### 오늘 태그 노트들
```dataview
LIST
FROM ""
WHERE contains(file.tags, "#<% tp.file.title %>")
```