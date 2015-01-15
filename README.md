Shapefiles are a flat table of data (and geometries). However one often wants to represent hierachial data. County A is in Country X. One common way is to give each entry in the shapefile an id and a parentid value. The parentid points to the id in the shapefile of this objects parent. A common approach is to interpret id = parentid as meaning "this object has no parent" or "this object is the 'root node'".

This programme is used to debug and investigate such files. It assembles all the "links" and creates a tree of objects, and then prints out in the format you desire.

Copyright 2015 Rory McCann, licenced under the GNU Geneeral Public Licence version 3 or later.
