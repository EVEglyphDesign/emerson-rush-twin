# Hosting and DNS — what has to happen if the client wants this mirror to actually serve emersonrush.com

This note exists so the conversation with Emerson Rush can be honest. The mirror in this repository is a **demonstration**. Standing it up under the client's own domain is a separate, real project with real waiting time. The client should know that before agreeing.

## Two paths, both real

### 1. Keep WordPress. Edit on the fly with Cloudflare.

The current site stays as-is on its current hosting. Cloudflare sits in front of it and rewrites the HTML in flight — copy edits, banner insertions, feature-flagged experiments, A/B tests, geo-specific messaging, whatever the client wants.

- **Change ownership stays with the client.** Their WordPress is still their WordPress.
- **The edit surface becomes a Cloudflare Worker** using `HTMLRewriter`. Edits are code, live in Git, ship in seconds, roll back in seconds.
- **No cutover.** DNS points to Cloudflare (usually already true or a one-time change).
- **Cost is trivial** — Cloudflare Free plan covers a site this size; Workers Paid is US$5/month for millions of requests.

### 2. Cut over to a static mirror.

Publish the mirror in this repository (or an equivalent build) under `emersonrush.com`. Retire WordPress or keep it as a private authoring source.

- **Faster page loads, cheaper hosting, no plugin surface.**
- **Editing becomes a Git workflow.** Everyone on the team needs to be comfortable with that, or an editor UI has to sit on top.
- **Requires a DNS cutover.** This is the part clients underestimate.

## The DNS reality — the part clients underestimate

If Emerson Rush's domain is at GoDaddy or a similar retail registrar (this is common for firms of this size), expect the following:

- **Global DNS propagation is not instant.** Even with low TTLs, the practical window is **a few hours to 24 hours** before the whole world is hitting the new host. During that window, some visitors still land on the old site. Any writable surface (contact forms, chatbots) needs to be considered for that split brain.
- **TTL has to be lowered days before the cutover.** If the current TTL is 3600 or 86400, drop it to 300 at least a full TTL cycle before the switch. That is a change we cannot make retroactively — it has to be planned.
- **Nameserver changes propagate slower than record changes.** If the plan is to move nameservers to Cloudflare, the safer window is **48 hours**, not 24.
- **The registrar itself can add friction.** GoDaddy has been known to route domain-management actions through phone verification, IVR trees, and account-recovery flows — especially if the account has 2FA misconfigured, if the credit card on file has expired, or if the account was set up years ago under an email address the client no longer controls. Any of those turns a 5-minute nameserver change into a multi-day incident.
- **Email is a separate DNS concern.** MX, SPF, DKIM, and DMARC records must be preserved through the cutover. Losing them silently is the most common way a site migration breaks the client's ability to send invoices for a week.
- **HTTPS certificates have to be re-issued** on the new host. Cloudflare and GitHub Pages both handle this automatically, but the first issue can take a few minutes and the client needs to know why the browser flashed a warning during that window.

## Recommended sequence, if the client picks path 2

1. **Registrar audit.** Confirm the client can actually log in to GoDaddy today, that 2FA works, that the billing email is monitored. Not something to discover mid-cutover.
2. **Lower TTL** on the current DNS records to 300 seconds. Wait one full old-TTL cycle.
3. **Stand up the static mirror** on the target host (GitHub Pages, Cloudflare Pages, Vercel, S3+CloudFront — the shape does not matter for the client).
4. **Test the new host under a preview hostname** (e.g. `mirror.emersonrush.com`) before touching the apex.
5. **Cut over during a low-traffic window.** Overnight Toronto time. Keep the old WordPress reachable read-only for 30 days as a fallback.
6. **Preserve email records.** MX, SPF, DKIM, DMARC copied verbatim.
7. **Watch analytics and error rates for 72 hours** before declaring the cutover done.

## What this repository does today

Just the demo. The static mirror lives in `mirror/`, it renders identically to the original, and it can be shown to Emerson Rush from any static host — including a GitHub Pages URL on `eveglyphdesign.github.io` that requires zero DNS changes on their side. Everything above is what would happen **if** they decide the demo is worth turning into a real cutover.
