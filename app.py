<<<<<<< HEAD
from flask import render_template
import config

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

if __name__ == "__main__":
=======
from flask import render_template
import config

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

if __name__ == "__main__":
>>>>>>> e2889fc1841252d7c44d92ac0068773bc7bfc1eb
    app.run(host="0.0.0.0", port=8000, debug=True)