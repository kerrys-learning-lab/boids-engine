import geometry
import itertools
import numpy as np
from sklearn.cluster import DBSCAN


class DBSCAN(object):

    def __init__(self, config):
        super().__init__(self)
        self.tileWidth = config['tile-width']

    def __call__(self, world):
        # Compute DBSCAN
        X = world.getLocationBatch(world.boids)
        db = DBSCAN(eps=self.tileWidth, min_samples=2).fit(X)
        labels = db.labels_
        n_clusters_ = len(set(labels))

        groups = [[] for i in itertools.repeat(None, n_clusters_)]
        for i in range(0, len(world.boids)):
            if world._clusterIndicators == 1:
                world.boids[i].setColour(world._colourList[labels[i]])
            if labels[i] != -1:
                groups[labels[i]].append(i)

        for i in range(n_clusters_):
            for k in range(0, len(groups[i])-1):
                for j in range(k+1, len(groups[i])):
                    v = geometry.Vector.fromPoints(world.boids[groups[i][j]].position,
                                                   world.boids[groups[i][k]].position)
                    if v.magnitude < world.boidConfig.get('range'):
                        if world.boids[groups[i][k]].angleBetweenBoids(v) < world.boids[groups[i][k]].view_angle:
                            world.boids[groups[i][k]].boid_mask[groups[i][j]] = 1
                        if world.boids[groups[i][j]].angleBetweenBoids(v) < world.boids[groups[i][j]].view_angle:
                            world.boids[groups[i][j]].boid_mask[groups[i][k]] = 1


class Tile(object):

    def __init__(self, config):
        super().__init__(self)
        self.tileWidth = config['tile-width']

    def updateLocalBoids(self, world):
        numTilesW = int(world.width/self.tileWidth)
        numTilesH = int(world.height/self.tileWidth)
        numTiles = numTilesW * numTilesH
        tiles = [[] for i in range(0, numTiles)]
        for i in range(0, len(world.boids)):
            x = int(world.boids[i].position.x // (world.width / numTilesW))
            x = np.min([numTilesW-1, x])
            y = int(world.boids[i].position.y // (world.height / numTilesH))
            y = np.min([numTilesH-1, y])
            tiles[x*numTilesH+y].append(i)
            if world._clusterIndicators == 1:
                world.boids[i].setColour(world._colourList[(x*numTilesH+y) % len(world._colourList)])

        world.boids[0].setColour([255, 0, 0])
        x = int(world.boids[0].position.x // (world.width / numTilesW)) * (world.width / numTilesW)
        y = int(world.boids[0].position.y // (world.height / numTilesH)) * (world.height / numTilesH)

        for x in range(0, numTilesW):
            for y in range(0, numTilesH):
                for i in tiles[x*numTilesH+y]:
                    world.boids[i].boid_mask[tiles[x*numTilesH+y]] = 1
                    if x > 0:
                        world.boids[i].boid_mask[tiles[(x-1)*numTilesH+y]] = 1
                    if x < numTilesW-1:
                        world.boids[i].boid_mask[tiles[(x+1)*numTilesH+y]] = 1
                    if y > 0:
                        world.boids[i].boid_mask[tiles[x*numTilesH+(y-1)]] = 1
                    if y < numTilesH-1:
                        world.boids[i].boid_mask[tiles[x*numTilesH+(y+1)]] = 1

                    if x > 0 and y > 0:
                        world.boids[i].boid_mask[tiles[(x-1)*numTilesH+y-1]] = 1
                    if x > 0 and y < numTilesH-1:
                        world.boids[i].boid_mask[tiles[(x-1)*numTilesH+y+1]] = 1
                    if x < numTilesW-1 and y > 0:
                        world.boids[i].boid_mask[tiles[(x+1)*numTilesH+y-1]] = 1
                    if x < numTilesW-1 and y < numTilesH-1:
                        world.boids[i].boid_mask[tiles[(x+1)*numTilesH+y+1]] = 1

        # unflag boids out of range
        for i in range(0, len(world.boids)):
            world.boids[i].boid_mask[i] = 0
            indexs = np.where(world.boids[i].boid_mask == 1)
            if np.size(indexs) > 0:
                for indx in np.nditer(indexs):
                    v = geometry.Vector.fromPoints(world.boids[indx].position, world.boids[i].position)
                    if (v.magnitude > world.boidConfig.get('range')) or (world.boids[i].angleBetweenBoids(v) > world.boids[i].view_angle):
                        world.boids[i].boid_mask[indx] = 0


class DBSCANwithTile(object):

    def __init__(self, config):
        super().__init__(self)
        self.reclusterNum = config['recluster-qty']

    def updateLocalBoids(self, world):
        # Compute DBSCAN
        X = world.getLocationBatch(world.boids)
        db = DBSCAN(eps=self.tileWidth, min_samples=2).fit(X)
        labels = db.labels_
        n_clusters_ = max(labels) + 1

        groups = [[] for i in itertools.repeat(None, n_clusters_)]
        clusterBounds = np.zeros((n_clusters_, 4))
        for i in range(0, n_clusters_):
            clusterBounds[i, :] = [world.width, 0, world.height, 0]  # minX, maxX, minY, maxY
        for i in range(0, len(world.boids)):
            if world._clusterIndicators == 1:
                world.boids[i].setColour(world._colourList[labels[i]])
            if labels[i] != -1:
                groups[labels[i]].append(i)
                if world.boids[i].position.x < clusterBounds[labels[i], 0]:
                    clusterBounds[labels[i], 0] = world.boids[i].position.x
                if world.boids[i].position.x > clusterBounds[labels[i], 1]:
                    clusterBounds[labels[i], 1] = world.boids[i].position.x + 1
                if world.boids[i].position.y < clusterBounds[labels[i], 2]:
                    clusterBounds[labels[i], 2] = world.boids[i].position.y
                if world.boids[i].position.y > clusterBounds[labels[i], 3]:
                    clusterBounds[labels[i], 3] = world.boids[i].position.y + 1

        for i in range(n_clusters_):  # Tile for each cluster
            if len(groups[i]) < self.reclusterNum:
                for k in range(0, len(groups[i])-1):
                    for j in range(k, len(groups[i])):
                        v = geometry.Vector.fromPoints(
                            world.boids[groups[i][j]].position, world.boids[groups[i][k]].position)
                        if v.magnitude < world.boidConfig.get('range'):
                            if world.boids[groups[i][k]].angleBetweenBoids(v) < world.boids[groups[i][k]].view_angle:
                                world.boids[groups[i][k]].boid_mask[groups[i][j]] = 1
                            if world.boids[groups[i][j]].angleBetweenBoids(v) < world.boids[groups[i][j]].view_angle:
                                world.boids[groups[i][j]].boid_mask[groups[i][k]] = 1
            else:
                width = (clusterBounds[i, 1]-clusterBounds[i, 0])
                height = (clusterBounds[i, 3]-clusterBounds[i, 2])
                numTilesW = int(width/self.tileWidth) + 1
                numTilesH = int((height)/self.tileWidth) + 1
                numTiles = numTilesW * numTilesH
                tiles = [[] for i in range(0, numTiles)]
                for k in range(0, len(groups[i])):
                    x = int((world.boids[groups[i][k]].position.x - clusterBounds[i, 0]) // (width / numTilesW))
                    x = np.max([np.min([numTilesW-1, x]), 0])
                    y = int((world.boids[groups[i][k]].position.y - clusterBounds[i, 2]) // (height / numTilesH))
                    y = np.max([np.min([numTilesH-1, y]), 0])
                    tiles[x*numTilesH+y].append(groups[i][k])

                for x in range(0, numTilesW):
                    for y in range(0, numTilesH):
                        for i in tiles[x*numTilesH+y]:
                            world.boids[i].boid_mask[tiles[x*numTilesH+y]] = 1
                            if x > 0:
                                world.boids[i].boid_mask[tiles[(x-1)*numTilesH+y]] = 1
                            if x < numTilesW-1:
                                world.boids[i].boid_mask[tiles[(x+1)*numTilesH+y]] = 1
                            if y > 0:
                                world.boids[i].boid_mask[tiles[x*numTilesH+(y-1)]] = 1
                            if y < numTilesH-1:
                                world.boids[i].boid_mask[tiles[x*numTilesH+(y+1)]] = 1

                            if x > 0 and y > 0:
                                world.boids[i].boid_mask[tiles[(x-1)*numTilesH+y-1]] = 1
                            if x > 0 and y < numTilesH-1:
                                world.boids[i].boid_mask[tiles[(x-1)*numTilesH+y+1]] = 1
                            if x < numTilesW-1 and y > 0:
                                world.boids[i].boid_mask[tiles[(x+1)*numTilesH+y-1]] = 1
                            if x < numTilesW-1 and y < numTilesH-1:
                                world.boids[i].boid_mask[tiles[(x+1)*numTilesH+y+1]] = 1

                # unflag boids out of range
                world.boids[i].boid_mask[i] = 0
                indexs = np.where(world.boids[i].boid_mask == 1)
                if np.size(indexs) > 0:
                    for indx in np.nditer(indexs):
                        v = geometry.Vector.fromPoints(world.boids[indx].position, world.boids[i].position)
                        if (v.magnitude > world.boidConfig.get('range')) or (world.boids[i].angleBetweenBoids(v) > world.boids[i].view_angle):
                            world.boids[i].boid_mask[indx] = 0
