# Walking Buddy Robot v1

This is the starter code for the Walking Buddy AI Robot prototype.

## What works before hardware arrives

- Web control panel
- Safe simulated motor movement
- Voice command placeholder
- Camera test using laptop webcam or Pi camera later
- Clean project structure

## First commands on Windows

```bash
cd WalkingBuddyRobot_v1
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Important

By default, this runs in SAFE MODE. It prints movement commands instead of moving real motors.

When hardware arrives, we will update:

```text
walking_buddy/config.py
```

and switch:

```python
SAFE_MODE = False
```

Only after confirming wiring.
