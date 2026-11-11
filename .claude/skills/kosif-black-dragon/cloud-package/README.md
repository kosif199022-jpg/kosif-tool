# Black Dragon: installable package (cloud + PC)

The source for `black-dragon-skill.zip`, the claude.ai skill. `CLOUD_SKILL.md` becomes the package's `SKILL.md`.
`app/` (the black-dragon engine and its 30 MB catalog) and the cartoon `vendor/` are not stored here. They are added when the zip is built.
`scripts/dragon.py where` detects cloud vs PC and routes to the local repo or the bundled engine.
