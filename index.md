---
publish:  true
---

# 옵시디언 볼트 메인 인덱스

## 프로젝트 정보
- [[readme]] - 이 볼트의 전체 구조와 사용법에 대한 상세 설명

## 주요 섹션들 (태그 + 색인)

```dataview
list
from ""
where contains(publish, true)
    and (contains(file.folder, "3-🏷️ 태그") or (contains(file.folder, "4-📋 색인") and file.path != this.file.path))
```

```dataview
TABLE length(rows.file.link) as "노트 수"
FROM ""
WHERE file.folder != ""
GROUP BY file.folder as "폴더"
```