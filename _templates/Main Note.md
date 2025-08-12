---
publish: false
---

<%*
/* 1) 제목 처리 */
const currentFileName = tp.file.title;
let title;

if (
  currentFileName === "Untitled" ||
  currentFileName.startsWith("새 파일") ||
  /^Untitled\s*\d*$/.test(currentFileName) ||
  currentFileName === "" ||
  currentFileName === "무제"
) {
  title = await tp.system.prompt("노트 제목을 입력하세요:");
  if (title && title.trim() !== "") {
    await tp.file.rename(title.trim());
  } else {
    title = currentFileName || "무제";
  }
} else {
  title = currentFileName;
}
%>
#<% tp.date.now() %> <% tp.date.now("HH:mm") %>

Tags:

# <% title %>


### 언급한 노트 (Outgoing Links)
```dataview
LIST
FROM -"Templates"
WHERE contains(this.file.outlinks, file.link) AND file.name != this.file.name
```
### 백링크 (Backlinks)
```dataview
LIST
FROM [[]]
```

