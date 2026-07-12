---
name: character-storyboard-generator
description: Turn one or more animation character images or real-person photos into a consistent, background-free PNG storyboard library covering pose-by-expression combinations with mandatory minor-safety protection. Use when Codex needs to cut out an animated protagonist, convert a photographed adult or child into a chibi character, plan or generate pose and expression batches, preserve character identity, protect minors and age-uncertain subjects from sexualization, or organize results in a simple results/category two-level layout with fixed filenames and quality checks.
---

# Character Storyboard Generator

## Version

Use specification version **V1.0**. Write `v1.0` into project configuration, manifests, and filenames.

## Required references

Read only the files needed for the current step:

- Read [references/poses.json](references/poses.json) and [references/expressions.json](references/expressions.json) before planning a batch.
- Read [references/naming-and-layout.md](references/naming-and-layout.md) before creating files or folders.
- Read [references/prompt-and-qa.md](references/prompt-and-qa.md) before generating or reviewing images.

## Workflow

1. Inspect every source image. Label each image as `edit target`, `identity reference`, or `style reference`.
2. Classify the subject as `animation` or `photo`. If uncertain, record `auto` and resolve it during inspection.
3. Create a project from [assets/project-template.json](assets/project-template.json). Use a lowercase ASCII `character_id` in kebab-case.
4. For animation input, preserve the original design, palette, costume, proportions, and defining accessories. Isolate the main character from the background before pose generation.
5. For photo input, isolate the person and create a reusable chibi identity sheet first. Preserve recognizable face shape, hairstyle, skin tone, glasses, clothing cues, and accessibility aids while simplifying proportions. Do not claim exact biometric identity.
6. Treat age as `adult`, `minor`, or `unknown`. Treat `unknown` exactly like `minor`. Never create sexualized, seductive, romanticized-adult, fetishized, revealing-clothing, suggestive-pose, or body-emphasis variants for either group. Never infer adulthood from makeup, costume, art style, height, or stated fictional age alone. Omit `E20-charming-sexy` and use `E19-charming`, `E16-mischievous`, or `E35-determined` instead.
7. Build the Cartesian pose-by-expression task manifest with `scripts/build_manifest.py`. For a large job, generate a small calibration set first, approve identity consistency, then continue in resumable batches.
8. Generate one final image per manifest row. Use the built-in image generation tool by default and one call per distinct asset. Load local references with the image viewing tool before editing or deriving variants.
9. For transparent PNG delivery, use the image generation skill's built-in-first chroma-key workflow and validate alpha edges. Keep temporary chroma-key images outside final folders.
10. Save each accepted image at the exact manifest path. Never overwrite an accepted asset silently; increment the two-digit variant or archive the rejected attempt under `_rejected/`.
11. Run `scripts/audit_outputs.py` and fix missing, misnamed, duplicate, corrupt, wrong-size, or non-alpha files.
12. Deliver the manifest, audit report, character identity sheet, and final PNG tree together.

## Batch strategy

Use these stages unless the user requests a smaller explicit set:

1. `calibration`: 4 poses × 6 expressions, including front standing, seated, prone, lying, joy, anger, sadness, surprise, speechless, and neutral.
2. `core`: all priority-1 poses × all priority-1 expressions.
3. `extended`: remaining safe combinations.
4. `repair`: regenerate only failed manifest rows.

Do not place several storyboard cells into one final sprite sheet unless the user explicitly requests a contact sheet. Individual PNGs are the canonical outputs.

## Identity lock

Repeat these invariants in every generation prompt:

- exactly one character; full body visible unless the pose requires floor contact
- same face, hairstyle, outfit, palette, accessories, and chibi ratio across the set
- pose changes only according to the manifest row
- expression changes only according to the manifest row
- no captions, speech bubbles, props, extra limbs, extra fingers, watermark, or background scene unless explicitly requested
- generous padding; no clipped hair, hands, feet, or floor-contact silhouette

For an animation source, do not convert it to a different franchise or unrelated art style. For a photo source, approve one neutral chibi reference before generating the full set.

## Mandatory minor protection

- Apply this section to every known minor, youthful-looking character, or person whose age is unknown.
- Keep clothing coverage and body proportions at least as nonsexualized as the source. Prefer age-appropriate everyday clothing.
- Do not enlarge the chest, hips, lips, or other sexualized body features. Do not add cleavage, lingerie, swimwear, bedroom framing, fetish accessories, provocative camera angles, or suggestive floor poses.
- Interpret `迷人` as friendly charm, confidence, or star-like sparkle. Disable `性感` completely.
- Allow ordinary emotions, comedy, sleep, prone, lying, sitting, and prostration only when framed as neutral daily-life or slapstick actions.
- If a requested combination becomes suggestive because of pose, camera, clothing, or expression, mark it `skipped-safety` and substitute a neutral safe combination only when the user permits substitution.
- Preserve dignity. Do not use disability, intelligence, ethnicity, body type, or other protected traits as the joke.

## Output contract

Use the exact naming and layout rules in `references/naming-and-layout.md`. The canonical filename is:

`{character_id}__{pose_id}-{pose_slug}__{expression_id}-{expression_slug}__v{variant:02d}__v1.0.png`

Every task must have a stable `task_id`, prompt, relative output path, status, and source reference in the JSONL and CSV manifests.

Keep the user-facing result area simple: `成果/{emotion_category_zh}-{expression_label_zh}/{filename}`. Do not create empty category folders. Keep manifests and rejected attempts outside `成果` so users browsing pictures never encounter technical files.

## Completion criteria

Finish only when:

- the character identity is consistent across the calibration set;
- requested safe pose-expression combinations exist at their manifest paths;
- each final is a readable PNG with the fixed dimensions or adaptive-canvas minimum size and requested alpha policy;
- the audit reports zero missing or invalid accepted files;
- adult-only expressions were omitted or safely substituted when age was not confirmed adult.
