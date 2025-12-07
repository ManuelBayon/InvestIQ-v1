# États

- FLAT
- LONG
- SHORT
# Variables internes

```python
class (str, Enum):
ACTIVE = "ACTIVE"
TRIGGERED = "TRIGDERED"

@dataclass(frozen=true)
class StaticStopLoss:
price : float
quantity : float
state : StopLossState
```

```python
stop_loss : list[StaticStopLoss]
cooldown_remaining : int
```
# Transitions

## 1. Flat -> Long

1. Si coodown remaining > 0 aller à l'itération suivante
2. Ajout dun stop loss dans la collection de stop-loss (prix, quantité, état = ACTIVE) et dans la colonne du DataFrame. 
3. Ecriture target_position = raw_position
