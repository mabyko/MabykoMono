# D2Coding 한글을 유지할 때의 간격과 크기

조사일: 2026-10-08 KST. 공개 프로젝트의 README, 빌드 소스와 배포 TTF, 현재 합성 샘플의 메트릭을 비교했다. 가독성 우열을 검증한 사용자 실험은 아니다.

## 권고

**JetBrains Mono + D2Coding과 현재의 영문 600 / 한글 1200을 유지한다.** 최초 후보는 윤곽의 가로·세로 5% 확대였으나, 후속 요청에서 사용자가 높이를 유지하고 싶다고 명시했다. 현재 권고 후보는 **세로 1.0배·가로 1.05배**이며 1.10배는 대조용이다. 가로 확대도 원래 글자 형태와 세로획 두께를 바꾸므로, 비교 결과가 뚜렷하지 않으면 현재 값을 유지한다. 기본 빌드 설정은 변경하지 않았다.

Jetendard의 `1.15`는 한글 윤곽을 키우는 배율이다. 영문:한글 advance 비율 `1:1.5`를 뜻하지 않는다. Jetendard도 한글 advance를 영문 두 글자 폭으로 설정한다. Pretendard를 대상으로 정한 배율이므로 D2Coding에 15%를 그대로 적용할 근거는 없다. [Jetendard v0.1.0 builder](https://github.com/kuskhan/jetendard/blob/v0.1.0/src/jetendard/builder.py)

## 먼저 구별할 값

| 값 | 의미 | 현재 합성 방식 |
| --- | --- | --- |
| advance width | 다음 글자까지 이동하는 거리, 고정폭 셀 | 영문 600, 한글 1200: 정확히 1:2 |
| outline scale | 실제 획과 글자 모양의 크기 | D2Coding 한글 윤곽 1.0배 |
| side bearing | 셀 안의 좌우 빈 공간 | 한글 advance 1000→1200, 윤곽은 X 방향 +100 이동 |
| baseline / Y offset | 글자의 수직 위치 | 현재 한글은 Y 이동 없음 |
| ascent/descent | 한 줄이 확보하는 수직 영역 | 현재 JB 기준 1020 / -300 |

현재 구현은 한글을 가로로 늘리는 방식이 아니다. `center_width()`가 `(새 폭-기존 폭)/2`만큼 수평 이동하고 새 advance를 지정한다. 한글 병합의 `merge_subset()`에서 이 함수를 사용한다. [현재 빌드 소스](../../scripts/build_regular.py)

## 비슷한 공개 합성 프로젝트

### 1. JetBrainsMonoHangul / JBD2: 현재와 같은 여백 확장

Jhyub의 JetBrainsMonoHangul은 JetBrains Mono 2.304에 D2Coding 1.3.2의 호환 자모와 완성형 한글을 붙인다. 설정의 `d2_coding_width=1000`, `jetbrains_mono_width=1200`은 D2 원래 한글 폭과 목표 한글 폭이다. 변수 이름만 보고 영문 한 글자가 1200이라고 해석하면 안 된다. [원 프로젝트 설정](https://github.com/Jhyub/JetBrainsMonoHangul/blob/master/config.py), [원 프로젝트 README](https://github.com/Jhyub/JetBrainsMonoHangul)

`add_bearing()`은 차이 200을 좌우에 100씩 더한다. 한글 윤곽 확대나 Y 이동은 없다. 후속 fork인 JBD2도 `BEARING_ADJUSTMENT=200`으로 같은 방식을 사용한다. 따라서 **윤곽을 유지하며 한글 셀만 영문의 두 칸으로 맞추는 현재 선택에는 실제 선례가 있다.** 두 저장소는 같은 계보이며 독립적인 두 설계 사례로 세지 않았다. [원본 hangulify.py](https://github.com/Jhyub/JetBrainsMonoHangul/blob/master/hangulify.py), [JBD2 hangulify.py](https://github.com/partrita/JBD2/blob/main/src/hangulify.py)

### 2. FiraD2: 합성 사례이지만 배포본은 1:2가 아니다

FiraD2는 Fira Code의 영문·합자에 D2Coding 한글을 붙인다. v1.0.2 코드는 한글 소스 EM을 1400으로 변경하고 스케일 변환을 적용한 뒤 복사한다. `ENGLISH_FONT_WIDTH=1200`은 일부 글리프를 처리하는 조건이며 최종 한글 폭을 2400으로 지정하는 코드가 아니다. [README](https://github.com/partrita/FiraD2), [v1.0.2 처리 소스](https://github.com/partrita/FiraD2/blob/v1.0.2/scripts/hangulify.py), [v1.0.2 설정](https://github.com/partrita/FiraD2/blob/v1.0.2/scripts/config.py)

실제 v1.0.2 `FiraD2-Regular.ttf`의 `head`·`cmap`·`hmtx`를 직접 읽은 값은 UPM 1950, `0/a` advance 1200, `가/한/글` advance 1959다. **샘플의 영문:한글 폭비는 1:1.6325**이며 1:2가 아니다. 이 값은 읽기 성능 측정이 아니라 해당 배포 파일의 수치다. 터미널 격자를 함께 지원할 우리 폰트의 폭을 정할 때 그대로 따라갈 사례로 삼기 어렵다. [측정한 배포 TTF](https://github.com/partrita/FiraD2/releases/download/v1.0.2/FiraD2-Regular.ttf), [릴리스](https://github.com/partrita/FiraD2/releases/tag/v1.0.2)

### 3. LythD2: 에디터판과 터미널판을 분리

LythD2는 Lyth Mono와 D2Coding을 합성한다. 기본판은 한글 문장이 덜 벌어져 보이도록 폭비 1:1.655, Mono판은 터미널용 1:2를 설정한다. 윤곽 배율과 여백은 advance 비율과 따로 조절한다. 폭을 좁힌 판을 만드는 사례는 있지만, 이 프로젝트도 터미널판에서는 두 칸 폭을 지킨다. [README](https://github.com/wudys/LythD2), [font_settings.py](https://github.com/wudys/LythD2/blob/main/scripts/font_settings.py)

실제 계산식은 `advance=round(영문폭×폭비)`, `scale=((advance-여백설정)/소스advance)×배율설정`이다. 영문 폭 설정 604를 대입하면 기본 한글 advance는 1000, Mono 한글 advance는 1208이다. 소스 한글 advance가 1000인 경우 실제 윤곽 배율은 기본 약 0.9898, Mono 약 1.01995다. 따라서 README의 Mono `0.9123`만 보고 “한글을 원본의 91.23%로 줄인다”고 설명하면 틀린다. 소스의 변환은 동일한 X/Y 배율과 수평 가운데 이동이며 Y 이동값은 0이다. [폭 설정](https://github.com/wudys/LythD2/blob/main/scripts/config.py), [계산식](https://github.com/wudys/LythD2/blob/main/scripts/font_settings.py), [윤곽 변환](https://github.com/wudys/LythD2/blob/main/scripts/hangulify.py)

## 왜 1:1.5로 바꾸지 않는가

Unicode 데이터에서 완성형 한글 U+AC00–D7A3는 East Asian Width `W`, ASCII는 `Na`다. 전통적인 터미널은 동일한 셀의 격자에서 동아시아 글자를 두 칸에 표시한다. 한글 폰트 advance만 영문의 1.5배로 바꾸어도 터미널의 커서·선택·열 계산까지 1.5칸으로 바뀌지는 않는다. 브라우저/에디터의 자연스러운 글줄과 터미널의 표시 간격이 달라질 수 있다. [Unicode 18 폭 데이터](https://www.unicode.org/Public/18.0.0/ucd/EastAsianWidth.txt), [kitty의 셀 설명](https://sw.kovidgoyal.net/kitty/text-sizing-protocol/)

UAX #11은 문자 폭 분류가 모든 현대 터미널 상황을 자동으로 해결하지 않으며 구현별 조정이 필요하다고 명시한다. 이를 “모든 문자는 Unicode 속성 하나로 폭이 결정된다”는 주장으로 확대하지 않는다. 여기서는 일반적인 완성형 한글의 두 칸 배치와 우리 폰트의 터미널 호환 목표를 근거로 1:2를 권한다. [UAX #11 §2](https://www.unicode.org/reports/tr11/#Scope)

NAVER도 D2Coding의 한글 한 글자가 영문 두 글자 폭이라 코드·표·박스 정렬을 유지한다고 설명한다. 원본의 500/1000과 현재의 600/1200은 **둘 다 1:2**다. 원본 숫자 500/1000으로 되돌리는 것은 한글 비율만 복원하는 일이 아니라 JetBrains 영문 셀까지 바꾸는 선택이다. [D2Coding 공식 README](https://github.com/naver/d2-coding-font#readme)

## 현재 합성본과 원본의 직접 비교

UPM은 모두 1000. D2Coding 1.3.3 원본 Regular와 현재 파이프라인으로 만든 임시 JB 합성본을 비교했다. 현재 합성본에는 이 비교를 위해 Nerd 아이콘을 포함하지 않았다.

| Regular `가` | advance | 윤곽 bbox `(xmin,ymin,xmax,ymax)` | 윤곽 폭 / 셀 폭 |
| --- | ---: | --- | ---: |
| D2Coding 원본 | 1000 | `(78,-133,944,780)` | 866 / 1000 = 86.6% |
| 현재 합성 | 1200 | `(178,-133,1044,780)` | 866 / 1200 = 72.2% |

두 bbox는 X 방향 +100만 차이 나며 높이·윤곽 폭은 같다. 원본보다 한글 사이가 넓게 느껴질 수 있는 이유는 셀 폭이 20% 늘었지만 글자 모양의 크기는 유지했기 때문이다. 이것은 수치에 근거한 인상 설명이며 가독성이 나빠졌다는 실험 결과는 아니다.

측정 파일:

- 원본: `/tmp/mabyko-mono-font-base-prototype-20261007/sources/D2Coding-Ver1.3.3-20260725/D2Coding/D2Coding-Ver1.3.3-20260725.ttf`
- 현재: `/tmp/mabyko-mono-font-base-prototype-20261007/out/fonts/jb/MabykoCompareJB-Regular.ttf`
- 대응하는 Bold 파일도 같은 경로에서 비교했다.

## 셀 폭을 유지한 확대 후보

임시 비교 샘플은 현재와 같은 advance 600/1200을 유지하고 한글 윤곽만 5%·10% 확대한다. 기본 배포 설정을 변경하지 않은 선호 비교 후보다. 생성 담당의 SFNT 실측 결과를 아래에 기록했다.

| Regular `가` 후보 | bbox | 윤곽 폭 | 셀 안 수평 여백 합 |
| --- | --- | ---: | ---: |
| 현재 1.0배 | `(178,-133,1044,780)` | 866 | 334 |
| 1.05배 | `(156,-140,1067,819)` | 911 | 289 |
| 1.10배 | `(135,-147,1089,858)` | 954 | 246 |

Regular/Bold의 세 배율, 총 여섯 샘플은 완성형 한글 11,172자의 advance가 모두 1200이고 ASCII는 600이다. ASCII 윤곽 및 GSUB 이름·advance는 유지됐고 모든 한글 bbox가 수평 0–1200, 수직 -300–1020 안에 들어가는 것을 확인했다. 이 검사만으로 실제 앱의 힌팅·작은 크기 렌더링·가독성까지 검증되지는 않는다. 확대는 획 두께도 함께 바꾸므로 Regular/Bold 모두 실제 쓰는 크기에서 비교해야 한다.

이 절의 가로·세로 동시 확대안은 초기 비교 결과다. 높이를 유지하겠다는 후속 제약에 맞춘 후보는 다음 절에 기록했다.

## 후속 비교: 높이와 수직 위치 유지

D2Coding 원본이 500/1000을 쓰는 것은 영문 셀 자체가 JetBrains Mono보다 좁기 때문이다. 원본 한글이 영문 두 칸에 들어가는 데 추가 여백이 필요하지 않다. 두 폰트의 UPM이 모두 1000인 확인 파일에서는 이 advance를 직접 비교할 수 있다. 500/1000으로 합성하면 JetBrains의 영문 셀도 600에서 500으로 16.7% 좁아져, 영문 배치와 일부 글리프의 셀 적합성까지 재검토해야 한다.

추가 시험본은 한글·호환 자모를 X 방향으로만 확대했다. 변환은 `x'=600+s×(x−600)`, `y'=y`이며 advance는 1200이다. 줄 높이 메트릭도 유지했다. 글자 형태의 가로 비율과 세로획 두께는 달라진다.

| Regular `가` 후보 | 윤곽 bbox | 높이 | 수평 여백 합 |
| --- | --- | ---: | ---: |
| 현재 | `(178,-133,1044,780)` | 913 | 334 |
| 가로 1.05·세로 1.0 | `(156,-133,1067,780)` | 913 | 289 |
| 가로 1.10·세로 1.0 | `(135,-133,1089,780)` | 913 | 246 |

Regular/Bold 여섯 샘플에서 완성형 한글 11,172자 각각의 Y 최소·최대가 현재와 정확히 같은지 검사했다. ASCII 윤곽·리거처 출력과 advance, 한글 1200 advance, 수직 메트릭 1020/-300/0, 수평·수직 안전범위 검사도 통과했다. 웹 비교는 728px·360px에서 실제 여섯 WOFF2가 로드되고 영문 5자 48px·한글 6자 115.2px를 쓰는지 확인했다. 실제 에디터·터미널의 힌팅과 작은 크기 품질을 검증한 배포본은 아니다.

생성 스크립트는 `/tmp/mabyko-mono-font-base-prototype-20261007/scripts/compare_d2_horizontal.py`, 검증 스크립트는 같은 폴더의 `verify_d2_horizontal.py`, TTF는 `out/fonts/d2horizontal105`와 `out/fonts/d2horizontal110`에 있다. 원래 한글 형태까지 보존하고 싶다면 현재 값을 유지하는 것이 적절하다.

## 추가 비교: 한글 가로 1.15배와 영문 500 기준

사용자 요청에 따라 두 가지 시험본을 추가로 생성했다. A는 현재 영문 600·한글 1200을 유지하면서 한글/호환 자모 윤곽의 X만 1.15배 확대한다. B는 영문을 가로 500으로 정규화하고 D2Coding 한글을 원본 1000 폭으로 병합한다. B도 UPM을 1000으로 유지하며 영문 높이를 줄이지 않는다. 두 안 모두 현재 줄 높이 메트릭을 유지한다. 채택한 기본 설정이 아니라 선호 비교용이다.

| Regular 측정 항목 | 현재 | A: 한글 가로 1.15배 | B: 영문 500 |
| --- | ---: | ---: | ---: |
| 영문 / 한글 advance | 600 / 1200 | 600 / 1200 | 500 / 1000 |
| `가` 윤곽 폭 × 높이 | 866 × 913 | 997 × 913 | 866 × 913 |
| `가` 수평 여백 합 | 334 | 203 | 134 |
| 16px 영문 5자 출력 너비 | 48px | 48px | 40px |
| 16px 한글 6자 출력 너비 | 115.2px | 115.2px | 96px |

A는 한글을 옆으로 넓히고, B는 한글 윤곽을 보존하면서 영문을 가로 약 16.7% 압축한다. B에서는 모든 일반 영문·한글 셀의 가로 길이가 A의 5/6이므로 한 줄 전체가 더 촘촘해진다. 두 안 모두 원본과 다른 가로·세로 획 균형을 갖는 글자가 생긴다.

현재·A·B의 Regular/Bold 여섯 파일에서 ASCII 600/500 advance, 한글 11,172자 1200/1000 advance, ASCII와 한글의 Y 최소·최대 유지, 줄 높이 메트릭 유지, 한글의 수평 셀 범위, 리거처 glyph 이름과 총 advance를 확인했다. B의 한글 bbox는 현재에서 X -100만 달라져 원본 D2Coding 범위로 돌아간 것도 확인했다. 웹 비교는 728px·360px에서 여섯 실제 WOFF2의 로드와 위 출력 너비를 확인했으며, 현재 구성 선택·14px·Bold·리거처 해제도 별도로 확인했다. `post.isFixedPitch=1`, `OS/2.xAvgCharWidth`와 `hhea.advanceWidthMax`를 비교용 TTF에 맞췄다.

임시 파일은 `/tmp/mabyko-mono-font-base-prototype-20261007/out/fonts/wide115/MabykoWide115-Regular.ttf`와 `/tmp/mabyko-mono-font-base-prototype-20261007/out/fonts/narrow500/MabykoNarrow500-Regular.ttf`이며 같은 폴더에 Bold도 있다. 생성과 검증 스크립트는 `scripts/compare_final_widths.py`, `scripts/verify_final_widths.py`다. 실제 에디터·터미널의 작은 크기 힌팅을 검증한 배포본은 아니다.

## 범위와 한계

비슷한 구현 세 계보를 확인했으며 이 목록은 사용량 순위가 아니다. Iosevka + D2Coding의 직접 합성 소스를 제한된 검색에서 확보하지 못했으므로 이름만 비슷한 프로젝트를 추가하지 않았다. Sarasa Gothic은 다른 CJK 기증 폰트를 쓰는 별도 계보다. 공개 저장소의 가독성 홍보 문구를 우리 폰트와의 우열 증거로 쓰지 않았다. 공개 main/master 소스는 조회일 기준이며 FiraD2와 Jetendard는 명시한 릴리스 태그/파일 기준이다.
