library (tidyverse)

read.csv('./out/rosetta_201106.csv') -> ros
head(ros$brokenPath)

# remove ephemeral clutter at beginning of broken paths in temp. 
# Arc creates these temp dummy sdes if the version of the database is deleted after the mxd was saved. 
ros %>% mutate(
  brokenPath = gsub('^C:\\\\Users\\\\jdmumm\\\\AppData\\\\Local\\\\Temp\\\\16\\\\arc6107\\\\.{37}', '', ros$brokenPath))-> trunc

#arctic circle caused unexpected errors. bandaid for now, ultimately may want to address upstream from here. 
# trouble converting to theis source \\dfg.alaska.local\GIS\Anchorage\GISStaff\AK_BASE\ARCTIC_CIRCLE.mdb\arctic_circle
trunc %>% mutate(
  newPath = gsub('arctic_circle$', '\\\\dfg.alaska.local\\\\GIS\\\\Anchorage\\\\GISStaff\\\\wc\\\\MUMM\\\\Stow\\\\arctic_circle.shp', ros$newPath))-> trunc

# colapse to only distinct brokenPaths and sort
trunc %>% distinct(brokenPath, .keep_all = TRUE) %>% arrange(brokenPath) -> dis

 dis[217,]

 # write
dis %>% write.csv('./out/rosetta_201117.csv', row.names = FALSE)  

