# Emerson Rush — Mirror Demo

Byte-faithful capture of [emersonrush.com](https://www.emersonrush.com/) for demonstration purposes. This repository shows how quickly an external site can be stood up as an editable copy without touching the client's live site, DNS, or WordPress installation.

**What lives here**

- [`mirror/www.emersonrush.com/`](mirror/www.emersonrush.com/) — **first mirror.** Byte-faithful capture, no overlays.
- [`mirror-2/www.emersonrush.com/`](mirror-2/www.emersonrush.com/) — **second mirror.** Same captured pages plus a small overlay banner on the home and about-us pages, and one new page: [`mirror-2/www.emersonrush.com/expertise/`](mirror-2/www.emersonrush.com/expertise/) — an EVEglyphDesign expertise overlay covering sovereign data repository assessment, the Decision Intelligence Center of Excellence for AI safety and security, and custom-agent execution inside client DMZ environments. Overlays are flagged in-page and in the provenance ledger; the underlying capture is unchanged.
- [`mirror-3/www.emersonrush.com/`](mirror-3/www.emersonrush.com/) — **third mirror.** Same captured pages plus a small overlay banner on the home and about-us pages, and one new surface: [`mirror-3/www.emersonrush.com/lillians-guide/`](mirror-3/www.emersonrush.com/lillians-guide/) — a landing page and downloadable handbook, [*Lillian's Guide — the Sovereign practitioner canon for transformational program management in information & technology*](mirror-3/www.emersonrush.com/lillians-guide/Lillians_Guide.pdf). The PDF is watermarked, content-hashed, Key ID `EgD-KEY-2026-07`, and free to redistribute. Tampering is legible against the hash recorded in the provenance ledger; the practice it describes is not copyable, and that is the point. There is only one Lillian.
- Original first-mirror description: the site itself. Full HTML, CSS, JavaScript, images, fonts. Rendered from this directory, the pages look and behave exactly like the original because no HTML content has been rewritten. `wget --convert-links` only adjusts asset paths so the mirror works from a static host.
- [`docs/demo-landing.html`](docs/demo-landing.html) — a short explainer page that opens the mirror in an iframe alongside the live emersonrush.com so a reviewer can compare them side by side.
- [`twin/`](twin/) — analysis lane. Kept completely separate from the mirror. Nothing here is injected into or overlaid on the mirrored pages.
- [`registry/`](registry/) — provenance ledger (SHA-256 + capture timestamp of every mirrored HTML page), source ↔ path map, defect register.

**What this repository does not do**

- Does not publish under emersonrush.com or any other domain the client owns.
- Does not move DNS, does not touch GoDaddy, does not sit behind Cloudflare in this repository. Those are downstream conversations captured in [`twin/docs/hosting-and-dns-caveats.md`](twin/docs/hosting-and-dns-caveats.md).
- Does not modify the mirrored HTML. If a comparison of the mirror and the live site looks or feels different, the mirror has failed and should be re-captured.

**What the demo shows the client**

Two choices, both real:

1. Keep the current WordPress site and let a proxy layer (Cloudflare Workers, HTMLRewriter, or a similar on-the-fly editor) apply edits without touching the origin. Ownership stays with them.
2. Cut the site over to a static mirror like this one and edit the mirror in Git. Faster to change, cheaper to host, but the DNS move needs to happen and the registrar (often GoDaddy) may make that inconvenient — see the caveats note.

---

© 2026 EVEglyphDesign. Mirror is Emerson Rush copyright, captured for demonstration and comparison only.
