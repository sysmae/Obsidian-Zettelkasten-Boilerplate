---
publish: 
---
<%* 
// 1) 제목을 사용자에게 입력받아 변수에 저장
const title = await tp.system.prompt("노트 제목을 입력하세요:");
// 2) 실제 파일명으로 리네임
await tp.file.rename(title);
// 3) 변수값을 헤딩으로 출력
-%>
# <% title %>

### 색인(Indexes)

### 관련 노트(Notes)
```dataview
list
from [[<% title %>]]
```