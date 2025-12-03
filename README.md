# 1. Introduction

InvestIQ-v1 est une infrastructure modulaire de backtesting en Python, conçue pour analyser et tester des stratégies systématiques. 

La version 1 propose un moteur fonctionnel complet (data, stratégie, exécution, journalisation), prêt à être utilisé ou étendu.

# 2. Structure du code

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

# 2. Pipeline de traitement
# 3. Installation (Windows)

Ce guide permet d’installer et d’exécuter _InvestIQ-v1_ dans un environnement isolé et reproductible.

## 3.1 Cloner le dépôt

Ouvrir PowerShell puis exécuter :

``` powershell
git clone https://github.com/ManuelBayon/InvestIQ-v1.git
cd InvestIQ-v1
```

---
## 3.2 Créer un environnement virtuel

Créer un environnement dédié dans le dossier `InvestIQ-v1` :

``` powershell
python -m venv .venv
```

---
## 3.3 Activer l'environnement virtuel

``` powershell
.venv\Scripts\Activate.ps1
```

La ligne de commande doit afficher un préfixe `(.venv)`, par exemple :

``` powershell
(.venv) PS C:\Users\Manuel\Documents\...\src>
```

---
## 3.4 Installer les dépendances

``` powershell
pip install -r requirements.txt
```

---
# 4. Configuration Interactive Brokers (TWS)

Cette section explique comment installer et configurer **Trader Workstation (TWS)** pour permettre à InvestIQ-v1 de communiquer avec Interactive Brokers (en mode simulé ou réel).

## 4.1. Pourquoi une configuration TWS propre ?

TWS mélange dans le même dossier :

- les exécutables (`tws.exe`, `ibgateway.exe`)
- **les paramètres utilisateurs** (`jts.ini`, fichiers XML, caches)
- les logs

Pour éviter les conflits, assurer la reproductibilité et permettre à InvestIQ-v1 de charger une configuration propre, **il est recommandé d’installer TWS dans un dossier dédié**, différent du dossier `C:\Jts` (qui est le dossier de configuration utilisé par IB par défaut).

## 4.2 Installation de TWS (Trader WorkStation)

### Étape 1 - Télécharger TWS

Télécharger TarderWorkstation (TWS) sur le site officiel d’Interactive Brokers :

👉 https://www.interactivebrokers.ie/en/trading/trading-platforms.php

Deux versions existent :

- **TWS (recommandé)**
- **TWS Latest** (plus fréquent en mise à jour)

### Étape 2 - Créer un dossier d'installation propre

>[!warning] Par défaut l'installateur de TWS choisis le dossier **C:\Jts**.

> 1. Créer un dossier `C:\TWS`
> 2. Lors de l’installation, sélectionner ce dossier comme destination.

![[choix dossier installation.png]]

---
## 4.3 Première connexion (Trading Simulé)

1. Lancer **TWS**
2. Se connecter en **Trading Simulé**  
3. Attendre que l’interface se charge complètement

![[1 - Connexion TWS.png]]

---
## 4.4. Configuration API requise

Dans TWS pour trouver les paramètres de l'API suivre les instructions suivantes :

- **Fichier** → _Configuration Générale_
- **API** → _Settings_

1. Cocher : **Enable ActiveX and Socket Clients**
2. Décocher : **Read-Only API**
3. Vérifier le port : **7497** (compte simulé)

![[TWS Parametres API.png]]

> [!warning] Ne pas fermer TWS.

---
# 5. Démarrage rapide (Quick Start)

## 5.1 Lancement de l'application 

Aller dans  le répertoire `src` du projet `InvestIQ-v1`et exécuter la commande suivante:

``` powershell
python Main.py
```

Le moteur va :

- initialiser les moteurs (backtest, data, export),
- se connecter à Interactive Brokers (simulé ou réel selon configuration),
- exécuter la stratégie par défaut,
- produire un fichier Excel dans `InvestIQ-v1\Backtest Logs\output.xlsx` dans lequel sont répertorié l'ensemble des positions exécutés par la stratégie.
- produire un fichier de logs pour l'ensemble des moteurs du projet dans `InvestIQ-v1\Engine Logs\output.log`

## 5.2 Exemple d'utilisation

![[Exemple logs console.png]]

![[Exemple logs excel.png]]
---
# 6. Licence / disclaimers

- Ce projet est fourni à des fins éducatives. 
- Aucune garantie n’est donnée pour l’utilisation en trading réel.