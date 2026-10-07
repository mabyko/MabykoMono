# Pretendard 한글 기증과 Jetendard 비교 조사

조사 시작: 2026-10-07. 조사 완료: 2026-10-08 KST. 파일명은 조사 시작일을 유지한다. 공식 문서·릴리스·소스와 실제 폰트 바이너리를 확인했다. Mabyko Mono의 기본 폰트 설정을 바꾸거나 폰트를 설치하지 않았다.

## 결론

**공식 제품인 `Pretendard Mono`는 확인되지 않았다.** 공식 문서가 안내하는 패밀리는 Pretendard, Pretendard JP, Pretendard Std, Pretendard GOV다. 다만 Pretendard 한글을 고정폭 베이스에 합성하는 독립 프로젝트는 실제 존재한다. 가장 직접적인 비교 대상은 **Jetendard**다. [공식 패밀리 목록](https://github.com/orioncactus/pretendard/blob/main/packages/pretendard/README.md), [Jetendard 원 프로젝트](https://github.com/kuskhan/jetendard)

Pretendard 자체가 전체적으로 비례폭이라는 이유만으로 한글 기증에 부적합한 것은 아니다. 실제 Regular의 완성형 한글 11,172자는 이미 같은 advance를 갖는다. 우리 영문 600·한글 1200 규칙으로 맞추는 작업과 시각적인 크기·중심 조정이 필요하다.

Jetendard와 현재 파이프라인으로 생성한 Mabyko 비교 샘플의 **영문·한글 셀폭과 줄 높이 메트릭은 같았다.** Jetendard의 한글은 더 크고 위쪽에 자리한다. 따라서 더 편하게 보이는 원인은 셀폭 비율 변화보다 **한글 윤곽의 크기·위치·디자인**일 가능성이 있다. 실제 가독성 우위를 입증한 사용자 실험은 이번 조사에서 수행하지 않았다.

## 공식 Pretendard의 출처와 범위

제작자는 길형진이며, 공식 설명은 Inter·Source Han Sans(본고딕)·M PLUS 1p를 바탕으로 다듬었다고 밝힌다. 100~900의 9개 굵기와 가변 글꼴을 제공한다. 제품 UI와 다국어 타이포그래피를 위한 설계이며 코딩 고정폭 전용 폰트라고 소개하지 않는다. [공식 README](https://github.com/orioncactus/pretendard/blob/main/packages/pretendard/README.md), [제작자 설명](https://cactus.tistory.com/306), [공식 정적 CSS](https://github.com/orioncactus/pretendard/blob/v1.3.9/packages/pretendard/dist/web/static/pretendard.css)

최신 정식 릴리스는 v1.3.9다. 공식 릴리스 HTML의 배포 시각은 2023-11-05 18:21:09 UTC이며 내부 Regular 이름 테이블 버전은 `Version 1.309`다. 다른 버전 번호를 혼동하지 않아야 한다. [공식 릴리스](https://github.com/orioncactus/pretendard/releases/tag/v1.3.9)

## 원본 메트릭 직접 측정

공식 v1.3.9의 Regular OTF를 다운로드하고 SFNT의 `head`, `post`, `cmap`, `hmtx`를 직접 읽었다. 표의 폭은 원본 UPM 2048 기준 advance이며, 글자 획의 실제 너비와는 다르다. [확인한 공식 원본](https://github.com/orioncactus/pretendard/blob/v1.3.9/packages/pretendard/dist/public/static/Pretendard-Regular.otf)

| 범위·문자 | 확인한 코드포인트 수 | 원본 advance |
| --- | ---: | --- |
| 완성형 한글 U+AC00~D7A3 | 11,172 | 모두 1770 |
| 호환 자모 U+3131~318E | 53 | 모두 1770 |
| 조합용 자모 U+1100~11FF | 0 | cmap에 없음 |
| 전각 ASCII U+FF01~FF5E | 94 | 모두 1920 |
| CJK 문장부호 U+3000~303F | 26 | 698~1920으로 다양 |
| 영문 `i` / `W` / 숫자 `0` | 각각 1 | 446 / 1874 / 1220 |
| 공백 / 전각 공백 | 각각 1 | 514 / 1920 |

`post.isFixedPitch`는 0이다. 전체 폰트는 고정폭이지만 한글만 예외라는 뜻이 아니라, **전체는 비례폭이고 해당 완성형 한글 범위는 동일폭**이라는 뜻이다. 한글의 원래 advance를 UPM 1000으로 환산하면 약 864.26이므로, 그대로 복사한 결과는 우리 두 칸 폭 1200이 되지 않는다. 폭 정규화와 윤곽 확대는 서로 다른 결정이다.

원본 Regular SHA-256: `3ffbacde6ab8411f1d2db54bb9b1f0b3ee2a738932033722cf0388c06aed1c93`. 로컬 파일은 `/tmp/mabyko-font-research/pretendard-v1.3.9/Pretendard-Regular.otf` 및 같은 폴더의 `Pretendard-Bold.otf`다. Regular는 조사 시점 main의 동일 경로와도 바이트가 같았다.

## Jetendard의 실제 구성

Jetendard는 Pretendard 제작자의 공식 패밀리가 아니라 `kuskhan/jetendard`의 독립 합성 프로젝트다. Yeomil Mono의 구현을 바탕으로, 영문을 Geist Mono에서 JetBrainsMono Nerd Font Mono로 바꿨다. 영문·리거처·Nerd Font 기호는 JetBrainsMono Nerd Font Mono에서, 한글·CJK는 Pretendard에서 가져온다. [Jetendard README](https://github.com/kuskhan/jetendard/blob/v0.1.0/README.md), [Yeomil Mono 원 프로젝트](https://github.com/taevel02/yeomil-mono)

실제 최신 배포는 **v0.1.0, 2026-07-06 08:11:50 UTC**다. TTF·OTF·WebFont ZIP이 있다. 다운로드 스크립트는 Nerd Fonts v3.4.0과 Pretendard 1.3.9를 고정한다. 8개 굵기의 upright와 italic을 만들어 총 16변형이다. 한글/CJK 원본은 각 굵기의 Pretendard upright를 사용하며 진짜 한글 이탤릭을 제공하지는 않는다. [릴리스](https://github.com/kuskhan/jetendard/releases/tag/v0.1.0), [고정된 upstream 버전](https://github.com/kuskhan/jetendard/blob/v0.1.0/download_upstream.py), [굵기 매칭 표](https://github.com/kuskhan/jetendard/blob/v0.1.0/README.md)

다음은 실제 배포 ZIP에서 꺼낸 파일이며 자체 재빌드한 결과가 아니다.

- `/tmp/mabyko-font-research/jetendard-v0.1.0/Jetendard-Regular.ttf`
- `/tmp/mabyko-font-research/jetendard-v0.1.0/Jetendard-Bold.ttf`

[공식 TTF ZIP](https://github.com/kuskhan/jetendard/releases/download/v0.1.0/Jetendard-TTF.zip)의 SHA-256은 `399ab416895c01ddc1d43db509d7aa7cede4ad209f597ae8639c6d0194c2b133`이다. Regular SHA-256은 `2a9eb39d9013fbaf7b6474ae5e37af2de0b4c2a92827cb730ea3c9151dde69c9`이다. 배포 태그와 조사 시점 main의 `builder.py` 및 `download_upstream.py`는 각각 바이트가 같았다.

## 1.15 배율이 실제로 하는 일

빌더의 요청 윤곽 배율은 `Latin UPM / Pretendard UPM × korean_scale`이고 기본 `korean_scale`은 1.15다. 글자 advance는 이 배율로 바꾸지 않고 **영문 advance × 2**로 정한다. 우리와 같은 600짜리 영문이면 한글 advance는 1200이다. [배포 버전 빌더](https://github.com/kuskhan/jetendard/blob/v0.1.0/src/jetendard/builder.py)

빌더는 각 글리프의 실제 윤곽을 측정해 균일한 가로·세로 배율로 확대하고 셀 가운데로 이동한다. 수평 여백과 기본 폰트의 수직 안전영역을 넘어가면 개별 글리프의 배율을 줄인다. 따라서 **모든 글리프가 무조건 15% 확대된다는 뜻은 아니다.** 기본 transform의 Y 이동은 0이며, 한글 전체에 별도 baseline 이동을 넣지 않는다. `hhea`/typo 높이를 한글 donor로 교체하는 구조도 아니다. [`calculate_fitted_transform`·`get_vertical_safe_bounds`·`merge_fonts`](https://github.com/kuskhan/jetendard/blob/v0.1.0/src/jetendard/builder.py)

배율은 `--korean-scale`로 조절할 수 있다. 다만 배율을 바꿔도 셀폭은 유지되며, 더 큰 설정의 결과가 일부 글자에서 제한될 수 있다. 이는 지원 옵션의 확인이며 이번 조사에서 여러 배율의 새 Jetendard를 빌드하지는 않았다. [공식 옵션 설명](https://github.com/kuskhan/jetendard/blob/v0.1.0/README.md)

## 현재 Mabyko 구성과 바이너리 비교

비교 기준은 현재 파이프라인 그대로 JetBrains Mono 2.304 + D2Coding 1.3.3으로 생성한 Regular/Bold 샘플이다. Nerd Font를 붙이기 전이므로 전체 배포 폰트의 아이콘 커버리지까지 비교한 결과는 아니다. 기준 파일은 `/tmp/mabyko-mono-font-base-prototype-20261007/out/fonts/jb/MabykoCompareJB-Regular.ttf`와 같은 폴더의 `MabykoCompareJB-Bold.ttf`다.

| Regular 측정 항목 | 현재 Mabyko 구성 샘플 | 실제 Jetendard v0.1.0 |
| --- | --- | --- |
| UPM / 영문 advance / 완성형 한글 advance | 1000 / 600 / 1200 | 1000 / 600 / 1200 |
| `hhea` ascent / descent / gap | 1020 / -300 / 0 | 1020 / -300 / 0 |
| typo ascent / descent / gap | 1020 / -300 / 0 | 1020 / -300 / 0 |
| Windows ascent / descent | 1020 / 300 | 1020 / 300 |
| `A`·`a`·`x`·`g`의 윤곽 bounds | 비교한 네 글자가 동일 | 비교한 네 글자가 동일 |
| `가`의 윤곽 너비 × 높이 | 866 × 913 | 928 × 998 |
| `한`의 윤곽 너비 × 높이 | 864 × 895 | 928 × 976 |
| `가`의 Y 최소·최대 | -133 / 780 | -91 / 907 |
| 전체 11,172 한글 윤곽 너비 범위 | 695~915 | 758~970 |
| 전체 11,172 한글 윤곽 높이 범위 | 690~947 | 736~1032 |

Bold에서도 셀폭·줄 높이 메트릭과 비교한 영문 윤곽은 같았다. `가`는 현재 880 × 927, Jetendard 962 × 1020이었다. 이 값은 `cmap`, `hmtx`, `loca`, `glyf`, `hhea`, `OS/2`를 직접 읽은 측정 결과다.

Regular의 `가`는 Jetendard가 약 7.2% 넓고 9.3% 높으며, 윤곽 중심 Y가 약 84.5 UPM 단위 위에 있다. 이 예시에서 한글이 상대적으로 크고 위쪽까지 차는 현상은 확인된다. 그러나 donor 디자인 자체도 다르고 글자마다 비율도 달라, **1.15 하나가 가독성 차이를 모두 설명한다**고 결론 낼 수는 없다. 줄 높이 메트릭이 같아도 실제 에디터의 명시적 line-height와 렌더링 조건에 따라 보이는 결과는 달라질 수 있다.

## 자모와 문장부호 처리

공식 Pretendard Regular의 `cmap`에는 조합용 자모 U+1100~11FF가 없다. Jetendard는 현대 자모를 호환 자모 윤곽으로 매핑해 추가하고, `ccmp`에서 초성+중성(+종성)을 완성형 한글로 치환하는 규칙을 생성한다. 분해형 입력의 동작은 한글 완성형만 복사하는 것과 다른 구현이다. 현재 Mabyko 비교 샘플에도 `ᄀ`, `ᅡ`, `ᆨ`의 직접 cmap 항목은 없었다. 다만 앱의 Unicode 정규화나 fallback까지 평가한 결과는 아니다. [자모 매핑·`build_hangul_ccmp_features`](https://github.com/kuskhan/jetendard/blob/v0.1.0/src/jetendard/builder.py)

Jetendard의 한글/CJK 선택 범위는 완성형 한글, 자모·확장 자모, 한자, U+3000~303F, U+FF00~FFEF다. 모두 같은 두 칸 advance로 넣는 구현이다. 이를 우리 코드에 그대로 이식하기보다, 전각과 반각·결합 자모를 구분하고 실제 원본 커버리지와 현재 터미널 요구를 확인해야 한다. 원본 문장부호는 여러 폭을 가지므로 기증 범위의 폭을 각각 검증해야 한다. [`is_cjk`·`collect_cjk_codepoints`·`merge_fonts`](https://github.com/kuskhan/jetendard/blob/v0.1.0/src/jetendard/builder.py)

## 라이선스와 권고

Pretendard는 SIL OFL 1.1이며 공식 LICENSE는 `Pretendard`, `Source`, `Inter`, `M PLUS 1`을 Reserved Font Name으로 기록한다. 수정·합성·재배포는 허용되며 저작권·라이선스를 보존하고 파생 폰트에도 OFL을 유지해야 한다. Mabyko Mono처럼 별도 패밀리명으로 만드는 방식과 맞는다. Jetendard도 OFL 1.1로 배포된다. [Pretendard 공식 LICENSE](https://github.com/orioncactus/pretendard/blob/v1.3.9/LICENSE), [Jetendard LICENSE](https://github.com/kuskhan/jetendard/blob/v0.1.0/LICENSE)

Pretendard 한글 기증은 충분히 가능한 대안이다. D2Coding의 Regular/Bold 기반과 달리 9개 굵기의 donor를 대응시킬 수 있다는 이점이 있다. 먼저 같은 영문·같은 셀폭·같은 화면 조건에서 D2Coding donor, Pretendard donor, 실제 Jetendard를 비교하고, 선호가 확실해진 뒤 크기·baseline·자모·문장부호 정책을 정하는 것이 적절하다. 공식 `Pretendard Mono`로 소개하거나, 단순히 donor만 교체한 결과를 Jetendard와 동일하다고 설명하지 않아야 한다.

참고로 [CodexMono](https://github.com/monolex/codexmono)도 README에서 Pretendard 한글을 1200 고정폭으로 바꿨다고 소개한다. 이는 다른 독립 파생 프로젝트의 사례이며, 해당 폰트 바이너리나 빌드 품질까지 이번에 검증하지는 않았다.

## 대화 내 실제 비교 화면

후속 비교 화면에는 현재 구성, Fira Code + D2Coding, JetBrains Mono + Pretendard 배율 1.0 시험본, 실제 Jetendard v0.1.0을 넣었다. 각 구성의 Regular/Bold를 샘플 문자만 포함한 WOFF2로 변환했으며, 글자 크기·굵기·리거처·구성 선택을 제공한다. Pretendard 시험본은 먼저 UPM을 1000으로 맞춘 다음 기존 합성 방식으로 윤곽을 가운데 배치했다. Jetendard의 자모와 글리프별 안전영역 처리를 재현한 결과는 아니다.

현재·Fira·Pretendard 시험본 6개에서 완성형 한글 11,172자의 커버리지와 1200 advance, ASCII 600 advance, 리거처 적용 시 총 advance 보존을 확인했다. 현재와 Fira 구성의 완성형 한글 윤곽은 Regular/Bold 모두 11,172자 전체가 동일했다. 웹 화면도 728px·360px에서 오류 없이 표시됐으며, 네 구성의 16px 출력에서 영문 5자 48px·한글 6자 115.2px를 확인해 fallback 없이 같은 셀폭을 쓰는지 검사했다. 이는 비교 샘플 검증이며 전체 배포 품질 검증은 아니다. 빌드와 검증 스크립트·원본·출력은 `/tmp/mabyko-mono-font-base-prototype-20261007/`에 두었다.
