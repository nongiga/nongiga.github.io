# Website and CV Profile Refresh — Design

**Date:** 2026-08-02  
**Project:** Website

## Objective

Update Noga Aharony's website and academic CV to reflect confirmed 2026 fellowships and accepted presentations while keeping her research program—not her credentials—as the primary narrative.

## Editorial principles

1. Lead with research on evaluating and applying genome language models in microbial genomics and biosurveillance.
2. Include only confirmed fellowships and accepted presentations. Do not list planned submissions or conditional conferences as commitments.
3. Present Pivotal and MATS as current affiliations that support a durable research trajectory, not as the headline identity.
4. Keep the website narrative and the academic CV conventional enough for their different audiences.
5. Maintain one editable DOCX as the CV source of truth and regenerate every published PDF copy from it.

## Website structure

### Hero

Replace the current generic tagline with a concise research-first description. It should explain that Noga evaluates and applies genome language models, with emphasis on microbial genomics and biosurveillance, while retaining her Columbia Systems Biology affiliation.

Update the HTML metadata description to match this positioning and remove the current repetition.

### Profile strip

Rework the three profile cards around:

- **Research focus:** genome language model evaluation and applications in microbial genomics and biosurveillance.
- **Current affiliations:** PhD candidate at Columbia University; Pivotal Research Frontier Biodefense Fellow; MATS Autumn 2026 participant.
- **Selected recognition:** Open Philanthropy early-career funding, the Gutwirth Memorial Fellowship, and the PRI Innovative Tools and Solutions award.

The fellowship card will use explicit dates or cohort names so later maintenance is a small factual edit rather than a homepage rewrite.

### Presentations

Split the current list into two clearly labeled groups:

- **Upcoming:** only confirmed future presentations as of 2026-08-02:
  - CIBB 2026 poster, Rome, September 2–4, 2026.
  - ASM BIG 2026 oral presentation, Washington, DC, October 11–14, 2026.
- **Selected past:** retain the strongest accepted or delivered talks and posters without implying that they are upcoming.

Each upcoming entry should give the presentation title, format, conference, city, and dates. NeurIPS 2026 must not appear as an upcoming conference unless the submission is accepted.

### Existing content

Keep the publication and writing sections structurally unchanged. Apply only small consistency corrections needed to align names, statuses, and terminology with the refreshed profile.

## CV structure

Expand the CV naturally to approximately three pages while preserving familiar academic conventions.

Recommended section order:

1. Header and research profile
2. Education
3. Current fellowships and affiliations
4. Research experience
5. Publications and manuscripts
6. Posters and talks
7. Awards and funding
8. Teaching, mentorship, and scientific service
9. Skills

### CV content changes

- Rewrite the opening profile around genome language model evaluation, microbial genomics, metagenomic surveillance, and biosurveillance.
- Add the Pivotal Research Frontier Biodefense Fellowship with its confirmed 2026 dates/status.
- Add MATS Autumn 2026 with its confirmed dates/status.
- Add complete, confirmed details for CIBB 2026 and ASM BIG 2026, including dates, location, and presentation format.
- Preserve the full awards and funding history; do not replace it with only current fellowships.
- Clearly distinguish future accepted presentations from completed presentations without adding speculative commitments.

## Source-of-truth and publication flow

The updated DOCX is the canonical editable CV. The publication flow is:

1. Edit the DOCX with minimal disruption to its established visual system.
2. Render the DOCX and inspect every page for layout problems.
3. Generate the public PDF from the verified DOCX.
4. Replace both published PDF copies used by the repository.
5. Update the website CV link's cache version.
6. Verify that the site and CV use identical titles, dates, and statuses.

## Validation

- Confirm every listed fellowship is accepted and every listed upcoming presentation is confirmed.
- Compare the website and CV for exact agreement on names, dates, locations, and presentation formats.
- Render and inspect every CV page at full size for clipping, crowding, inconsistent typography, and poor page breaks.
- Preview the website locally at desktop and mobile widths.
- Check that the CV link opens the new PDF and that existing external links still work.
- Keep unrelated untracked files and existing user changes untouched.

