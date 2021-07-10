conda env:
conda env create -f environment.yml

export:
conda env export > environment.yml

flask run