# urbanair_demo
Python and Jupyter notebook example for UrbanAir NWP data

## Install

To install the demo e.g. locally do, in this case with micromamba,

```
micromamba create -n urbanair_demo python=3.10 
micromamba activate urbanair_demo
pip install requests bs4 wget notebook earthkit.data earthkit.plots
```
Now you can open the v4 example demo by
```
jupyer notebook ./documentation_antwerp.ipynb
```
or the v5 example by
```
jupyer notebook ./earthkit_example.ipynb
```

This will open the demo in your browser

## Download all data
You can download all data to the `data` directory by
```
python3 ./download.py
```

## List file content
After install the above mentioned environment the GRIB files can be listed with `grib_ls` as e.g.

```
(urbanair_demo) [a000864@c22681 uademo]$ grib_ls data/GRIBPFDEOD+0001h00m00s | head -5
data/GRIBPFDEOD+0001h00m00s
edition      centre       date         dataType     gridType     stepRange    typeOfLevel  level        shortName    packingType  
2            lfpw         20240811     fc           lambert_lam  1            surface      0            sd           grid_ccsds  
2            lfpw         20240811     fc           lambert_lam  1            surface      0            t            grid_ccsds  
2            lfpw         20240811     fc           lambert_lam  1            surface      0            h            grid_ccsds  
```

