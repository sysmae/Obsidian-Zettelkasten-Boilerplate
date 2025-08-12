---
type: weekly
week: <% tp.file.title %>
---

<%*
const weekTitle = tp.file.title; // 예: 2025-W30

// ISO 주차에서 실제 날짜 계산 함수
function getDateFromWeek(weekStr, weekday) {
    const match = weekStr.match(/(\d{4})-W(\d{2})/);
    if (!match) return null;
    
    const year = parseInt(match[1]);
    const weekNum = parseInt(match[2]);
    
    // 해당 년도 1월 4일 (ISO 주차 기준점)
    const jan4 = new Date(year, 0, 4);
    const jan4Weekday = jan4.getDay() || 7; // 일요일=0 -> 7로 변환
    
    // 첫째 주 월요일
    const firstMonday = new Date(jan4.getTime() - (jan4Weekday - 1) * 24 * 60 * 60 * 1000);
    
    // 원하는 주의 월요일
    const weekStart = new Date(firstMonday.getTime() + (weekNum - 1) * 7 * 24 * 60 * 60 * 1000);
    
    // 원하는 요일 (월요일=1, 일요일=7)
    const targetDate = new Date(weekStart.getTime() + (weekday - 1) * 24 * 60 * 60 * 1000);
    
    return targetDate.toISOString().split('T')[0];
}

// 7일간의 날짜 정확히 계산
const days = [];
const dayNames = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"];
for (let i = 1; i <= 7; i++) {
    const date = getDateFromWeek(weekTitle, i);
    const dayName = dayNames[i-1];
    days.push({date, dayName});
}

// 시작일과 종료일
const startDate = days[0].date;
const endDate = days[6].date;
const startMonth = new Date(startDate).toLocaleDateString('ko-KR', {month: 'long', day: 'numeric'});
const endMonth = new Date(endDate).toLocaleDateString('ko-KR', {month: 'long', day: 'numeric'});

// 이전주, 다음주 계산
const currentWeekNum = parseInt(weekTitle.match(/W(\d+)/)[1]);
const year = parseInt(weekTitle.match(/(\d{4})/)[1]);
const prevWeek = `${year}-W${String(currentWeekNum - 1).padStart(2, '0')}`;
const nextWeek = `${year}-W${String(currentWeekNum + 1).padStart(2, '0')}`;

// 전체 템플릿 출력
tR += `# 📚 ${weekTitle} 주간 노트
*${startMonth} ~ ${endMonth}*

---
## 🗓️ 네비게이션
- **이전 주**: [[${prevWeek}]]
- **다음 주**: [[${nextWeek}]]

### 📅 일간 노트 바로가기
|일 | 월 | 화 | 수 | 목 | 금 | 토 |
|---|---|---|---|---|---|---|
| [[${days[0].date}]] | [[${days[1].date}]] | [[${days[2].date}]] | [[${days[3].date}]] | [[${days[4].date}]] | [[${days[5].date}]] | [[${days[6].date}]] |

---

\`\`\`dataview
TABLE WITHOUT ID
"[[" + file.name + "|" + file.name + "]]" as "📅 날짜",
choice(file.mtime = file.ctime, "📝 새 노트", "✅ 작성됨") as "📊 상태",
file.mtime as "🕐 수정일시",
"약 " + round(file.size / 3, 0) + "자" as "📝 글자수"
FROM "2 - ✍️ 문헌 노트/데일리노트"
WHERE file.name >= "${startDate}" AND file.name <= "${endDate}"
AND file.name != this.file.name
SORT file.name ASC
\`\`\`

## 📖 일간 노트 뷰어
`;

days.forEach(d => {
    tR += `![[${d.date}]]\n\n`;
});

// 프론트매터 업데이트 (템플릿 마지막에 실행)
setTimeout(async () => {
    try {
        await tp.obsidian.fileManager.processFrontMatter(tp.file.find_tfile(), (frontmatter) => {
            frontmatter.startDate = startDate;
            frontmatter.endDate = endDate;
        });
    } catch (error) {
        console.log("프론트매터 업데이트 오류:", error);
    }
}, 100);
%>
