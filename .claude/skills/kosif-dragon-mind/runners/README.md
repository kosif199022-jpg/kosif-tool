# Dragon Mind power runners

Each `fam_<family>[_<part>].py` turns method cards of one power family into real programs.
`scripts/power_run.py ARTIFACT POWER_ID TASK` runs one; `power_run.py --build` runs them all and writes
`kosif-superpowers/data/black_dragon_adapters_powers_mind.json` with only the cards that passed here.

Rules for every runner (they are what makes "executed" mean something):

1. Do the card's method for real (its `what`, `how`, `params`) on a deterministic fixture made in the work folder.
2. Return known-answer checks on the produced output, with measured and expected values.
3. Include a negative control: the same measurement on the unprocessed input must fail the criterion,
   so the check proves the method was applied (`check("negative control: ...", not criterion(input))`).
4. Return at least one non-empty output file; never write outside the work folder; finish in under 15 s.
5. A card that cannot run here (paid key, model download, GPU, macOS, a missing engine) goes in `GAPS` with the reason.
   Never register a stub, a print, or a check that is true whatever the program did.
