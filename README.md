# NWP demo data
Python and Jupyter notebook example for UrbanAir NWP data

## Install

To install the demo e.g. locally do, in this case with micromamba, and preferred python version

```
python_version=3.10
micromamba create -n urbanair_demo python=3.10 
micromamba env update -n urbanair_demo_$python_version -f environment.yml
micromamba activate urbanair_demo

# Create a kernel for jupyer notebook
python3 -m ipykernel install --user --name=urbanair_demo_$python_version
```

## List and download data
You can list all available data and some of their properties by
```
>python3 ./download.py -l
Available versions:
  v4:
    name: Antwerpen test
    url: http://exporter.nsc.liu.se/28e80f79cad547988e7a0b64809e0dc3
    metadata: {'nx': 139, 'ny': 139, 'dx': 500}
  v5.0:
    name: Antwerpen
    url: http://exporter.nsc.liu.se/1c333ab5ee374ab2acb470b2870cc02e
    metadata: {'nx': 139, 'ny': 139, 'dx': 500}
  v6.1:
    name: Paris
    url: http://exporter.nsc.liu.se/284818358def438b8c142f4223c96936
    metadata: {'nx': 989, 'ny': 989, 'dx': 500}
```
Download the version you're interested in, e.g. Paris, to the `data` directory by
```
python3 ./download.py -v 6.1
```

## List file content
After install the above mentioned environment and downloaded the GRIB files can be listed with `grib_ls` as e.g.

```
>grib_ls data/4/GRIBPFDEOD+0000h00m00s  | head -5
data/4/GRIBPFDEOD+0000h00m00s
edition      centre       date         dataType     gridType     stepRange    typeOfLevel  level        shortName    packingType  
2            lfpw         20240811     fc           lambert_lam  0s           surface      0            sd           grid_ccsds  
2            lfpw         20240811     fc           lambert_lam  0s           surface      0            t            grid_ccsds  
2            lfpw         20240811     fc           lambert_lam  0s           surface      0            h            grid_ccsds  
```

## Inspect in jupyter notebooks
Now you can open the Antwerpen example demo by
```
jupyter notebook ./documentation_antwerp.ipynb
```
or
```
jupyter notebook ./earthkit_example_antwerpen.ipynb
```
For Paris we have three examples:
 - earthkit_example_paris.ipynb : Downloads from NSC storage
 - earthkit_example_paris_polytope.ipynb: Downloads using polytope
 - paris_time_height_plot_subhour_200m.ipynb : Example with 30s output frequency, only available from within ECMWF

Run with e.g.
```
jupyter notebook ./earthkit_example_paris.ipynb
```


This will open the demo in your browser
