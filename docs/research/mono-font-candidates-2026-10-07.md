# Mabyko Mono 영문 베이스 후보 조사

조사일: 2026-10-07. 대상은 현재 JetBrains Mono 2.304를 바탕으로 D2Coding 한글과 Nerd Font 기호를 합성하는 Mabyko Mono의 영문 베이스다. 폰트와 빌드 설정은 변경하지 않았다.

## 결론

초기 비교 후보는 **JetBrains Mono, Fira Code, Iosevka**다. 후속 요청으로 **Cascadia Code와 Source Code Pro**를 추가해 총 다섯 후보를 검토했다. 이는 전 세계 사용률 1~3위라는 뜻이 아니다. 공개 선호 조사, 최근 사용자 의견, 공식 배포와 기능, 우리 합성 구조를 함께 고려한 후보 목록이다. 현재 모양에 특별한 불만이 없다면 JetBrains Mono를 유지하는 편이 합리적이다. 리거처의 다른 표현을 보고 싶으면 Fira Code, 폭과 글자 형태까지 직접 설계하고 싶으면 Iosevka를 비교할 만하다. 이 선택은 조사자의 판단이다.

## 사용자 선호 근거와 한계

Linux.org.ru가 2024-09-02에 연 자발적 참여 설문은 조회된 페이지 기준 534명·1,104개 선택이다. JetBrains Mono 105명(20%), Iosevka 81명(15%), FiraCode 68명(13%), Cascadia Code 24명(4%)이었다. 복수 선택이므로 점유율이 아니며, 러시아어 Linux 커뮤니티의 표본이다. 전체 1위는 Terminus 135명(25%)이고 Ubuntu Mono와 DejaVu Sans Mono도 상위에 있어, 세 후보를 설문 전체 상위 3개로 소개하면 틀린다. [설문 원문](https://www.linux.org.ru/polls/polls/17718889)

2025년에 시작해 2026년에도 댓글이 달린 VS Code 토론과 2026-04-21의 Neovim 토론에서도 이 후보들을 선호하는 사용자의 직접 의견을 볼 수 있다. 이는 최근에도 비교·사용되고 있다는 보조 근거이며, 이용자 수를 추정할 근거는 아니다. [VS Code 사용자 토론](https://www.reddit.com/r/vscode/comments/1myvi8u/what_are_the_most_popular_and_preferred_fonts_for/), [Iosevka 사용자 토론](https://www.reddit.com/r/neovim/comments/1ss4zbs/many_users_here_dont_know_about_iosevka_a_bunch/)

## 공식 배포와 관심도

아래 숫자는 조사일에 GitHub 공식 API의 `stargazers_count`, 최신 정식 release의 `tag_name`과 `published_at`을 직접 조회한 값이다. 날짜는 UTC다. 별은 누적 프로젝트 관심도의 대리 지표이고 현재 설치 수·사용률·만족도는 아니다.

| 후보 | GitHub 별 | 최신 정식 배포 | 배포일 | 근거 |
| --- | ---: | --- | --- | --- |
| JetBrains Mono | 13,063 | 2.304 | 2023-01-14 | [저장소 API](https://api.github.com/repos/JetBrains/JetBrainsMono), [릴리스](https://github.com/JetBrains/JetBrainsMono/releases/tag/v2.304) |
| Fira Code | 82,084 | 6.2 | 2021-12-06 | [저장소 API](https://api.github.com/repos/tonsky/FiraCode), [릴리스](https://github.com/tonsky/FiraCode/releases/tag/6.2) |
| Iosevka | 22,827 | 34.9.0 | 2026-09-26 | [저장소 API](https://api.github.com/repos/be5invis/Iosevka), [릴리스](https://github.com/be5invis/Iosevka/releases/tag/v34.9.0) |
| Cascadia Code | 27,914 | 2407.24 | 2024-11-27 | [저장소 API](https://api.github.com/repos/microsoft/cascadia-code), [릴리스](https://github.com/microsoft/cascadia-code/releases/tag/v2407.24) |
| Source Code Pro | 20,450 | upright 2.042 / italic 1.062 / VF 1.026 | 2023-04-12 | [저장소 API](https://api.github.com/repos/adobe-fonts/source-code-pro), [릴리스](https://github.com/adobe-fonts/source-code-pro/releases/tag/2.042R-u%2F1.062R-i%2F1.026R-vf) |

초기 조회한 네 저장소 모두 API의 `archived`는 `false`다. Fira Code의 `pushed_at`은 2026-07-28, Iosevka는 2026-10-07이었다. `pushed_at`은 저장소 활동이지 새 폰트의 배포일은 아니다. 오래된 최신 릴리스만으로 단종이나 결함을 단정할 수 없다. [Fira Code API](https://api.github.com/repos/tonsky/FiraCode), [Iosevka API](https://api.github.com/repos/be5invis/Iosevka), [JetBrains Mono API](https://api.github.com/repos/JetBrains/JetBrainsMono), [Cascadia Code API](https://api.github.com/repos/microsoft/cascadia-code)

## 세 후보의 차이

### JetBrains Mono — 현재 구성을 유지할 기준점

공식 설계는 소문자 높이를 키우면서 일반적인 문자 폭을 유지하고 `1`, `l`, `I`와 점 있는 `0`을 구분한다. 코드 리거처와 8개 굵기의 대응 이탤릭을 제공한다. JetBrains IDE에 함께 배포되는 폰트다. 우리 현재 버전인 2.304가 최신 정식 배포이므로 새 버전으로 교체할 이유는 없다. [설계·폰트 패밀리](https://www.jetbrains.com/lp/mono/), [공식 저장소](https://github.com/JetBrains/JetBrainsMono), [최신 배포](https://github.com/JetBrains/JetBrainsMono/releases/tag/v2.304)

우리에게는 기존 합성·검증 결과를 그대로 사용할 수 있다는 이점이 있다. 가독성과 글자 모양에 만족한다면 계속 기본형으로 쓰는 것이 이번 조사에서의 권고다.

### Fira Code — 리거처와 연산자 표현을 비교할 대안

정확한 이름은 **Fira Code**다. Fira Mono를 바탕으로 코드 리거처를 더한 별도 프로젝트다. 다양한 화살표·연산자 조합, 문자별 대체 모양, 스타일 세트, 콘솔 박스와 Powerline 표현을 제공한다. [공식 설명](https://github.com/tonsky/FiraCode)

공식 6.2 ZIP의 TTF 목록을 직접 확인했다. Light, Regular, Retina, Medium, SemiBold, Bold와 가변 TTF가 있으며, 별도의 이탤릭 TTF는 없다. 현재 Mabyko Mono는 기울임 없는 6개 굵기를 제공한다. Fira Code에는 Thin이 없으므로 굵기 대응을 다시 정해야 하며, 향후 실제 이탤릭을 추가하려면 별도 대안이 필요하다. [확인한 공식 ZIP](https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip)

Mabyko Mono에서는 Fira Code의 영문·숫자·리거처를 한 덩어리로 비교하는 편이 명확하다. JetBrains Mono 리거처와 조합별로 섞으면 어느 모양을 우선할지 다시 정해야 한다. 현재 변경은 수행하지 않았다.

### Iosevka — 폭과 글자 모양을 설계할 대안

공식 고정폭 패밀리는 9개 굵기, Normal/Extended의 2개 폭, Upright/Italic/Oblique의 3개 기울기를 제공한다. 스타일 세트와 문자별 변형을 선택하고 자체 빌드할 수 있다. 리거처 그룹을 개별 선택하려면 커스텀 빌드가 필요하다고 공식 README가 명시한다. [공식 설명](https://github.com/be5invis/Iosevka), [커스텀 빌드 문서](https://github.com/be5invis/Iosevka/blob/main/doc/custom-build.md)

배포판도 골라야 한다. Default에는 두 칸 폭의 일부 기호가 있고 Term은 터미널용으로 기호를 좁히며 리거처를 유지한다. Fixed는 리거처와 넓은 기호를 제거한 정확한 고정폭 변형이다. [배포 구성](https://github.com/be5invis/Iosevka/blob/main/doc/PACKAGE-LIST.md)

우리처럼 한글 두 칸 정렬과 리거처를 함께 유지하려면 Iosevka Term 또는 그 기준의 커스텀 빌드를 우선 검토할 만하다. 현재 빌드는 원본 영문을 가로로 늘이거나 줄여 600 폭에 맞춘다. 따라서 Iosevka의 좁은 원래 폭은 그대로 유지되지 않으며, 촘촘한 배치가 목적이면 한글 1200과 함께 폭 정책을 재검토해야 한다. 획의 크기·기준선·한글과의 균형도 별도로 비교해야 한다. [현재 합성 코드](../../scripts/build_regular.py) 이는 현재 합성 요구를 적용한 판단이며, 호환성을 빌드로 검증한 결과는 아니다.

## 추가 조사 후보 1: Cascadia Code / Cascadia Mono

Windows Terminal은 Cascadia Code와 Cascadia Mono를 함께 배포하고 기본값으로 **Cascadia Mono**를 사용한다. Visual Studio 2022의 기본값도 Cascadia Mono다. Code는 리거처를, Mono는 리거처 없는 구성을 제공한다. 따라서 “Cascadia Code가 기본 폰트”라고 이름을 좁혀 쓰면 부정확하다. [Windows Terminal 공식 설명](https://learn.microsoft.com/en-us/windows/terminal/cascadia-code), [Visual Studio 2022 공식 설명](https://devblogs.microsoft.com/dotnet/whats-new-for-visual-basic-in-visual-studio-2022/) Powerline/Nerd Font 변형, 200~700 가변 굵기, 기본 이탤릭과 `ss01`로 선택하는 필기체 이탤릭도 있다. Windows 터미널 사용을 중심으로 비교한다면 충분히 좋은 추가 후보다. 별 수가 Iosevka보다 많다는 사실만으로 사용률이 더 높다고 결론 낼 수는 없다. [공식 설명](https://github.com/microsoft/cascadia-code)

## 추가 조사 후보 2: Source Code Pro

Adobe가 UI와 코딩 환경을 위해 만든 고정폭 폰트다. ExtraLight, Light, Regular, Medium, Semibold, Bold, Black의 7개 굵기에 대응 이탤릭이 있다. 현재 우리의 Thin(100)은 없으므로 합성 베이스로 교체한다면 굵기 대응이 필요하다. [공식 저장소](https://github.com/adobe-fonts/source-code-pro), [Adobe 폰트 페이지](https://fonts.adobe.com/fonts/source-code-pro), [공식 CSS 굵기 구성](https://github.com/adobe-fonts/source-code-pro/blob/release/source-code-pro.css)

리거처를 강조하는 Fira Code·Cascadia Code와 달리, 문자 그대로의 코드 표현을 비교할 대안이다. 공식 최신 배포의 Regular TTF를 직접 분석했을 때 GSUB에 `calt`, `liga`, `dlig`가 없었다. 이를 “모든 OpenType 기능이 없다”로 확대하면 안 된다. 문자 변형과 숫자 관련 기능 등은 있다. 원본 UPM은 1000, 숫자 0의 advance는 600이었다. [확인한 원본 TTF](https://github.com/adobe-fonts/source-code-pro/blob/release/TTF/SourceCodePro-Regular.ttf)

2024년 시작된 Linux.org.ru 복수 선택 설문에서 Source Code Pro는 33명(6%)이었다. 2025년 Neovim 사용자 토론에도 Source Code Pro를 선호한다는 직접 의견이 있다. GitHub 별 20,450개와 이 자료는 인지도와 사용자 선호의 근거이지, 전체 개발자 사용률을 산정한 결과는 아니다. [설문](https://www.linux.org.ru/polls/polls/17718889), [2025년 사용자 토론](https://www.reddit.com/r/neovim/comments/1itje9p/is_anyone_else_very_picky_about_which_monospace/)

추가 두 후보 중 실제 제품에 동봉·기본 배포되는 근거가 가장 분명한 것은 Cascadia 패밀리다. Source Code Pro는 오래 알려진 대안이자 리거처 없이 읽는 비교 기준으로 선정했다. 이는 조사자의 선택이며 세계 사용량 순위가 아니다. Fira Code보다 두 후보가 더 많이 사용된다는 비교 통계는 확보하지 못했다.

Hack도 검토했다. 공식 API 기준 별 17,366개, 최신 정식 v3.003(2018-03-06)이며 Regular/Bold/Italic/Bold Italic의 4개 스타일이다. Linux 커뮤니티의 선호 근거는 있으나 현재 6굵기를 제공하는 Mabyko Mono의 대안으로는 Source Code Pro의 굵기 구성이 더 적합하다고 판단했다. [Hack 공식 저장소](https://github.com/source-foundry/Hack), [API](https://api.github.com/repos/source-foundry/Hack), [릴리스](https://github.com/source-foundry/Hack/releases/tag/v3.003)

## 우리 작업에 대한 판단

현재 JetBrains Mono를 유지하고, 모양 비교 후 분명한 선호가 생겼을 때 Fira Code, Iosevka, Cascadia Code 또는 Source Code Pro를 별도 변형으로 실험하는 순서가 적절하다. 다른 베이스로 바꾸는 일은 영문뿐 아니라 숫자, 연산자, 리거처, 이탤릭, 한글과의 시각적 균형을 함께 바꾸는 선택이다. 이번 조사는 인기도와 기능을 확인했으며, 새 합성 폰트의 출력 품질은 검증하지 않았다.

## 후속 조사: Fira Code의 가독성과 별 수, 한국어 검색

비교 대상은 리거처가 포함된 **Fira Code**다. 기반인 Fira Mono와 구분한다. 이번 검색 범위에서는 Fira Code 6.2와 JetBrains Mono 2.304를 직접 대조해 독해 속도·오류율의 우열을 입증한 신뢰할 만한 실험을 찾지 못했다. 제작자의 가독성 설명은 설계 의도이며, GitHub 별과 검색 노출을 가독성의 측정값으로 사용할 수 없다. [Fira Code 공식 설명](https://github.com/tonsky/FiraCode), [JetBrains Mono 설계 설명](https://www.jetbrains.com/lp/mono/)

공식 Regular 파일에서 읽은 OS/2 x-height는 JetBrains Mono 550/UPM 1000(0.55em), Fira Code 1053/UPM 1950(0.54em)이다. 문자 셀 폭은 각각 0.600em, 약 0.615em이다. 소문자 높이만으로 우열을 말할 수 없고 우리 빌드는 두 원본의 영문 폭을 모두 600으로 맞추므로 원본의 폭 차이도 그대로 남지 않는다. 실제 합성 결과의 글자 모양·굵기·한글과의 균형을 비교해야 한다. [JetBrains Mono 확인한 배포](https://github.com/JetBrains/JetBrainsMono/releases/tag/v2.304), [Fira Code 확인한 배포](https://github.com/tonsky/FiraCode/releases/tag/6.2), [현재 합성 코드](../../scripts/build_regular.py)

Fira Code의 공식 0.1은 Initial release이며 공개 HTML의 날짜가 2014-11-11T19:49:44Z다. JetBrains Mono의 공식 공개 발표는 2020-01-15다. Fira Code가 약 5년 먼저 공개돼 관심을 누적할 기간이 길었다는 것은 확인되지만, 이것이 별 수 격차의 얼마를 설명하는지는 측정하지 않았다. [Fira 첫 릴리스](https://github.com/tonsky/FiraCode/releases/tag/0.1), [JetBrains 공개 발표](https://blog.jetbrains.com/blog/2020/01/15/jetbrains-mono-a-new-font-made-for-developers/)

JetBrains Mono는 2020.1부터 IntelliJ 기반 IDE에 기본으로 제공됐다. 사용자가 GitHub 저장소를 방문하거나 별을 누르지 않고도 쓰는 경로다. 따라서 IDE 기본 배포가 많은 사용과 상대적으로 적은 GitHub 별을 함께 설명할 수 있다는 것은 타당한 추론이지만, 두 폰트의 설치 수를 직접 비교한 결과는 아니다. [공식 배포 안내](https://blog.jetbrains.com/webstorm/2020/01/webstorm-2020-1-eap-1/)

한국어 검색에서도 두 폰트가 확인된다. JetBrains는 한국어 출시 소개와 WebStorm 기본 폰트 안내를 제공하며, Fira Code도 한국어 추천·설정 후기가 있다. 한국어권 검색 결과의 순서나 개인이 자주 보는 글만으로 국내 사용률이나 Fira Code의 인지도 부족을 결론 내릴 수 없다. 한국어 문서·검색어·검색 플랫폼이 노출에 영향을 줄 수 있다는 것은 가능한 설명이다. 이번에 한국 개발자의 두 폰트 사용률을 비교하는 대표성 있는 조사는 확보하지 못했다. [JetBrains 한국어 출시글](https://blog.jetbrains.com/ko/2020/01/21/jetbrains-mono-jetbrains/), [한국어 기본 폰트 안내](https://blog.jetbrains.com/ko/2020/04/14/webstorm-2020-1-ko/), [Fira Code 한국어 추천글](https://winterloop.tistory.com/7)

Fira Code가 알려지지 않은 폰트라는 해석에 반하는 실제 사용 사례도 있다. Sourcegraph의 2021년 내부 17개 작업환경 소개는 폰트를 변경한 사용자 중 Fira Code가 가장 많고 JetBrains Mono가 다음이라고 기록한다. 본문도 통계적 유의성이 없다고 명시하므로 당시의 작은 사용 사례로만 해석한다. [Sourcegraph 원문](https://sourcegraph.com/blog/workspaces-of-sourcegraph)

이번 후속 조사의 GitHub API 재조회는 HTTP 403 rate limit으로 실패했다. 별 수는 앞서 같은 조사일에 성공한 조회값을 재사용했으며, 재시도하거나 인증을 변경하지 않았다.

베이스 교체는 별 수나 검색 빈도 대신 동일한 한글·영문 샘플과 실제 사용하는 크기에서 비교해 결정하는 것을 권한다. 먼저 Regular와 Bold를 합성해 읽어 보고, Fira Code에 없는 Thin 및 NL 변형 처리를 정한 뒤 기본형을 확정하는 순서가 적절하다. 이는 작업 제안이며 Fira Code 기반 합성을 완료했다는 뜻은 아니다.
