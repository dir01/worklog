import os

activate_this = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "./env/bin/activate_this.py"
    )
)
with open(activate_this) as f:
    exec(f.read())
