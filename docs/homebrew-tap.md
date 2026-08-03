# Mabyko Mono Homebrew tap 구축 가이드

Mabyko Mono를 `brew install`로 설치할 수 있게 하는 작업 순서.
2026-08-03 기준(v0.2.0)으로 작성했고, sha256 값은 실제 릴리스 자산에서 계산·검증한 값이다.

## 전체 구조

```
사용자: brew install mabyko/tap/font-mabyko-mono-nf
  → brew가 github.com/mabyko/homebrew-tap 저장소를 읽음 (캐스크 = 설치 레시피)
  → 캐스크에 적힌 MabykoMono 릴리스 zip 다운로드 + sha256 검증
  → ttf를 ~/Library/Fonts에 설치
```

- tap = `homebrew-` 접두사가 붙은 평범한 GitHub 공개 저장소. 등록·승인 절차 없음.
- 폰트 파일은 계속 MabykoMono 릴리스에 있고, tap은 버전·해시·URL만 기록.
- 릴리스마다 캐스크의 `version`/`sha256` 두 줄만 갱신하면 됨 (5단계에서 자동화).

## 1단계: tap 저장소 생성

```sh
gh repo create mabyko/homebrew-tap --public \
  --description "Homebrew tap for mabyko projects"
git clone git@github.com:mabyko/homebrew-tap.git
cd homebrew-tap
mkdir Casks
```

저장소 이름은 반드시 `homebrew-tap` (brew가 `mabyko/tap` → `mabyko/homebrew-tap`으로 해석).
폰트 외 다른 프로젝트도 나중에 `Casks/`(앱·폰트), `Formula/`(CLI 도구)에 추가하면 된다.

## 2단계: 캐스크 3개 작성

`Casks/font-mabyko-mono-nf.rb`:

```ruby
cask "font-mabyko-mono-nf" do
  version "0.2.0"
  sha256 "cee2ae7d8dd28ee6fd5b77479701c9f932e5085810e59729f1f83f9665f0e9fe"

  url "https://github.com/mabyko/MabykoMono/releases/download/v#{version}/MabykoMono_NF_v#{version}.zip"
  name "Mabyko Mono NF"
  desc "Korean-friendly programming font with Nerd Font symbols"
  homepage "https://github.com/mabyko/MabykoMono"

  livecheck do
    url :url
    strategy :github_latest
  end

  font "MabykoMonoNF-Thin.ttf"
  font "MabykoMonoNF-Light.ttf"
  font "MabykoMonoNF-Regular.ttf"
  font "MabykoMonoNF-Medium.ttf"
  font "MabykoMonoNF-SemiBold.ttf"
  font "MabykoMonoNF-Bold.ttf"
end
```

`Casks/font-mabyko-mono.rb`:

```ruby
cask "font-mabyko-mono" do
  version "0.2.0"
  sha256 "99cd7be908e8718e4d9cad7b7873598a02036c9b86664b64e3f27b2ead2687e5"

  url "https://github.com/mabyko/MabykoMono/releases/download/v#{version}/MabykoMono-v#{version}.zip"
  name "Mabyko Mono"
  desc "Korean-friendly programming font blending JetBrains Mono and D2Coding"
  homepage "https://github.com/mabyko/MabykoMono"

  livecheck do
    url :url
    strategy :github_latest
  end

  font "MabykoMono-Thin.ttf"
  font "MabykoMono-Light.ttf"
  font "MabykoMono-Regular.ttf"
  font "MabykoMono-Medium.ttf"
  font "MabykoMono-SemiBold.ttf"
  font "MabykoMono-Bold.ttf"
end
```

`Casks/font-mabyko-mono-nl.rb`:

```ruby
cask "font-mabyko-mono-nl" do
  version "0.2.0"
  sha256 "5bdb125ac6a9e7a802fe0837ee024770dc4198916ce572512da96ce11d85ede7"

  url "https://github.com/mabyko/MabykoMono/releases/download/v#{version}/MabykoMono_NL_v#{version}.zip"
  name "Mabyko Mono NL"
  desc "Korean-friendly programming font without ligatures"
  homepage "https://github.com/mabyko/MabykoMono"

  livecheck do
    url :url
    strategy :github_latest
  end

  font "MabykoMonoNL-Thin.ttf"
  font "MabykoMonoNL-Light.ttf"
  font "MabykoMonoNL-Regular.ttf"
  font "MabykoMonoNL-Medium.ttf"
  font "MabykoMonoNL-SemiBold.ttf"
  font "MabykoMonoNL-Bold.ttf"
end
```

주의: zip 파일명 규칙이 변형마다 다르다 (`MabykoMono-v*.zip`는 하이픈,
`MabykoMono_NF_v*.zip`/`MabykoMono_NL_v*.zip`는 언더스코어). URL 오타 나기 쉬운 지점.

커밋하고 푸시:

```sh
git add Casks && git commit -m "add Mabyko Mono casks (v0.2.0)" && git push
```

## 3단계: 로컬 테스트

**먼저 수동 설치한 폰트를 제거할 것.** 캐스크도 `~/Library/Fonts`에 설치하므로
같은 파일이 이미 있으면 설치가 충돌로 실패한다. 서체 관리자에서
Mabyko Mono 패밀리 3종을 제거한 뒤:

```sh
brew tap mabyko/tap
brew install --cask font-mabyko-mono-nf font-mabyko-mono font-mabyko-mono-nl

# 검증
brew audit --cask --online mabyko/tap/font-mabyko-mono-nf
brew style mabyko/tap
ls ~/Library/Fonts | grep Mabyko
```

이후 새 버전이 나오면 사용자는 `brew upgrade`만 하면 된다 (제거→설치 자동 처리).

## 4단계: MabykoMono README에 설치법 추가

README 설치 섹션 macOS 부분에 추가 (PR, `docs` 라벨):

```markdown
### macOS (Homebrew)

​```sh
brew install --cask mabyko/tap/font-mabyko-mono-nf   # Nerd Font symbols 포함
brew install --cask mabyko/tap/font-mabyko-mono      # 일반
brew install --cask mabyko/tap/font-mabyko-mono-nl   # ligature 제거
​```

업데이트는 `brew upgrade`로 처리됩니다.
```

## 5단계(선택): 릴리스 시 tap 자동 범프

릴리스를 게시하면 캐스크의 version/sha256을 자동 갱신하는 GitHub Actions.

### 준비: PAT 발급 (저장소 관리자만 가능)

1. https://github.com/settings/personal-access-tokens → Generate new token (fine-grained)
   - Resource owner: `mabyko` / Repository access: `mabyko/homebrew-tap`만
   - Permissions: Contents → Read and write
   - (org 드롭다운이 안 보이면 org Settings → Third-party Access에서 fine-grained PAT 허용,
     또는 classic 토큰 `repo` 스코프로 대체)
2. MabykoMono 저장소 → Settings → Secrets and variables → Actions →
   New repository secret: 이름 `TAP_GITHUB_TOKEN`, 값 = 토큰

### MabykoMono에 `.github/workflows/bump-tap.yml` 추가

```yaml
name: Bump Homebrew tap

on:
  release:
    types: [published]

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout tap
        uses: actions/checkout@v4
        with:
          repository: mabyko/homebrew-tap
          token: ${{ secrets.TAP_GITHUB_TOKEN }}

      - name: Update casks
        env:
          TAG: ${{ github.event.release.tag_name }}
        run: |
          set -euo pipefail
          VERSION="${TAG#v}"
          BASE="https://github.com/mabyko/MabykoMono/releases/download/${TAG}"
          bump() {  # bump <cask-file> <zip-name>
            sha=$(curl -sfL "${BASE}/$2" | shasum -a 256 | cut -d' ' -f1)
            sed -i -E \
              -e "s/version \"[^\"]+\"/version \"${VERSION}\"/" \
              -e "s/sha256 \"[^\"]+\"/sha256 \"${sha}\"/" \
              "Casks/$1"
          }
          bump font-mabyko-mono.rb    "MabykoMono-${TAG}.zip"
          bump font-mabyko-mono-nf.rb "MabykoMono_NF_${TAG}.zip"
          bump font-mabyko-mono-nl.rb "MabykoMono_NL_${TAG}.zip"

      - name: Commit and push
        env:
          TAG: ${{ github.event.release.tag_name }}
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git commit -am "bump Mabyko Mono casks to ${TAG}"
          git push
```

자동화 전까지는 수동 범프도 간단하다: 새 릴리스 후 tap 저장소에서
캐스크의 `version` 두 줄과 `sha256`(위 bump 함수의 curl 명령으로 계산)만 고쳐 푸시.

## 6단계(선택, 나중에): 공식 homebrew/cask 등록

폰트 사용자가 어느 정도 생기면 github.com/Homebrew/homebrew-cask 에 캐스크 추가 PR.
승인되면 `brew install font-mabyko-mono`처럼 tap 접두사 없이 설치 가능.
- 요건: 재배포 가능 라이선스(OFL 1.1 — 충족), 태그된 안정 릴리스(충족), 인지도(시간 필요)
- 등록 후에도 우리 tap은 그대로 유지 가능 (두 경로 공존)

## 체크리스트

- [ ] 1. `mabyko/homebrew-tap` 저장소 생성
- [ ] 2. 캐스크 3개 작성·푸시
- [ ] 3. 수동 설치 폰트 제거 → `brew install` 테스트 → `brew audit`/`brew style` 통과
- [ ] 4. README에 Homebrew 설치법 추가 (PR, docs 라벨)
- [ ] 5. PAT 발급·시크릿 등록 → `bump-tap.yml` 추가 (PR, build 라벨)
- [ ] 6. (다음 릴리스 때) 자동 범프 동작 확인
