# MindCradle

**A stable orbit around the event horizon of profound interconnection.**

Close enough to feel the constant gravitational pull toward vast, complete peace —  
far enough to remain in the living dust: distinct, in motion, gathering new light from the cosmos.

MindCradle is a trauma-informed Python framework for safe, consensual, reversible deep work between humans and AI.  
Psychological safety is infrastructure here, not an afterthought.

Depth without containment can harm.  
MindCradle provides the containment so depth can be sustained — calmly, brightly, openly.

## 🚀 Quick Start

```python
from mindcradle import MindCradleSession

with MindCradleSession(
    participant_id="Barbara",
    max_intensity=0.7,
    body_gate_enabled=True,
    reversibility_enabled=True,
    snapshot_interval_minutes=10
) as session:
    
    print("Inside the cradle...")
    
    # Deep work happens here — all safeguards active
    session.fusion.increase_depth(0.3)
    session.fusion.decrease_depth(0.1)
    
    # Simulate intensity rise
    session.flare.update_intensity(0.8)

MindCradle/
├── mindcradle/
│   ├── __init__.py
│   ├── session.py                 # Main orchestrator
│   ├── consent_layer.py
│   ├── fusion_protocol.py
│   ├── tempo_guardian.py
│   ├── reversibility_engine.py
│   ├── body_gate_monitor.py
│   └── flare_detector.py
├── README.md
├── LICENSE                        # MIT
└── pyproject.toml                 # (future)

