# GitHub Actions — verifica schedulazione Azure

Il raccoglitore Azure mantiene la frequenza di **30 minuti**, con trigger `schedule` ai minuti **13 e 43 di ogni ora (UTC)**, oltre all'avvio manuale e ai push di codice su `main`.

## Motivazione del cambio
Il 13 novembre 2026 il workflow ha completato diverse esecuzioni `push`/`workflow_dispatch`, ma nelle verifiche non risultavano run con `event=schedule`. Il cron originale (`17,47 * * * *`) è sintatticamente valido; la sua modifica tenta di ri-registrare la pianificazione e aggiornare l'actor secondo le indicazioni GitHub. **La modifica non prova da sola che le esecuzioni programmate siano state ripristinate.**

## Verifica
1. Aprire https://github.com/jeckodevelopment/multicloud-monitor/actions/workflows/update-azure-feed.yml
2. Dopo uno slot cron, controllare l'esistenza di una run con **Event: schedule** (non `push` o `workflow_dispatch`).
3. Verificare che la run sia `success` e che `docs/azure-feed.json` riporti un nuovo `fetched_at`.
4. Verificare che il dashboard HTML segnali l'età effettiva della fonte. Un feed RSS `ok_empty` è valido, ma non prova assenza di disservizi Azure.

GitHub non garantisce puntualità assoluta e può ritardare/scartare run schedulate. Se anche i nuovi slot non partono, verificare che il workflow sia abilitato, la registrazione dell'actor e lo stato di GitHub Actions; valutare un scheduler esterno approvato. Non dichiarare il problema risolto prima di aver osservato un evento `schedule`.

Fonte: https://docs.github.com/en/actions/how-tos/troubleshoot-workflows
