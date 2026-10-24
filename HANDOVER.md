# HANDOVER

KindPath Collective public website. This note is for the next worker.

## What changed

The home page now states the public mission and the four service lines. Shared colours are yellow `#F7BC0D` and navy `#154A73`. The only artwork is `assets/kindpath-logo.png`. It was not redrawn, recolored, or replaced. On the navy footer it sits on a white plate so the existing navy wordmark and yellow sun stay visible.

The services page lists the same four lines. The previous offers (goal and action planning, hands-on daily support, community and connection) are no longer on the site, so the two pages do not contradict each other.

## Build

A clean environment fails with `ModuleNotFoundError: No module named 'markdown'` until the dependency is installed. `requirements.txt` pins `markdown==3.11.2`. GitHub Actions installs from that file, then runs `python build.py`.

```bash
pip install -r requirements.txt
python build.py
python -m http.server 8090
```

Edit copy in `build.py` (`build_home`, `build_services`, and the shared page template). Edit policy text in `content/policies/*.md`. Then rebuild. Do not hand-edit generated HTML.

## What the site is allowed to say

- Mission: free, broad-spectrum advocacy and research on Bundjalung Country. Community authority before programs.
- Four service lines:
  - Free social advocacy via the Life-Field tool. No NDIS plan is needed for this advocacy (already published for that line).
  - NDIS Specialist Support Coordination.
  - KindPath Succession: mentoring for people about to leave prison.
  - Social Impact Consultancy.
- Limits already on the site, and kept: not a crisis service; advocacy caseload is by referral; KindPath Collective Inc is building toward NDIS registration; supports are delivered under the founders' own sole-trader arrangements until then; research is described on the About page and this website is not recruiting participants.

## What was not added

No new logo. No "available now" badges. No outcomes, client names, or Life-Field product description. No claim that NDIS registration is complete. No street address.

## Preview and git

GitHub Pages deploys from `main` only, so this pull request has no hosted preview. Review locally with the server command above. Do not force-push. Do not merge until a person has read it. Do not commit secrets or participant data.
