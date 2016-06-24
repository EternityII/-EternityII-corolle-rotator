# EternityII-corolle_rotator.py

## Description

Génére un fichier de la corolle à la rotation voulue, suivant le fichier initial.

## Usage :

`python main.py file_path [-o output_file, -r rotation]`

- `file_path` est le chemin vers le fichier de corolle
- `-o` ou `--output` est le chemin vers le fichier généré
- `-r` ou `--rotation` est la rotation souhaitée (entre 0 et 3)

:warning: si `-o` est spécifié, alors `-r` doit l'être aussi.

:info: si `-r` n'est pas spécifié, alors il générera les 3 rotation complémentaire au fichier

Le fichier de sortie est généré dans le même répertoire que le fichier d'entré

### testé sous linux debian 8