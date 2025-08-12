#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
옵시디언 메타데이터 자동 추가 스크립트
특정 폴더의 모든 .md 파일에 frontmatter 메타데이터를 안전하게 추가합니다.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime


def add_metadata_to_obsidian_folder(
    folder_path, metadata_key="publish", metadata_value="true", create_backup=True
):
    """
    옵시디언 폴더의 모든 .md 파일에 메타데이터를 안전하게 추가

    Args:
        folder_path (str): 대상 폴더 경로
        metadata_key (str): 추가할 메타데이터 키 (기본값: "publish")
        metadata_value (str): 추가할 메타데이터 값 (기본값: "true")
        create_backup (bool): 백업 생성 여부 (기본값: True)

    Returns:
        bool: 처리 성공 여부
    """

    print(f"📁 대상 폴더: {folder_path}")
    print(f"🏷️  추가할 메타데이터: {metadata_key}: {metadata_value}")
    print("-" * 60)

    # 폴더 경로 확인
    folder_path = Path(folder_path)
    if not folder_path.exists():
        print(f"❌ 폴더를 찾을 수 없습니다: {folder_path}")
        return False

    # .md 파일 찾기 (하위 폴더 포함)
    md_files = list(folder_path.rglob("*.md"))

    if not md_files:
        print(f"📝 폴더에 .md 파일이 없습니다: {folder_path}")
        return False

    print(f"📋 총 {len(md_files)}개의 .md 파일을 찾았습니다.")

    # 백업 폴더 생성
    backup_folder = None
    if create_backup:
        backup_folder = (
            folder_path.parent / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        backup_folder.mkdir(exist_ok=True)
        print(f"💾 백업 폴더 생성: {backup_folder}")

    processed_files = 0
    skipped_files = 0
    error_files = 0

    for file_path in md_files:
        try:
            print(f"🔍 처리중: {file_path.name}")

            # 백업 생성
            if create_backup:
                # 하위 폴더 구조 유지하며 백업
                relative_path = file_path.relative_to(folder_path)
                backup_file = backup_folder / relative_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_file)

            # 파일 읽기
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # frontmatter 패턴 매칭
            frontmatter_pattern = r"^---\n(.*?)\n---\n"
            frontmatter_match = re.match(frontmatter_pattern, content, re.DOTALL)

            # 새 메타데이터 라인
            new_metadata_line = f"{metadata_key}: {metadata_value}"

            if frontmatter_match:
                # 기존 frontmatter가 있으면 publish 키가 있는지 확인 후 업데이트 또는 추가
                existing_frontmatter = frontmatter_match.group(1)
                lines = existing_frontmatter.split("\n")
                updated = False
                skipped = False
                for idx, line in enumerate(lines):
                    key_match = re.match(
                        rf"^\s*{re.escape(metadata_key)}\s*:\s*(.*)$", line
                    )
                    if key_match:
                        value = key_match.group(1).strip().lower()
                        if value == metadata_value.lower():
                            print(
                                f"   ⏭️  이미 {metadata_key}: {metadata_value} 상태, 건너뜀"
                            )
                            skipped = True
                        else:
                            lines[idx] = new_metadata_line
                            updated = True
                            print(f"   🔄 {metadata_key} 메타데이터 값 업데이트")
                        break
                if skipped:
                    skipped_files += 1
                    continue
                if not updated and not skipped:
                    lines.append(new_metadata_line)
                    print(f"   ✅ 기존 frontmatter에 메타데이터 추가")
                new_frontmatter = f"---\n" + "\n".join(lines) + "\n---\n"
                new_content = content.replace(
                    frontmatter_match.group(0), new_frontmatter
                )
            else:
                # frontmatter가 없으면 새로 생성
                new_frontmatter = f"---\n{new_metadata_line}\n---\n\n"
                new_content = new_frontmatter + content
                print(f"   ✅ 새 frontmatter 생성하여 메타데이터 추가")

            # 파일 쓰기
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            processed_files += 1

        except Exception as e:
            print(f"   ❌ 오류 발생: {str(e)}")
            error_files += 1

    print("\n" + "=" * 60)
    print(f"🎉 작업 완료 결과:")
    print(f"   ✅ 처리된 파일: {processed_files}개")
    print(f"   ⏭️  건너뛴 파일: {skipped_files}개")
    print(f"   ❌ 오류 파일: {error_files}개")

    if create_backup and processed_files > 0:
        print(f"   💾 백업 위치: {backup_folder}")

    return processed_files > 0


def main():
    """
    메인 실행 함수
    여기서 폴더 경로를 설정하고 스크립트를 실행합니다.
    """

    # ========== 여기를 수정하세요 ==========

    # 옵시디언 볼트 내의 대상 폴더 경로를 입력하세요
    # Windows 예시: r"C:\Users\사용자명\Documents\ObsidianVault\1 - 📚 참고 노트\ai 답변"
    # Mac/Linux 예시: "/Users/사용자명/Documents/ObsidianVault/1 - 📚 참고 노트/ai 답변"

    folder_path = "1-📚 참고 노트/ai 답변"  # ← 실제 경로로 변경하세요

    # 추가할 메타데이터 설정 (필요시 수정)
    metadata_key = "publish"
    metadata_value = "true"

    # 백업 생성 여부 (안전을 위해 True 권장)
    create_backup = False  # ← 필요시 True로 변경

    # =====================================

    print("🚀 옵시디언 메타데이터 자동 추가 스크립트 시작")
    print("=" * 60)

    # 실행 전 확인
    print(f"설정 확인:")
    print(f"  - 대상 폴더: {folder_path}")
    print(f"  - 메타데이터: {metadata_key}: {metadata_value}")
    print(f"  - 백업 생성: {'예' if create_backup else '아니오'}")
    print()

    # response = input("계속 진행하시겠습니까? (y/N): ")
    # if response.lower() not in ["y", "yes", "예"]:
    #     print("❌ 작업이 취소되었습니다.")
    #     return

    # 메타데이터 추가 실행
    success = add_metadata_to_obsidian_folder(
        folder_path=folder_path,
        metadata_key=metadata_key,
        metadata_value=metadata_value,
        create_backup=create_backup,
    )

    # if success:
    #     print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
    # else:
    #     print("\n❌ 작업 중 문제가 발생했습니다.")


if __name__ == "__main__":
    main()
