# urbanair_demo
Jupyter notebook example for UrbanAir NWP data

## Install

To install the demo e.g. locally do, in this case with micromamba,

```
micromamba create -n urbanair_demo python=3.10 
micromamba activate urbanair_demo
pip install wget notebook xarray matplotlib cartopy warnings cfgrib cftime 
```
Now you can open the example demo by
```
jupyer notebook ./documentation_antwerp.ipynb
```
This will open the demo in your browser
