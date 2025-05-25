# api/management/commands/generate_book_music.py

import os
from django.core.management.base import BaseCommand, CommandError
from api.models import Book, Music, EmotionTag
from api.services.music_service import generate_music_tensor
from torchaudio import save as torchaudio_save

class Command(BaseCommand):
    help = "도서별 감성 태그마다 MusicGen으로 음악을 생성하고 저장합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--book_id",
            type=int,
            required=True,
            help="음악을 생성할 Book의 PK",
        )

    def handle(self, *args, **options):
        book_id = options["book_id"]
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise CommandError(f"Book(id={book_id}) 를 찾을 수 없습니다.")

        tags = [et.name for et in EmotionTag.objects.all()]
        if not tags:
            self.stdout.write(self.style.WARNING("데이터베이스에 EmotionTag가 없습니다."))
            return

        for tag in tags:
            self.stdout.write(f"[{book.title}] '{tag}' 생성 중…")
            try:
                wav = generate_music_tensor(tag)  # Tensor, dim=1~3
                # 차원 정리
                if wav.dim() == 3:
                    # (1, C, T) -> (C, T)
                    wav = wav.squeeze(0)
                elif wav.dim() == 1:
                    # (T,) -> (1, T)
                    wav = wav.unsqueeze(0)
                # now wav.dim()==2

                # 저장 준비
                filename = f"book_{book_id}_{tag.replace(' ', '_')}.wav"
                media_dir = os.path.join("media", "book_music")
                os.makedirs(media_dir, exist_ok=True)
                path = os.path.join(media_dir, filename)

                # 샘플레이트는 서비스 쪽 기본(44100)으로 가정
                torchaudio_save(path, wav, 44100)

                Music.objects.create(book=book, tag=tag, audio_file=f"book_music/{filename}")
                self.stdout.write(self.style.SUCCESS(f"  ✓ 저장됨: {path}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  → 실패: {e}"))

        self.stdout.write(self.style.SUCCESS("모든 음악 생성 완료."))
