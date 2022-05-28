import time
from . import main

Execute_time = '8:03'
Executed = False
while Executed is False:
    if Executed not in time.time():
        print('not yet')
        pass
    else:
        Executed = True
        main.TheBadjie()