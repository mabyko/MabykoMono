# 폰트 구성과 버전 확인

2026-10-08 기준. Mabyko Mono 0.5.0은 기본형의 비율을 유지하고 Narrow 계열을 추가한다.

## 선택한 폭과 모양

| 계열 | 영문 셀 | 한글·전각 셀 | 윤곽 처리 |
| --- | ---: | ---: | --- |
| 기본형 | 600 | 1200 | 기존 영문과 한글 모양 유지 |
| Narrow | 500 | 1000 | 영문 가로만 5/6, 한글 원본 모양 유지 |

두 계열 모두 UPM 1000에서 한글을 영문 두 칸에 배치한다. Narrow는 UPM이나 폰트 크기를
줄이지 않아 글자 높이·기준선·줄 높이를 유지한다. 영문을 압축하므로 세로획은 더 얇아질 수 있다.
한글 가로 1.05~1.15배 확대안은 비교용으로만 만들었으며 최종 배포에 적용하지 않았다.

각 계열에는 일반형, `NL`(합자 제거), `NF`(Nerd Font 기호 포함)가 있다. 각 6굵기를 제공해
36개 TTF와 6개 ZIP을 생성한다. 패밀리와 파일 이름은 README의 폰트 종류 표를 따른다.
Narrow는 별도 패밀리이므로 기본형과 함께 설치할 수 있다.

[기본형·Narrow 미리보기](../assets/preview-Narrow-comparison.png)는 이번 빌드의 폰트를 사용한다.
브라우저에서 20px 기준 기본형 `12/24px`, Narrow `10/20px`의 실제 문자 폭과 6개 패밀리 로드를 확인했다.

폭은 `config.ini`의 `half_width`/`full_width`, `narrow_half_width`/`narrow_full_width`로 정한다.
한글·전각 폭은 각 영문 폭의 정확히 두 배여야 한다. Narrow NF의 기호와 Powerline도 500 셀에 맞춘다.

## 최신 버전 확인

공식 최신 정식 릴리스와 PyPI 메타데이터를 직접 조회했다. 이미 최신인 원본은 유지했다.

| 항목 | 기존 → 적용 | 확인한 출처 |
| --- | --- | --- |
| JetBrains Mono | 2.304 유지 | [공식 최신 릴리스](https://github.com/JetBrains/JetBrainsMono/releases/latest) |
| D2Coding | 1.3.3 → 1.4.0 | [공식 1.4.0 릴리스](https://github.com/naver/d2-coding-font/releases/tag/VER1.4.0) |
| Nerd Fonts | 3.5.1 유지 | [공식 최신 릴리스](https://github.com/ryanoasis/nerd-fonts/releases/latest) |
| fontTools | 4.64.0 → 4.66.1 | [PyPI](https://pypi.org/project/fonttools/4.66.1/) |
| uv | 0.12.10 → 0.12.23 | [공식 릴리스](https://github.com/astral-sh/uv/releases/tag/0.12.23) |

D2Coding은 일반 Regular/Bold에서 한글·전각 범위만 가져온다. 영문·숫자·합자는 JetBrains Mono를
사용하므로 D2Coding 1.4.0의 영문 대체 숫자 기능이 우리 숫자에 추가되는 것은 아니다.
원본 ZIP의 SHA256을 `config.ini`에 고정했고, 새 ZIP의 OFL 고지는 현재 보관본과 바이트가 같았다.

fontTools는 `uv.lock`, uv는 Docker 이미지 digest로 고정한다. Docker 빌드 이미지 이름은
`mabyko/mabyko-mono-build:1.2.0`이며 Ubuntu digest와 APT 스냅샷은 기존 값을 유지한다.

## 검증과 참고 자료

`scripts/test_font.py`는 실제 advance, 범위 커버리지, 리거처 유무, NF/Powerline 셀 폭,
버전·패밀리·고정폭 메타데이터를 검사한다. Narrow와 대응하는 기본형의 완성형 한글 11,172자
크기·수직 위치, ASCII 높이와 줄 높이 메트릭도 비교한다. ZIP의 폰트·라이선스 내용은
`scripts/test_outputs.py`로 확인하며 CI는 두 번의 전체 빌드 SHA256을 비교한다.

선호 조사와 비교용 합성 실험의 상세 기록:

- [영문 베이스 후보](research/mono-font-candidates-2026-10-07.md)
- [Pretendard와 Jetendard](research/pretendard-mono-2026-10-07.md)
- [D2Coding 한글 간격과 배율](research/d2coding-hangul-spacing-2026-10-08.md)

연구 기록의 임시 파일 경로와 당시의 미적용 상태는 조사 시점의 이력이다. 현재 배포 구성을
확인할 때는 이 문서와 README, `config.ini`를 기준으로 한다. 실제 에디터의 작은 크기 힌팅과
읽기 선호는 환경마다 다를 수 있어 수치 검증만으로 가독성의 우열을 단정하지 않는다.
