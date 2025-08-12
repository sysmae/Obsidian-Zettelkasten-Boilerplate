import sys
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml
from datetime import datetime
import re

# --- 설정 (사용자 직접 수정) ---
# 1. 여러분의 Obsidian Vault(보관소) 전체 경로를 입력하세요.
#    Windows 예시: "C:/Users/YourUser/Documents/ObsidianVault"
#    Mac 예시: "/Users/YourUser/Documents/ObsidianVault"
VAULT_PATH = "C:\\workspace\\ObsidianVault"

# 2. 영구 노트 폴더의 이름을 입력하세요.
TARGET_FOLDER_NAME = "5-💎 영구 노트"
# -----------------------------

# 스크립트의 동작을 기록(로깅)하기 위한 기본 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


def update_note_content(file_path):
    """지정된 마크다운 파일의 frontmatter와 본문 날짜를 읽고 업데이트합니다."""
    try:
        p = Path(file_path)
        # 파일이 존재하고, 마크다운 파일인지 다시 한번 확인
        if not p.exists() or not p.is_file() or p.suffix.lower() != ".md":
            return

        logging.info(f"파일 처리 시작: {p.name}")

        full_content = p.read_text(encoding="utf-8")

        # frontmatter와 본문을 분리
        if full_content.startswith("---"):
            parts = full_content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                content = "---".join(parts[2:])
                data = yaml.safe_load(frontmatter_str) or {}
            else:  # frontmatter 형식이 잘못된 경우
                data = {}
                content = full_content
        else:  # frontmatter가 없는 경우
            data = {}
            content = full_content

        # 1. Frontmatter의 publish 상태만 업데이트
        data["publish"] = True
        new_frontmatter_str = yaml.dump(data, allow_unicode=True, sort_keys=False)

        # 2. 본문의 날짜/시간 헤더 업데이트 또는 추가
        # [수정] '#' 바로 뒤에 공백이 없는 형식으로 변경
        new_date_line = f"#{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        # [수정] 정규식 패턴에서 공백( \s* ) 부분을 제거하여 '#{YYYY-MM-DD}' 형식을 정확히 찾도록 함
        date_line_pattern = re.compile(r"^#\d{4}-\d{2}-\d{2}.*$", re.MULTILINE)

        # 기존 날짜 라인을 찾아 교체 시도
        content, subs_made = date_line_pattern.subn(
            new_date_line, content.lstrip(), count=1
        )

        # 교체된 라인이 없다면 (기존 날짜 라인이 없었다면) 맨 위에 새로 추가
        if subs_made == 0:
            content = f"{new_date_line}\n\n{content}"

        # 최종 파일 내용 조합 및 저장
        final_content = f"---\n{new_frontmatter_str}---\n{content}"
        p.write_text(final_content, encoding="utf-8")

        logging.info(f"✅ 성공: '{p.name}' 파일이 업데이트되었습니다.")

    except Exception as e:
        logging.error(f"❌ 오류: '{file_path}' 파일 처리 중 문제 발생 - {e}")


# 신뢰성을 높이기 위해 on_created와 on_moved 이벤트를 모두 처리하는 핸들러
class NoteEventHandler(FileSystemEventHandler):
    """파일 시스템 이벤트를 처리하는 핸들러 클래스"""

    def _handle_event(self, path_str):
        """파일 생성 또는 이동 시 공통으로 호출될 내부 메소드"""
        target_path = Path(path_str)

        # 이벤트가 발생한 파일의 부모 폴더 이름이 타겟 폴더 이름과 일치하는지 확인
        if target_path.parent.name == TARGET_FOLDER_NAME:
            logging.info(
                f"감지: '{target_path.name}' 파일이 '{TARGET_FOLDER_NAME}' 폴더에 나타났습니다."
            )
            # Obsidian이 파일 쓰기를 완료할 시간을 주기 위해 짧은 지연 추가
            time.sleep(0.5)
            update_note_content(target_path)

    def on_created(self, event):
        """파일이나 폴더가 생성되었을 때 호출"""
        super().on_created(event)
        if not event.is_directory:
            self._handle_event(event.src_path)

    def on_moved(self, event):
        """파일이나 폴더가 이동했을 때 호출"""
        super().on_moved(event)
        if not event.is_directory:
            self._handle_event(event.dest_path)


if __name__ == "__main__":
    # 설정된 경로가 유효한지 확인
    path = Path(VAULT_PATH)
    if not path.is_dir():
        logging.error(
            "설정 오류: VAULT_PATH가 올바른 폴더 경로가 아닙니다. 스크립트를 종료합니다."
        )
        sys.exit(1)

    if VAULT_PATH == "여기에 여러분의 Obsidian Vault 전체 경로를 입력하세요":
        logging.error(
            "설정 오류: VAULT_PATH를 실제 Obsidian Vault 경로로 수정해주세요."
        )
        sys.exit(1)

    # 이벤트 핸들러와 옵저버(감시자) 생성
    event_handler = NoteEventHandler()  # 수정된 핸들러 사용
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=True)

    # 옵저버 시작
    observer.start()
    logging.info(
        f"'{VAULT_PATH}' 폴더 감시를 시작합니다. (중단하려면 Ctrl+C를 누르세요)"
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("감시를 중단합니다.")
    observer.join()
