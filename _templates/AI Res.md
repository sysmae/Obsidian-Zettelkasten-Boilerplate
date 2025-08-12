---
publish:  false
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

/* 2) 이전 노트 찾기 (여러 방법 시도) */
let linkedNote = "";
try {
  // 방법 1: 현재 활성화된 다른 파일들 확인
  const allLeaves = app.workspace.getLeavesOfType("markdown");
  const currentFile = tp.file.path(true);
  
  for (let leaf of allLeaves) {
    if (leaf.view.file && leaf.view.file.path !== currentFile) {
      const prevFileName = leaf.view.file.basename;
      linkedNote = `[[${prevFileName}]]`;
      break;
    }
  }
  
  // 방법 2: 최근 파일 목록에서 찾기 (방법 1이 실패한 경우)
  if (!linkedNote) {
    const recentFiles = app.workspace.getLastOpenFiles();
    if (recentFiles.length > 1) {
      // 현재 파일이 아닌 가장 최근 파일
      for (let filePath of recentFiles) {
        if (filePath !== currentFile) {
          const file = app.vault.getAbstractFileByPath(filePath);
          if (file) {
            linkedNote = `[[${file.basename}]]`;
            break;
          }
        }
      }
    }
  }
  
  // 방법 3: workspace history (백업 방법)
  if (!linkedNote) {
    const workspace = app.workspace;
    if (workspace.lastActiveFile && workspace.lastActiveFile.path !== currentFile) {
      linkedNote = `[[${workspace.lastActiveFile.basename}]]`;
    }
  }
  
} catch (error) {
  console.log("이전 노트 연결 중 오류:", error);
  linkedNote = "";
}

// 디버깅용 로그 (필요시 주석 해제)
// console.log("Current file:", tp.file.path(true));
// console.log("Found linked note:", linkedNote);
-%>
#<% tp.date.now() %> <% tp.date.now("HH:mm") %>

Tags:

# <% title %>

## 레퍼런스(References)
<% linkedNote %>