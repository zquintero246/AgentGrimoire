# calculate

Evaluate an arithmetic expression safely — the classic calculator tool
for models that shouldn't do arithmetic in their heads.

- **Input**: `expression` (string), e.g. `"(2 + 3) * sqrt(16)"`
- **Output**: `int | float`
- **Side effects**: none. Deterministic. Stdlib only.
- **Safety**: not `eval()`. AST-whitelisted: numbers, `+ - * / // % **`,
  parentheses, unary minus, constants `pi`/`e`, functions
  `abs round min max sqrt`. Exponents bounded (`|exp| <= 128`,
  `|base| <= 1e9`). Everything else raises `ValueError` naming the
  offending fragment, so agents can self-correct.

## Example

```python
from spell import calculate

calculate("(2 + 3) * sqrt(16)")   # 20.0
calculate("2**10 % 7")            # 2
```
