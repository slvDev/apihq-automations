# apihq automations

Importable automation workflows built on [apihq](https://apihq.dev)'s
pay-per-result data actors for YouTube and Google Play. Every workflow
ships with the failure branch pre-wired: an invalid or unavailable input
becomes a typed `success: false` row on the false branch — billed $0.0000 —
and the run keeps going.

## What's here

| Workflow | Tool | What it does |
| --- | --- | --- |
| [`n8n/youtube-transcripts.n8n.json`](n8n/youtube-transcripts.n8n.json) | n8n | Video IDs → one item per video with the transcript joined to plain text |
| [`n8n/youtube-channel-transcripts.n8n.json`](n8n/youtube-channel-transcripts.n8n.json) | n8n | Channel URL/@handle → every video's transcript as plain text (channel + transcript actors chained) |
| [`n8n/youtube-search-transcripts.n8n.json`](n8n/youtube-search-transcripts.n8n.json) | n8n | Keyword → transcripts of its top-ranking videos (search + transcript actors chained) |
| [`n8n/play-reviews-monitor.n8n.json`](n8n/play-reviews-monitor.n8n.json) | n8n | Daily pull of an app's newest Google Play reviews, one item per review |
| [`n8n/play-review-alerts.n8n.json`](n8n/play-review-alerts.n8n.json) | n8n | Daily Slack alerts for 1–2 star Google Play reviews, deduped across runs (at-least-once: the first active run covers the current backlog, and a failed run can repeat alerts) |
| [`n8n/youtube-comments.n8n.json`](n8n/youtube-comments.n8n.json) | n8n | One video → one item per comment (author, text) |
| [`make/youtube-transcripts.make.json`](make/youtube-transcripts.make.json) | Make | Video IDs → one bundle per video, transcript and failure rows on separate filtered routes |
| [`make/play-reviews-monitor.make.json`](make/play-reviews-monitor.make.json) | Make | An app's newest Google Play reviews, one bundle per review (schedule the scenario for a daily snapshot) |
| [`make/youtube-comments.make.json`](make/youtube-comments.make.json) | Make | One video → one bundle per comment (author, text, likes) |
| [`github-actions/youtube-transcripts.yml`](github-actions/youtube-transcripts.yml) | GitHub Actions | Manual dispatch: video IDs in, dataset artifact + delivered/failed job summary out |
| [`github-actions/play-reviews-history.yml`](github-actions/play-reviews-history.yml) | GitHub Actions | Daily git-scraping: an app's newest reviews committed to your repo as dated JSON — diffable history |
| [`github-actions/youtube-comments.yml`](github-actions/youtube-comments.yml) | GitHub Actions | Manual dispatch: one video's comments as a dataset artifact |

## How to use (n8n)

1. Open a workflow file from the table above (a star helps other
   builders find these).
2. Click **Raw** and copy the URL.
3. In n8n: **Workflow → Import from URL**, paste it.
4. Open the HTTP Request node and replace `YOUR_APIFY_TOKEN` with your
   token (Apify Console → Settings → API tokens — the free tier works).
   The chained workflows have two actor nodes — replace the token in
   both. The Slack alert workflow additionally needs your incoming
   webhook URL in its last node.
5. Put your own inputs in the request body and run. Successes and typed
   failures exit on separate branches; wire the last nodes to wherever
   your data lives.
6. For the scheduled workflows (review monitor and review alerts):
   **save and publish (activate)** the workflow. The Schedule Trigger
   only fires while the workflow is active, and the alert workflow's
   dedup memory only persists on the active workflow.

## How to use (Make)

1. Open a blueprint file from the table above, click **Raw**, and save
   the file (Make imports blueprints from a file, not a URL).
2. In the Make scenario editor: **⋯ (More) → Import Blueprint**, pick
   the saved file.
3. Open the HTTP module and replace `YOUR_APIFY_TOKEN`; put your own
   inputs in the request body.
4. Run once to check the routes, then set the scenario schedule if the
   job is recurring (the daily review snapshot, for example).

## How to use (GitHub Actions)

1. Copy a workflow file from `github-actions/` into your repository's
   `.github/workflows/` directory.
2. Add an `APIFY_TOKEN` repository secret (repo Settings → Secrets and
   variables → Actions).
3. For the reviews-history workflow, set `APP_ID` in the file's `env`
   block; it commits dated snapshots to your repo, so it needs the
   `contents: write` permission it already declares.
4. Run from the Actions tab (workflow_dispatch), or let the schedule
   fire. The job summary shows delivered vs failed counts; failure rows
   are typed `success: false` records and cost $0.

## Billing

The actors run on your own Apify account and bill per delivered result —
a transcript, a review, a comment. Failed items return as typed rows and
are not billed. Prices and per-actor docs: [apihq.dev/actors](https://apihq.dev/actors?utm_source=github&utm_medium=readme&utm_campaign=automations)

- [YouTube Transcript Scraper](https://apify.com/apihq/youtube-transcript-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $3.00 / 1,000 transcripts
- [YouTube Channel Scraper](https://apify.com/apihq/youtube-channel-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $0.50 / 1,000 videos
- [YouTube Search Scraper](https://apify.com/apihq/youtube-search-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $0.20 / 1,000 results
- [Google Play Reviews Scraper](https://apify.com/apihq/google-play-reviews-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $0.08 / 1,000 reviews
- [YouTube Comments Scraper](https://apify.com/apihq/youtube-comments-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $0.40 / 1,000 comments

## Support

Open an issue here or on the actor's Issues tab in the Apify Console, and
include the `request_id` from any error row. Error-code reference:
[apihq.dev/docs/errors](https://apihq.dev/docs/errors)

## License

MIT
