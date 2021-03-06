import os
import unittest
from .._contW_lists import ContiguityWeightsLists, ROOK, QUEEN
from ..weights import W
from ...io.FileIO import FileIO as ps_open


try:
    import geopandas as gpd
except ImportError:
    gpd = None


from ... import examples as pysal_examples



class TestContiguityWeights(unittest.TestCase):
    def setUp(self):
        """ Setup the binning contiguity weights"""
        shpObj = ps_open(pysal_examples.get_path('virginia.shp'), 'r')
        self.binningW = ContiguityWeightsLists(shpObj, QUEEN)
        shpObj.close()

    def test_w_type(self):
        self.assert_(isinstance(self.binningW, ContiguityWeightsLists))

    def test_QUEEN(self):
        self.assertEqual(QUEEN, 1)

    def test_ROOK(self):
        self.assertEqual(ROOK, 2)

    def test_ContiguityWeightsLists(self):
        self.assert_(hasattr(self.binningW, 'w'))
        self.assert_(issubclass(dict, type(self.binningW.w)))
        self.assertEqual(len(self.binningW.w), 136)

    def test_nested_polygons(self):
        # load queen gal file created using Open Geoda.
        geodaW = ps_open(
            pysal_examples.get_path('virginia.gal'), 'r').read()
        # build matching W with pysal
        pysalWb = self.build_W(
            pysal_examples.get_path('virginia.shp'), QUEEN, 'POLY_ID')
        # compare output.
        for key in geodaW.neighbors:
            geoda_neighbors = map(int, geodaW.neighbors[key])
            pysalb_neighbors = pysalWb.neighbors[int(key)]
            geoda_neighbors.sort()
            pysalb_neighbors.sort()
            self.assertEqual(geoda_neighbors, pysalb_neighbors)

    def test_true_rook(self):
        # load queen gal file created using Open Geoda.
        geodaW = ps_open(pysal_examples.get_path('rook31.gal'), 'r').read()
        # build matching W with pysal
        #pysalW = pysal.rook_from_shapefile(pysal_examples.get_path('rook31.shp'),','POLY_ID')
        pysalWb = self.build_W(
            pysal_examples.get_path('rook31.shp'), ROOK, 'POLY_ID')
        # compare output.
        for key in geodaW.neighbors:
            geoda_neighbors = map(int, geodaW.neighbors[key])
            pysalb_neighbors = pysalWb.neighbors[int(key)]
            geoda_neighbors.sort()
            pysalb_neighbors.sort()
            self.assertEqual(geoda_neighbors, pysalb_neighbors)

    def test_true_rook2(self):
        # load queen gal file created using Open Geoda.
        geodaW = ps_open(
            pysal_examples.get_path('stl_hom_rook.gal'), 'r').read()
        # build matching W with pysal
        pysalWb = self.build_W(pysal_examples.get_path(
            'stl_hom.shp'), ROOK, 'POLY_ID_OG')
        # compare output.
        for key in geodaW.neighbors:
            geoda_neighbors = map(int, geodaW.neighbors[key])
            pysalb_neighbors = pysalWb.neighbors[int(key)]
            geoda_neighbors.sort()
            pysalb_neighbors.sort()
            self.assertEqual(geoda_neighbors, pysalb_neighbors)

    def test_true_rook3(self):
        # load queen gal file created using Open Geoda.
        geodaW = ps_open(
            pysal_examples.get_path('sacramentot2.gal'), 'r').read()
        # build matching W with pysal
        pysalWb = self.build_W(pysal_examples.get_path(
            'sacramentot2.shp'), ROOK, 'POLYID')
        # compare output.
        for key in geodaW.neighbors:
            geoda_neighbors = map(int, geodaW.neighbors[key])
            pysalb_neighbors = pysalWb.neighbors[int(key)]
            geoda_neighbors.sort()
            pysalb_neighbors.sort()
            self.assertEqual(geoda_neighbors, pysalb_neighbors)

    def test_true_rook4(self):
        # load queen gal file created using Open Geoda.
        geodaW = ps_open(
            pysal_examples.get_path('virginia_rook.gal'), 'r').read()
        # build matching W with pysal
        pysalWb = self.build_W(
            pysal_examples.get_path('virginia.shp'), ROOK, 'POLY_ID')
        # compare output.
        for key in geodaW.neighbors:
            geoda_neighbors = map(int, geodaW.neighbors[key])
            pysalb_neighbors = pysalWb.neighbors[int(key)]
            geoda_neighbors.sort()
            pysalb_neighbors.sort()
            self.assertEqual(geoda_neighbors, pysalb_neighbors)

    @unittest.skipIf(gpd is None, 'geopandas is missing in the testing environment')
    def test_shapely(self):
        pysalneighbs = ContiguityWeightsLists(ps_open(
            pysal_examples.get_path('virginia.shp')), ROOK)
        gdf = gpd.read_file(pysal_examples.get_path('virginia.shp')) 
        shplyneighbs = ContiguityWeightsLists(gdf.geometry.tolist(), ROOK)
        self.assertEqual(pysalneighbs.w, shplyneighbs.w)
        pysalneighbs = ContiguityWeightsLists(ps_open(
            pysal_examples.get_path('virginia.shp')), QUEEN)
        shplyneighbs = ContiguityWeightsLists(gdf.geometry.tolist(), QUEEN)
        self.assertEqual(pysalneighbs.w, shplyneighbs.w)

    def build_W(self, shapefile, type, idVariable=None):
        """ Building 2 W's the hard way.  We need to do this so we can test both rtree and binning """
        dbname = os.path.splitext(shapefile)[0] + '.dbf'
        db = ps_open(dbname)
        shpObj = ps_open(shapefile)
        neighbor_data = ContiguityWeightsLists(shpObj, type).w
        neighbors = {}
        weights = {}
        if idVariable:
            ids = db.by_col[idVariable]
            self.assertEqual(len(ids), len(set(ids)))
            for key in neighbor_data:
                id = ids[key]
                if id not in neighbors:
                    neighbors[id] = set()
                neighbors[id].update([ids[x] for x in neighbor_data[key]])
            for key in neighbors:
                neighbors[key] = list(neighbors[key])
            binningW = W(neighbors, id_order=ids)
        else:
            neighbors[key] = list(neighbors[key])
            binningW = W(neighbors)
        return binningW

#suite = unittest.TestLoader().loadTestsFromTestCase(_TestContiguityWeights)

if __name__ == '__main__':
    #runner = unittest.TextTestRunner()
    #runner.run(suite)
    unittest.main()
