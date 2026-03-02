# NWP demo data
Documentation with Python and Jupyter notebook examples for UrbanAir NWP data. Data can be 
accessed in three ways
 * Via http URL's from nsc.liu.se. This includes all data stored as files
 * Using ECMWF's polytope API. This does not yet cover the tiled surface data
 * Using FDB directly on ECMWF's HPC. This does not yet cover the tiled surface data

The two latter enables field extractions whereas the first works with files.

## Install

To install the demo e.g. locally do, in this case with micromamba, and preferred python version

```
python_version=3.10
micromamba create -n urbanair_demo python=3.10 
micromamba env update -n urbanair_demo -f environment.yml
micromamba activate urbanair_demo

# Create a kernel for jupyer notebook
python3 -m ipykernel install --user --name=urbanair_demo
```

## List and download data
You can list all available data and some of their properties by
```
>python3 ./download.py -l
Available versions:
...
7.1:
  name: Paris 7.1
  url: http://exporter.nsc.liu.se/f1559d3fb24e47b5b9b3f77905a8bcba
  metadata:
   nx: 989
   ny: 989
   dx: 500
   date: 2023-08-20T00:00:00Z
   forecast_range: PT36H
   output_frequency: PT15M
   fdb:
    expver: aabg
    georef: u09tvk
   polytope:
    collection: deode
    url: polytope-test.ecmwf.int
 
8.0:
  name: Paris 8.0
  url: http://exporter.nsc.liu.se/aebc1d3690d441cf82818d9893fa9e57
  metadata:
   nx: 989
   ny: 989
   dx: 500
   date: 2023-08-20T00:00:00Z
   forecast_range: PT48H
   output_frequency: PT15M
   toc:
    climate_fields: http://exporter.nsc.liu.se/aebc1d3690d441cf82818d9893fa9e57/Const.Clim.grib2.toc
    surface_fields: http://exporter.nsc.liu.se/aebc1d3690d441cf82818d9893fa9e57/2023/08/20/GRIBTILEDEOD+0048h00m00s.sfx.toc
    atmospheric_fields: http://exporter.nsc.liu.se/aebc1d3690d441cf82818d9893fa9e57/2023/08/20/GRIBPFDEOD+0048h00m00s.toc
   fdb:
    expver: aad4
    georef: u09tvk
   polytope:
    collection: deode
    url: polytope-test.ecmwf.int


```
Download the version you're interested in, e.g. Paris, to the `data` directory by
```
python3 ./download.py -v 8.0
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

For each file type the listings are available in the \*.toc files listed above.

## Inspect and download in jupyter notebooks



### Paris
For Paris we have four examples valid for runs >=v7.1 
 - earthkit_example_paris.ipynb : Downloads from NSC storage
 - earthkit_example_paris_polytope.ipynb: Downloads using polytope or fdb directly on atos
 - paris_time_height_plot.ipynb : Downloads using poltype/fdb and creates a time-heigh plot
 - paris_time_height_plot_subhour_200m.ipynb : Example with 30s output frequency over a smaller domain, only available from within ECMWF

Run with e.g.
```
jupyter notebook ./earthkit_example_paris.ipynb
```

This will open the demo in your browser
