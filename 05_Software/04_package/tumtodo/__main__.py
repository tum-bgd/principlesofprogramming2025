### either use fire
### or keep it simple

import sys

if (sys.argv[1] == "serve"):
    print("here I could run a flask app")
if (sys.argv[1] == "fire"):
    import fire
    fire.Fire()
