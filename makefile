# =========================================================
# VARIABLES
# =========================================================

PYTHON = python
# 👉 interpréteur Python utilisé (modifiable si besoin)

PROJECT = .
# 👉 racine du projet (utile si monorepo futur)


# =========================================================
# INSTALLATION
# =========================================================
install:
	@echo "📦 Installation des dépendances avec uv..."
	uv sync
# 👉 installe toutes les dépendances définies dans pyproject.toml
# 👉 garantit un environnement reproductible


# =========================================================
# FORMAT CODE (STYLE AUTOMATIQUE)
# =========================================================
format:
	@echo "✨ Formatage du code avec Ruff..."
	ruff format $(PROJECT)
# 👉 applique formatage automatique (style, indent, guillemets)
# 👉 ne modifie pas la logique métier


# =========================================================
# LINT (QUALITÉ CODE + BUGS)
# =========================================================
lint:
	@echo "🧹 Analyse qualité du code avec Ruff..."
	ruff check $(PROJECT)
# 👉 détecte :
#    - erreurs de style
#    - imports mal organisés
#    - bugs potentiels
#    - mauvaises pratiques


# =========================================================
# TYPE CHECKING (MYPY)
# =========================================================
type:
	@echo "🧠 Vérification des types avec MyPy..."
	mypy $(PROJECT)
# 👉 vérifie cohérence des types Python
# 👉 détecte bugs logiques invisibles à l'exécution


# =========================================================
# TESTS UNITAIRES
# =========================================================
test:
	@echo "🧪 Exécution des tests..."
	pytest
# 👉 exécute tous les tests unitaires du projet


# =========================================================
# COVERAGE (QUALITÉ DES TESTS)
# =========================================================
cov:
	@echo "📊 Analyse de couverture des tests..."
	pytest --cov=$(PROJECT) --cov-report=term-missing
# 👉 affiche :
#    - % de code testé
#    - lignes non couvertes
# 👉 permet de détecter zones non testées


# =========================================================
# PIPELINE LOCAL (QUALITÉ COMPLÈTE)
# =========================================================
check: lint type test
# 👉 exécute :
#    1. lint (qualité code)
#    2. type (types)
#    3. test (tests unitaires)
#
# 👉 utilisé avant commit pour valider le code


# =========================================================
# PIPELINE CI (SIMULATION PRODUCTION)
# =========================================================
ci: lint type test cov
# 👉 pipeline complet identique à la CI/CD
# 👉 garantit que le code est prêt pour production


# =========================================================
# CLEAN (NETTOYAGE ENV LOCAL)
# =========================================================
clean:
	@echo "🧼 Nettoyage des caches..."
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
# 👉 supprime tous les fichiers temporaires Python
# 👉 utile en cas de bugs de cache


# =========================================================
# HELP (OPTIONNEL MAIS PRO)
# =========================================================
help:
	@echo "📌 COMMANDES DISPONIBLES :"
	@echo "  make install  → installe dépendances"
	@echo "  make format   → formate le code"
	@echo "  make lint     → analyse qualité code"
	@echo "  make type     → vérifie types"
	@echo "  make test     → lance tests"
	@echo "  make cov      → coverage tests"
	@echo "  make check    → pipeline local complet"
	@echo "  make ci       → pipeline CI complet"
	@echo "  make clean    → nettoie caches"