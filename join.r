library (tidyverse)

read.csv("Y_inventory_working.csv") %>% select(code, Path, Type) ->inv
read.csv("ALL_BrokenSrc20200803_1950_working.csv") -> brk

brk %>% drop_na (code) -> brk.noNa

brk.noNa %>% left_join (inv) -> full

full %>% transmute ( UniqID,dataType,newType = replace_na(Type, "_review"),brokenPath,newPath = Path) -> out

out %>% write.csv('out.csv', row.names = FALSE)  

