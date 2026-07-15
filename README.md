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
| [`n8n/play-reviews-monitor.n8n.json`](n8n/play-reviews-monitor.n8n.json) | n8n | Daily pull of an app's newest Google Play reviews, one item per review |
| [`n8n/youtube-comments.n8n.json`](n8n/youtube-comments.n8n.json) | n8n | One video → one item per comment (author, text) |

## How to use (n8n)

1. Download a workflow file (or clone this repo).
2. In n8n: **Workflow → Import from File**.
3. Open the HTTP Request node and replace `YOUR_APIFY_TOKEN` with your
   token (Apify Console → Settings → API tokens — the free tier works).
4. Put your own inputs in the request body and run. Successes and typed
   failures exit on separate branches; wire the last nodes to wherever
   your data lives.

## Billing

The actors run on your own Apify account and bill per delivered result —
a transcript, a review, a comment. Failed items return as typed rows and
are not billed. Prices and per-actor docs: [apihq.dev/actors](https://apihq.dev/actors?utm_source=github&utm_medium=readme&utm_campaign=automations)

- [YouTube Transcript Scraper](https://apify.com/apihq/youtube-transcript-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $3.00 / 1,000 transcripts
- [Google Play Reviews Scraper](https://apify.com/apihq/google-play-reviews-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $0.08 / 1,000 reviews
- [YouTube Comments Scraper](https://apify.com/apihq/youtube-comments-scraper?utm_source=github&utm_medium=readme&utm_campaign=automations) — $0.40 / 1,000 comments

## Support

Open an issue here or on the actor's Issues tab in the Apify Console, and
include the `request_id` from any error row. Error-code reference:
[apihq.dev/docs/errors](https://apihq.dev/docs/errors)

## License

MIT
