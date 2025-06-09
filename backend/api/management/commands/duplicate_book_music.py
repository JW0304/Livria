# api/management/commands/duplicate_book_music.py
import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from api.models import Music

class Command(BaseCommand):
    help = (
        "이미 생성된 책 음악을 복사하여, "
        "다른 책(book_id)에 동일한 감성 태그로 새 레코드를 생성합니다."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--from-book",
            type=int,
            required=True,
            help="원본으로 사용할 책의 pk (Existing Music이 이 책에 있어야 함)",
        )
        parser.add_argument(
            "--to-books",
            nargs="+",
            type=int,
            required=True,
            help="복사 대상 책들의 pk 리스트 (space 로 구분)",
        )

    def handle(self, *args, **options):
        src_book_id = options["from_book"]
        dst_book_ids = options["to_books"]

        # 1) 원본 Music들 조회
        src_musics = Music.objects.filter(book_id=src_book_id)
        if not src_musics.exists():
            self.stderr.write(self.style.ERROR(f"Book(pk={src_book_id})에는 생성된 음악이 없습니다."))
            return

        for music in src_musics:
            for dst_id in dst_book_ids:
                # 이미 해당 책+태그 조합이 있으면 건너뜀
                if Music.objects.filter(book_id=dst_id, tag=music.tag).exists():
                    self.stdout.write(f"→ Book {dst_id} 에 이미 '{music.tag}' 태그 음악이 존재하여 건너뜁니다.")
                    continue

                # 2) 파일 복사
                src_path = music.audio_file.path
                # 새 filename: book_{dst_id}_{tag}.확장자
                ext = os.path.splitext(src_path)[1]
                safe_tag = music.tag.replace(" ", "_")
                new_filename = f"book_{dst_id}_{safe_tag}{ext}"
                rel_dest = os.path.join("book_music", new_filename)
                abs_dest = os.path.join(settings.MEDIA_ROOT, rel_dest)
                os.makedirs(os.path.dirname(abs_dest), exist_ok=True)
                shutil.copy(src_path, abs_dest)

                # 3) DB 레코드 생성
                new_music = Music.objects.create(
                    book_id=dst_id,
                    tag=music.tag,
                    audio_file=rel_dest,
                    created_at=timezone.now()
                )
                self.stdout.write(
                    f"✅ Book {dst_id}에 '{music.tag}' 복제 완료 → {rel_dest}"
                )

        self.stdout.write(self.style.SUCCESS("모든 복제 작업이 완료되었습니다."))
