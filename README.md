# Mabyko Mono

Mabyko Mono는 [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono),
[D2Coding](https://github.com/naver/d2codingfont),
[Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)를 합성한 한국어 친화
프로그래밍 폰트입니다.

한글과 라틴 문자를 함께 쓰는 코드 편집 환경에서 자연스럽게 보이는 고정폭 폰트를
목표로 합니다. 특히 VS Code에서 한글 wrap과 selection이 어긋나지 않도록,
한글과 full-width 문자의 폭을 라틴 문자 폭의 정확히 2배로 맞춥니다.

## 미리보기

| Mabyko Mono NF | Mabyko Mono | Mabyko Mono NL |
| :---: | :---: | :---: |
| ![Mabyko Mono NF](assets/preview-MabykoMonoNF.png) | ![Mabyko Mono](assets/preview-MabykoMono.png) | ![Mabyko Mono NL](assets/preview-MabykoMonoNL.png) |

## 특징

- JetBrains Mono 기반의 라틴 문자와 프로그래밍 기호
- D2Coding 기반의 한글 glyph와 full-width metric
- Nerd Font symbols 포함 variant 제공
- 한글과 full-width glyph를 라틴 문자 2칸 폭으로 처리
- 기본 폭: half-width `600`, full-width `1200`

## 폰트 종류

| Variant | Family name | 설명 |
| --- | --- | --- |
| Standard NF | `Mabyko Mono NF` | Nerd Font symbols 포함 |
| Standard | `Mabyko Mono` | Nerd Font symbols 미포함 |
| Standard NL | `Mabyko Mono NL` | Nerd Font symbols 미포함, ligature 제거 |

각 variant는 `Thin`, `Light`, `Regular`, `Medium`, `SemiBold`, `Bold`를 제공합니다.
`NL`은 No Ligatures를 뜻합니다.

## 다운로드

최신 버전은 [Releases](https://github.com/mabyko/MabykoMono/releases/latest)에서
받을 수 있습니다.

## 설치

1. Releases에서 원하는 zip 파일을 다운로드합니다.
2. 압축을 풉니다.
3. 필요한 `.ttf` 파일을 설치합니다.

### macOS

`.ttf` 파일을 더블클릭한 뒤 Font Book에서 설치합니다.

### Windows

`.ttf` 파일을 선택한 뒤 우클릭해서 설치합니다.

### Linux

`.ttf` 파일을 `~/.local/share/fonts`에 복사한 뒤 font cache를 갱신합니다.

```sh
fc-cache -f
```

VS Code에서는 설치 후 아래처럼 설정합니다.

```json
{
  "editor.fontFamily": "Mabyko Mono NF"
}
```

### 업데이트

폰트 파일에는 업그레이드 개념이 없어서, 같은 이름의 새 버전을 설치하면
중복 설치로 처리됩니다. 이전 버전을 제거한 뒤 새 버전을 설치합니다.

- macOS: 서체 관리자에서 `Mabyko Mono` 패밀리를 제거한 뒤 새로 설치합니다.
- Windows: 설정 → 개인 설정 → 글꼴에서 제거한 뒤 새로 설치합니다.
- Linux: `~/.local/share/fonts`의 기존 파일을 덮어쓰고 `fc-cache -f`를 실행합니다.

## 빌드

### 로컬 빌드

필요한 도구:

- Python 3.12 이상
- [uv](https://github.com/astral-sh/uv)
- FontForge
- HarfBuzz `hb-shape`
- Fontconfig `fc-scan`

빌드와 검증:

```sh
uv sync --locked
uv run --locked python scripts/fetch.py
rm -rf build out/fonts
fontforge -script scripts/build_regular.py
uv run --locked python scripts/fix_tables.py
uv run --locked python scripts/test_font.py
uv run --locked python scripts/package_release.py
uv run --locked python scripts/test_outputs.py
```

산출물은 `out/fonts/` 아래에 생성됩니다.
Release zip 파일은 `out/release/` 아래에 생성됩니다.
각 ZIP에는 폰트 6개와 `LICENSE`, 원본 저작권·라이선스 고지를 담은 `licenses/`가 포함됩니다.

### Docker 빌드

로컬에 FontForge나 HarfBuzz를 설치하지 않고 Docker로도 같은 빌드를 실행할 수 있습니다.

```sh
docker compose run --rm build
```

Docker는 현재 작업 폴더만 `/work`로 마운트합니다. Python 가상환경과 uv cache는
Docker 전용 volume을 사용하므로 로컬 `.venv`는 사용하지 않습니다. Docker 환경을
초기화하려면 `docker compose down -v`를 실행합니다.

Docker 이미지는 `mabyko/mabyko-mono-build:1.1.0` 이름으로
생성됩니다.
이미지까지 지우려면 아래 명령을 실행합니다.

```sh
docker compose down -v
docker image rm mabyko/mabyko-mono-build:1.1.0
```

이미 생성된 산출물을 다시 검증할 때:

```sh
docker compose run --rm test
```

컨테이너 shell로 들어갈 때:

```sh
docker compose run --rm shell
```

### 재현성과 CI

Docker 빌드는 Ubuntu 이미지 digest, APT 스냅샷(`20260905T000000Z`),
uv `0.12.10`을 고정합니다. Python은 스냅샷의 시스템 Python을 사용하고,
fontTools는 `uv.lock`에 고정된 버전을 `--locked`로 설치합니다.
로컬 빌드는 설치된 FontForge·HarfBuzz 버전에 따라 결과가 달라질 수 있습니다.

`config.ini`의 `source_date_epoch`는 TTF와 ZIP의 고정 생성 시각(UTC Unix 초)입니다.
폰트의 생성·수정 시각을 통일하고 FontForge의 `FFTM` 시각 테이블은 제거합니다.
ZIP은 파일의 수정 시각이나 권한에 영향을 받지 않도록 패키징합니다.
PR과 `main` push의 CI는 전체 빌드·검증 후 다시 빌드해 TTF 18개와 ZIP 3개의 SHA256을 비교합니다.
해시 일치는 같은 아키텍처와 고정된 빌드 환경을 기준으로 검증합니다.

도구 버전을 갱신할 때는 Dockerfile의 이미지 digest와 APT 스냅샷을 갱신하고
전체 빌드·해시 비교를 다시 수행합니다. 원본 폰트를 갱신할 때는 `config.ini`의
버전·URL·SHA256·경로와 `licenses/`의 해당 원본 고지를 함께 갱신합니다.
프로젝트 버전은 `config.ini`와 `pyproject.toml`을 함께 바꾸고 `uv lock`으로 반영합니다.

다운로드나 FontForge 없이 빌드 스크립트의 회귀 검증만 실행할 수도 있습니다.

```sh
uv run --locked python scripts/test_build.py
```

ZIP·tar 압축 해제는 임시 폴더에서 완료된 뒤 원본 폴더로 이동합니다.
실패하면 임시 파일을 정리하므로 재실행할 수 있습니다.

## Contributing

- 새 glyph 범위나 metric 정책을 바꾸면 `scripts/test_font.py`에 검증을 추가합니다.
- 새 variant를 추가하면 `scripts/test_outputs.py`의 기대 산출물도 함께 갱신합니다.
- `sources/`, `build/`, `out/`은 생성물이라 커밋하지 않습니다.
- D2Coding의 Reserved Font Name 조건 때문에 family name에 `D2Coding`을 쓰지 않습니다.
- 릴리스 노트는 Release Drafter가 PR 라벨을 기준으로 한국어 draft를 만듭니다.
  PR에는 `feature`, `fix`, `font`, `build`, `docs`, `chore` 중 알맞은 라벨을 붙입니다.

## 라이선스

Mabyko Mono는 SIL Open Font License 1.1, 즉 OFL 1.1로 배포합니다.

이 프로젝트는 아래 폰트의 데이터를 사용합니다.

- JetBrains Mono: Copyright 2020 The JetBrains Mono Project Authors.
  https://github.com/JetBrains/JetBrainsMono
- D2Coding: Copyright NAVER Corp.
  https://github.com/naver/d2codingfont
- Nerd Fonts: Copyright (c) 2014 Ryan L McIntyre.
  https://github.com/ryanoasis/nerd-fonts

원본 배포본의 고지는 `licenses/`에 보존합니다. JetBrains Mono와 D2Coding의
OFL 전문 및 Nerd Fonts 배포본의 MIT 라이선스를 릴리스 ZIP에도 동봉합니다.

`JetBrains Mono`, `D2Coding`, `Nerd Fonts` 이름은 출처 표기를 위해서만 사용합니다.
생성되는 폰트 family name은 `Mabyko Mono`, `Mabyko Mono NF`, `Mabyko Mono NL`입니다.
