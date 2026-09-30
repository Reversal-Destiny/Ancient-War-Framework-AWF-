# Public release checklist

Use this checklist before publishing a new AWF source archive or GitHub release.

## Sensitive information

- [ ] No API keys, access tokens, passwords, private keys or `.env` files.
- [ ] No personal email addresses, account identifiers or local usernames unless deliberately public.
- [ ] No absolute local paths such as `/Users/...`, `/home/...` or `C:\\Users\\...`.
- [ ] No private server addresses, internal endpoints or unpublished repository URLs.

## Project separation

- [ ] No production behavior/resource pack copied into the framework repository.
- [ ] No project-specific models, textures, audio, structures, UI art or balance tables unless intentionally released.
- [ ] No private project code names, internal directory maps or roadmap material.
- [ ] Examples use neutral placeholder identifiers rather than identifiers from an unreleased game project.

## Third-party compliance

- [ ] `THIRD_PARTY_NOTICES.md` is present.
- [ ] Required third-party license texts remain under `licenses/`.
- [ ] Source comments identifying directly derived design/code have not been removed without a license review.

## Repository metadata

- [ ] AWF's own repository-level license has been selected and added if reuse rights are intended.
- [ ] README version/status statements match the release.
- [ ] CHANGELOG has the release entry.
- [ ] Generated archives, workspace files and caches are not committed.

## Final review

- [ ] Run a case-insensitive search for old project names, code names and private identifiers.
- [ ] Run a credential/secret scanner if available.
- [ ] Review `git diff --cached` before push.
