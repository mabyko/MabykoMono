## 변경 내용

<!-- 무엇을 바꿨는지 짧게 적어주세요. -->

## 변경 유형

Release Drafter가 릴리스 노트를 만들 수 있도록 알맞은 라벨을 붙여주세요.

- `feature` / `enhancement`: 새로운 기능
- `fix` / `bug`: 버그 수정
- `font`: glyph, metric, weight, variant 변경
- `build` / `ci`: 빌드나 자동화 변경
- `docs`: 문서 변경
- `chore` / `refactor`: 정리

## 확인

- [ ] `uv run python scripts/test_font.py`
- [ ] `uv run python scripts/test_outputs.py`
- [ ] 새 glyph 범위나 metric 정책을 바꿨다면 테스트를 추가했다.
- [ ] 새 variant를 추가했다면 `scripts/test_outputs.py`를 갱신했다.

## 스크린샷

<!-- 폰트 모양이나 VS Code wrap/selection에 영향이 있다면 스크린샷을 추가해주세요. -->
