# 1. Objectif du projet

InvestIQ-v1 est une infrastructure modulaire de backtesting en Python, conçue pour analyser et tester des stratégies systématiques.  
La version 1 propose un moteur fonctionnel complet (data, stratégie, exécution, journalisation), prêt à être utilisé ou étendu.

# 2. Structure du projet

``` sql
src/
│
├── backtest_engine/          # moteur de simulation
├── strategy_engine/          # interface stratégie + exemple
├── historical_data_engine/   # récup. données historiques
├── export_engine/            # export résultats / métriques
├── config/                   # fichiers de configuration
├── utilities/                # outils généraux
└── Main.py                   # point d’entrée

```

# 3. Installation & Lancement (Windows)

Ce guide permet d’installer et d’exécuter _InvestIQ-v1_ dans un environnement isolé et reproductible.

## 1. Cloner le dépôt

Ouvrir PowerShell puis exécuter :

``` powershell
git clone https://github.com/ManuelBayon/InvestIQ-v1.git
cd InvestIQ-v1
```

---
## 2. Créer un environnement virtuel

Créer un environnement dédié dans le dossier `InvestIQ-v1` :

``` powershell
python -m venv .venv
```

---
## 3. Activer l'environnement virtuel

``` powershell
.venv\Scripts\Activate.ps1
```

La ligne de commande doit afficher un préfixe `(.venv)`, par exemple :

``` powershell
(.venv) PS C:\Users\Manuel\Documents\...\src>
```

---
## 4. Installer les dépendances

``` powershell
pip install -r requirements.txt
```

---
## 5. Lancer le moteur de backtest

Aller dans `src` :
``` powershell
cd src
python Main.py
```

Le moteur va :

- initialiser les moteurs (backtest, data, export),
- se connecter à Interactive Brokers (simulé ou réel selon configuration),
- exécuter la stratégie par défaut,
- produire un fichier Excel dans `InvestIQ-v1\Backtest Logs\output.xlsx`
- produire un fichier de logs relatif à l'exécution du programme dans `InvestIQ-v1\Engine Logs\output.log`

---
## 6. Désactiver l'environnement virtuel (optionnel)

``` powershell
deactivate
```

---

# 📂 Résultat final

Après installation, l’utilisateur peut :

- tester l’architecture du moteur V1,
- analyser l’export Excel,
- modifier la stratégie ou les règles,
- intégrer InvestIQ-v1 à un workflow existant.

