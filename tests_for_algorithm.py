import unittest
from HelperClass import HelperFunctions
from battleship_simulation import Ship,Square,Simulator

#This file focuses on testing the ship killing algorithm
class BattleshipTestCase(unittest.TestCase):
    def setUp(self):
        self.simulation1 = Simulator()
        self.ship1 = Ship(5)  #this ship is 5 units long
        self.ship2 = Ship(4)  #this ship is 4 units long
        self.ship3 = Ship(3)  # etc.
        self.ship4 = Ship(3)
        self.ship5 = Ship(2)
        
    def tearDown(self):
        del(self.simulation1)
        del(self.ship1, self.ship2, self.ship3, self.ship4, self.ship5)
        
    #these tests provide an initial attack coordinate at the start of each simulation.
    
    #ONE SHIP TESTS
    def test_algorithm1(self):
        self.simulation1.ships = [self.ship1]
        slots = [(3,4,'horizontal')]
        self.simulation1.start_simulation2((4,4),slots)
        self.assertLess(len(self.simulation1.strike_summary),9)

    def test_algorithm2(self):
        self.simulation1.ships = [self.ship1]
        slots = [(0,0,'horizontal')]
        self.simulation1.start_simulation2((0,0),slots)
        self.assertLess(len(self.simulation1.strike_summary),9)

    def test_algorithm3(self):
        self.simulation1.ships = [self.ship1]
        slots = [(0,3,'vertical')]
        self.simulation1.start_simulation2((0,4),slots)
        self.assertLess(len(self.simulation1.strike_summary),9)

    def test_algorithm4(self):  
        self.simulation1.ships = [self.ship1]
        slots = [(0,1,'vertical')]
        self.simulation1.start_simulation2((0,1),slots)
        print(self.simulation1.strike_summary)
        self.assertLess(len(self.simulation1.strike_summary),6)    

                 
    def test_algorithm5(self):
        self.simulation1.ships = [self.ship5]
        slots = [(5,5,'vertical')]
        self.simulation1.start_simulation2((5,5),slots)
        self.assertLess(len(self.simulation1.strike_summary),6)

    def test_algorithm6(self):
        self.simulation1.ships = [self.ship5]
        slots = [(9,8,'vertical')]
        self.simulation1.start_simulation2((9,9),slots)
        self.assertLess(len(self.simulation1.strike_summary),4)
        
    #TWO SHIP TESTS
        
    def test_algorithm7(self):
        self.simulation1.ships = [self.ship1,self.ship5] #5, 2
        slots = [(3,3,'vertical'),(1,5,'horizontal')]
        self.simulation1.start_simulation2((2,5),slots)
        self.assertLess(len(self.simulation1.strike_summary),13)

    def test_algorithm8(self):
        self.simulation1.ships = [self.ship1,self.ship5] #5, 2
        slots = [(5,7,'horizontal'),(5,8,'vertical')]
        self.simulation1.start_simulation2((5,8),slots)
        self.assertLess(len(self.simulation1.strike_summary),13)

    def test_algorithm9(self):
        self.simulation1.ships = [self.ship1,self.ship5] #5, 2
        slots = [(6,3,'vertical'),(7,5,'horizontal')]
        self.simulation1.start_simulation2((7,5),slots)
        self.assertLess(len(self.simulation1.strike_summary),13)

    def test_algorithm10(self):
        self.simulation1.ships = [self.ship3,self.ship4] #3, 3
        slots = [(3,3,'horizontal'),(4,0,'vertical')]
        self.simulation1.start_simulation2((4,2),slots)
        self.assertLess(len(self.simulation1.strike_summary),11)


   #THREE SHIP TESTS
    def test_algorithm11(self): 
        self.simulation1.ships = [self.ship2,self.ship3,self.ship4]
        slots = [(0,3,'horizontal'),(0,4,'horizontal'),(0,5,'horizontal')]
        self.simulation1.start_simulation2((0,4),slots)
        print(self.simulation1.strike_summary)
        self.assertLess(len(self.simulation1.strike_summary),13)


    #FIVE SHIP TESTS

      # test_algorithm 12 through 13:  basic layout of ships on gameboard:
      #
      #   5432
      #3335432
      #   543
      #   54
      #   5
      
    def test_algorithm12(self):
        #5, 4, 3, 3, 2
        self.simulation1.ships = [self.ship1,self.ship2,self.ship3,self.ship4,self.ship5] 
        slots = [(3,2,'vertical'),(4,2,'vertical'),(5,2,'vertical'),(0,3,'horizontal'),(6,2,'vertical')]
        self.simulation1.start_simulation2((2,3),slots)
        self.assertLess(len(self.simulation1.strike_summary),25)

    def test_algorithm13(self): 
        #5, 4, 3, 3, 2
        self.simulation1.ships = [self.ship1,self.ship2,self.ship3,self.ship4,self.ship5] 
        slots = [(3,0,'vertical'),(4,0,'vertical'),(5,0,'vertical'),(0,0,'horizontal'),(6,0,'vertical')]
        self.simulation1.start_simulation2((2,0),slots)
        self.assertLess(len(self.simulation1.strike_summary),21)

if __name__ == '__main__':
    unittest.main()


#'assertAlmostEqual', 'assertAlmostEquals', 'assertCountEqual',
#'assertDictContainsSubset', 'assertDictEqual', 'assertEqual', 'assertEquals',
#'assertFalse', 'assertGreater', 'assertGreaterEqual', 'assertIn',
#'assertIs', 'assertIsInstance', 'assertIsNone', 'assertIsNot',
#'assertIsNotNone', 'assertLess', 'assertLessEqual', 'assertListEqual',
#'assertLogs', 'assertMultiLineEqual', 'assertNotAlmostEqual',
#'assertNotAlmostEquals', 'assertNotEqual', 'assertNotEquals', 'assertNotIn',
#'assertNotIsInstance', 'assertNotRegex', 'assertNotRegexpMatches',
#'assertRaises', 'assertRaisesRegex', 'assertRaisesRegexp', 'assertRegex',
#'assertRegexpMatches', 'assertSequenceEqual'
