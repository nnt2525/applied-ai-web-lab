# Working on the lab

Use Node.js 20+ for the browser assets and Python 3.10+ for the reproducible models.
There are no npm or Python package dependencies to install.

1. Make a branch such as `codex/improve-ticket-evaluation`.
2. Keep generated artifacts reproducible with `python -m ml.train`.
3. Run `python -m unittest discover -s tests -v`, `npm test`, and `npm run check`.
4. Preview all three pages with `npm run dev`. Check narrow screens, keyboard
   navigation, the classifier's abstention, filters, CSV, and the demand scenario.
5. Explain the behavior changed, validation performed, and remaining limitations
   in the pull request. Do not describe synthetic results as customer impact.

For new model work, preserve a locked test set. Select features and thresholds
with training/development data. If a previously inspected test set informs an
improvement, report that fact and create a fresh independent evaluation set.

Do not commit credentials, private records, third-party datasets without rights,
student verification documents, or medical/customer data. Use clearly attributed
and appropriately licensed public data or consented deidentified data.

This starter was created with AI assistance. Review the code and build your own
experiments before presenting it in interviews; explain precisely which parts
you designed, changed, and verified.
