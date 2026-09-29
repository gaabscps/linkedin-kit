"""Constantes compartilhadas pelos scripts do motor."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

# Os caminhos que pertencem ao motor, relativos à raiz. O /atualizar troca
# exatamente estes, e eu/ nunca está aqui.
CAMINHOS_MOTOR = ["CLAUDE.md", "README.md", ".gitignore", ".claude/skills", "motor"]
