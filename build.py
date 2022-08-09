import os
from kruz.__version__ import __version__

input("Please check __version__.py has changed..")
dir = 'dists/'
for f in os.listdir(dir): os.remove(os.path.join(dir, f))

print(f'kruz {__version__}')
ver = ["38","39","310"]
os.system(f"python38 setup.py sdist")
for v in ver:
    os.system(f"python{v} setup.py install")
    os.system(f"python{v} setup.py bdist_egg")

input("Press Enter to continue...")
input("Press double check if file is correct...")
username = "jameshoi"
password = "heGeT%;nM.PA,4n"
os.system(f'twine upload dist/* -u {username} -p {password}')