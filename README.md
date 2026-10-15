# 市场研究笔记

Public static edition of the original market research journal.

GitHub Pages serves the `docs/` directory from the `main` branch. Article paths remain stable under `/research-blog/`.

## Update an approved public edition

Use only the already-approved public static build. Do not supply research PDFs, private archives, credentials, or internal source material.

```
python3 scripts/sync_public.py /path/to/public/dist --source-origin https://original-public-site.example
```

Review the diff, then commit and push the `docs/` changes. GitHub Pages redeploys automatically after a push to `main`. The exporter rewrites the original public origin and root-relative HTML links for the project URL; it does not copy repository history or private source files.

The articles are personal original research summaries, not official institutional publications or investment advice. Linked research may require the relevant institution's access permissions.
