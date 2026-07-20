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
