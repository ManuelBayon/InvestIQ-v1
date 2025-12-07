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

⚠️ **Attention — par défaut, l’installateur de TWS choisit le dossier `C:\Jts`.**

1. Créer un dossier `C:\TWS`
2. Lors de l’installation, sélectionner ce dossier comme destination.


![dossier installation](pictures/choix_dossier_installation.png)

---
## 4.3 Première connexion (Trading Simulé)

1. Lancer **TWS**
2. Se connecter en **Trading Simulé**  
3. Attendre que l’interface se charge complètement

![dossier installation](pictures/connexion_tws.png)

---
## 4.4. Configuration API requise

Dans TWS pour trouver les paramètres de l'API suivre les instructions suivantes :

- **Fichier** → _Configuration Générale_
- **API** → _Settings_

1. Cocher : **Enable ActiveX and Socket Clients**
2. Décocher : **Read-Only API**
3. Vérifier le port : **7497** (compte simulé)

![TWS Parametres API](pictures/tws_param_api.png)

⚠️ **Ne PAS fermer TWS**

---




# 5. Moteur d'ingestion de données
# 6. Création d’une stratégie personnalisée

Pour créer une nouvelle stratégie dans **InvestIQ-v1**, rendez-vous dans :
```powershell
./src/strategy_engine/
```

Vous y trouverez la classe abstraite `AbstractStrategy`, qui définit l’interface que toutes les stratégies doivent respecter.

Une stratégie doit **hériter** de `AbstractStrategy` et **implémenter** la méthode suivante :
```powershell
generate_signals(self, data: pd.DataFrame) -> pd.DataFrame
```

Cette méthode reçoit les données de marché (OHLC + timestamp) et doit retourner un `DataFrame` contenant au minimum :

- `timestamp`
- `close` (ou autre prix utilisé)
- `target_position` (position cible souhaitée, utilisée par le moteur FIFO)

---
## 5.1 Exemple complet pas à pas

### Étape 1 — Créer un fichier `exemple.py`

Dans :
``` powershell
./src/strategy_engine
```

Créer un fichier nommé comme vous le souhaitez, par exemple :
``` powershell
exemple.py
```

---
### Étape 2 : Créer la classe de stratégie

Voici le squelette minimal d'une stratégie :

```python
from strategy_engine.AbstractStrategy import AbstractStrategy
import pandas as pd


class MaStrategie(AbstractStrategy):

    def __init__(
        self,
        param_1: int,
        param_2: float = 0.025
    ):
        """
        Exemple d'initialisation de paramètres de stratégie.
        param_1 : entier (ex : période courte)
        param_2 : flottant (ex : seuil)
        """
        self.param_1 = param_1
        self.param_2 = param_2
```

---
### Étape 3 : Implémenter la méthode `generate_signals`

La signature **doit être strictement** : 

```python
def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
```

Et vous devez retourner un `DataFrame` contenant **au minimum** :

```python
["timestamp", "close", "target_position"]
```

> [!NOTE]
Le moteur utilise par défaut `close` pour le calcul du PnL.  
Voir ci-dessous pour changer le type de prix.

---
### Étape 3.2 : Contraintes de types imposées par le moteur de backtest

Le moteur de backtest d'InvestIQ impose des contraintes strictes sur les types des colonnes
retournées par `generate_signals()`. Ces contraintes sont nécessaires pour :

- garantir la cohérence des opérations FIFO
- assurer la stabilité des filtres de risques appliqués dans le chapitre suivant
- éviter toute ambiguïté numérique lors du calcul du PnL

Chaque ligne du DataFrame retourné doit respecter les contraintes suivantes :
#### • `timestamp : datetime64[ns]`

Représente l’instant associé à la ligne. 

Le moteur suppose un timestamp :
- trié de manière strictement croissante,
- sans valeur manquante,
- de type `datetime64` et non un objet Python.

#### • `close : float`

Le prix utilisé pour le calcul du PnL doit être un `float` (`float64`).  
Toute autre forme (objet, string, Int64) entraînera une erreur lors du passage dans : `backtest_engine/portfolio/generate_and_apply_fifo_operations_from_signals()`

Ce champ peut porter un autre nom si vous modifiez le moteur, mais il doit impérativement
être **un flottant**.

#### • `target_position : float`

Même si les valeurs usuelles sont `-1`, `0` et `+1`, le moteur attend un **float**.  

Cela garantit :
- la compatibilité avec les filtres de risques (seuils, normalisation, clipping),
- l’extensibilité vers des stratégies fractionnaires,
- une cohérence mathématique dans tout le pipeline.

Toute valeur non numérique ou typée en entier Python peut provoquer :
- un comportement incohérent,
- une incompatibilité avec certains filtres,
- une erreur dans le FIFO.

---

En résumé, le DataFrame final doit être parfaitement « numériquement formé » avant de
passer dans les modules de risques et dans le moteur d’exécution.

---
### Étape 3.3 (optionnelle) : Modifier le type de prix utilisé pour le PnL

Pour utiliser `open`, `high`, `low` ou tout autre prix :

1. Aller dans :
``` powershell
./src/backtest_engine/portfolio/portfolio.py
```

2. Trouver la méthode `generate_and_apply_fifo_operations_from_signals`

3. Modifier :

```python
price = row.close
```

en : 
``` python
price = row.open  # ou row.high / row.low
```

---
### Étape 4 : Exemple final : stratégie `BollingerMeanReversion`

Objectif :  
- Acheter quand le prix touche la bande basse.  
-  Vendre quand il touche la bande haute.  
-  Rester neutre au milieu.

```python
from strategy_engine.AbstractStrategy import AbstractStrategy
import pandas as pd


class BollingerMeanReversionStrategy(AbstractStrategy):

    def __init__(
        self,
        window: int = 20,
        num_std: float = 2.0
    ):
        """
        Stratégie de retour à la moyenne basée sur les bandes de Bollinger.
        - window  : taille de la fenêtre mobile
        - num_std : nombre d'écarts-types pour les bandes
        """
        self.window = window
        self.num_std = num_std

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Bande centrale : moyenne mobile
        df["middle"] = df["close"].rolling(self.window).mean()

        # Écart-type
        df["std"] = df["close"].rolling(self.window).std()

        # Bandes de Bollinger
        df["upper"] = df["middle"] + self.num_std * df["std"]
        df["lower"] = df["middle"] - self.num_std * df["std"]

        # Initialisation de la position cible
        df["target_position"] = 0

        # Règles :
        df.loc[df["close"] < df["lower"], "target_position"] = +1   # acheter
        df.loc[df["close"] > df["upper"], "target_position"] = -1   # vendre

        # Retour au format attendu
        return df[["timestamp", "close", "target_position"]]
```


# 7. Fonctionnement des modules de risques (Risk Filters)

Dans InvestIQ-v1, une stratégie ne produit **pas directement** les signaux consommés par le moteur de backtest.  
Elle produit un signal **brut** (`raw_target`), puis un ensemble de **filtres de risques** transforme ces signaux en signaux **finalisés** (`target_position`) avant l’exécution.

Le schéma est le suivant :
``` powershell
Strategy.generate_raw_signals()    →    Risk Filters    →   Backtest Engine
      (raw_target)                      (target_position)
```

Ce pipeline est orchestré par la classe `StrategyOrchestrator`.

---

## 6.1 Le rôle de l'Orchestrateur (`StrategyOrchestrator`)

``` python
class StrategyOrchestrator:  
  
    def __init__(self, strategy: AbstractStrategy):  
        self.strategy: AbstractStrategy = strategy  
        self.filters: list[BaseFilter] = []  
  
    def add_filter(self, filter_: BaseFilter):  
        self.filters.append(filter_)  
  
    def run(self, data: pd.DataFrame) -> pd.DataFrame:  
  
        df = self.strategy.generate_raw_signals(data)  
  
        for f in self.filters:  
            df = f.apply_filter(df)  
  
        df["timestamp"] = df["date"]  
        return df[["timestamp", "close", "target_position"]]
```

L’orchestrateur :

1. **Demande à la stratégie de produire le signal brut** via `generate_raw_signals()`.
2. **Applique séquentiellement les filtres de risques**, dans l’ordre où ils ont été ajoutés.  
    Chaque filtre agit sur le DataFrame et renvoie un DataFrame transformé.
3. **Construit le signal final** (`target_position`) qui sera envoyé :
    - au moteur d’exécution FIFO,
    - puis au moteur de PnL / portfolio.

L'utilisateur n’a donc qu’à :
- créer une stratégie (ou en choisir une existante),
- ajouter un ou plusieurs filtres,
- passer l’orchestrateur final au moteur de backtest.

---
## 6.2 Logique de base : `raw_signals` -> `filtered_signals`

### Le signal brut : `raw_target`

Dans ta stratégie :
``` python
df["raw_target"] = 0
df.loc[df["close"] < df["lower"], "raw_target"] = +1
df.loc[df["close"] > df["upper"], "raw_target"] = -1
```

C’est un signal **théorique** :
- il réagit instantanément aux conditions de marché,
- il ne représente **pas une position exécutable**,
- il ne tient pas compte :
    - du stop-loss,
    - du take-profit,
    - des contraintes opérationnelles,
    - d’un cooldown,
    - ni d'aucun autre filtre.

Le signal brut **doit être filtré** avant d'être exécuté.

---
## 6.3 Les modules de risques : filtres autonomes et chaînables

Chaque filtre hérite de :
```python
class BaseFilter(ABC):
@abstractmethod
def apply_filter(self, data: pd.DataFrame) -> pd.DataFrame:
	...
```

Un filtre :
- **prend un DataFrame en entrée**,
- **renvoie un DataFrame en sortie**,
- ne modifie jamais la structure fondamentale (`timestamp`, `close`, `raw_target`, `target_position`).

Les filtres sont **empilables** :
```python
orchestrator.add_filter(StopTakeFilter(...))
orchestrator.add_filter(AnotherFilter(...))
```

---
## 6.4 Exemple détaillé : `StopTakeFilter` (Stop-Loss + Take-Profit + Cooldown)

Ce filtre illustre parfaitement comment les modules de risques transforment un signal brut en signal tradable.

---
### 6.4.1 Idée

`StopTakeFilter` applique une logique opérationnelle sur une séquence de signaux :
- entrée en position lorsque `raw_target ≠ 0`
- maintien de la position tant que SL/TP ne sont pas atteints
- sortie lorsque :
    - take-profit atteint,
    - ou stop-loss atteint
- cooldown empêchant de reprendre immédiatement une position

---
### 6.4.2 Fonctionnement interne

Le filtre parcourt la série chronologique ligne par ligne :
#### Variables internes :
- `current_position` : position courante (+1, 0, −1)
- `entry_price` : prix auquel la position a été ouverte
- `cooldown_rem` : nombre d'unités de temps restantes avant de pouvoir rouvrir une position

### Logique par étape :

1. **Cooldown actif**

```python
if cooldown_rem > 0:
    cooldown_rem -= 1
    current_position = 0
```

Empêche la stratégie d’ouvrir une position pendant une période définie.

---

2. **Si pas en position, suivre le signal brut**

```python
if current_position == 0 and raw != 0:
    current_position = raw
    entry_price = price
```

L’entrée en position se fait uniquement si le signal brut demande à entrer.

---

3. **Si en position, surveiller SL/TP**

```python
pnl_pct = (price - entry_price) / entry_price
dir_pnl = pnl_pct if current_position > 0 else -pnl_pct

if dir_pnl >= self.tp_pct:
    current_position = 0
    cooldown_rem = self.cooldown
elif dir_pnl <= -self.sl_pct:
    current_position = 0
    cooldown_rem = self.cooldown
```

À la sortie, on impose un cooldown.

---
4. **Production du signal final (filtré) : `target_position`**

```python
df.at[i, "target_position"] = current_position
```

C’est **ce signal** que le moteur de backtest consommera.

---
## 6.5 Résultat final du pipeline

Le rôle des filtres est maintenant clair :

| Étape           | Colonne           | Signification                          |
| --------------- | ----------------- | -------------------------------------- |
| Stratégie       | `raw_target`      | Signal théorique basé sur indicateurs  |
| Filtres         | `target_position` | Signal réellement tradable             |
| Backtest engine | Exécution FIFO    | Construction des entrées/sorties & PnL |
L’utilisateur :
1. **ne gère que la logique stratégique → `raw_target`**
2. **choisit / créé les filtres qu’il souhaite → stop-loss, take-profit, etc.**
3. **laisse l’orchestrateur construire un signal propre pour le moteur**

# 8. Le moteur de backtest

# 9. Le portefeuille
# 10. Le moteur d'export en Excel
# 11. Démarrage rapide (Quick Start)

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

Logs console : 

![Exemple logs console](pictures/exemple_logs_console.png)

Résultats Excel des positions prises en fonction de la stratégie et de la configuration du moteur :

![exemple_logs_excel](pictures/exemple_logs_excel.png)

---

# 12. Licence / disclaimers

- Ce projet est fourni à des fins éducatives. 
- Aucune garantie n’est donnée pour l’utilisation en trading réel.