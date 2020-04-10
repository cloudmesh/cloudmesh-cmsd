cmsd --clean
cmsd --ps
cmsd --setup ~/.cloudmesh
cmsd --ps
cmsd config set cloudmesh.data.mongo.MONGO_PASSWORD=admin99
cmsd --setup ~/.cloudmesh
cmsd --ps
