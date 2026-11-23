# dados/clean

Um CSV por vaca (T01 a T10), gerado por `clean.ipynb` a partir de `dados/raw` (sensor `immu` + `behavior_labels`), apenas do dia 25/07.

Cada linha é uma janela de 10 s.

| Coluna | Descrição |
|---|---|
| `janela` | `timestamp // 10`, identifica a janela |
| `timestamp` | primeiro timestamp (unix) da janela |
| `x_*`, `y_*`, `z_*` | aceleração (m/s²) por eixo: `mean`, `std`, `min`, `max` |
| `mag_*` | magnitude da aceleração triaxial: `mean`, `std`, `min`, `max` |
| `behavior` | comportamento mais frequente na janela (4, 5, 6 → 3; 1 → 2; classe 0 removida) |
| `vaca_id` | T01 a T10 |
