library(ClusterGVis)
raw_data <- read.csv("all.csv", row.names = 1)
getClusters(exp = raw_data)
# mfuzz
cm <- clusterData(exp = raw_data,
                  cluster.method = "mfuzz",
                  cluster.num = 5)

# plot line only
visCluster(object = cm,
           plot.type = "line",
          line.col = "white")
# change color
visCluster(object = cm,
           plot.type = "line",
           ms.col = c("#ffffff","#ff96d8","#c90093"))
visCluster(object = cm,
           plot.type = "heatmap")
visCluster(object = cm,
           plot.type = "heatmap",
           column_names_rot = 45,
           ctAnno.col = ggsci::pal_rickandmorty()(10))

