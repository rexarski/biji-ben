# students do not import
import nose 
from all_keys_values import all_keys_values

def test_all_keys_values_two_keys():
  assert all_keys_values ({4:5, 5:4}), 'two keys'


if __name__ == '__main__':
  nose.runmodule()
  