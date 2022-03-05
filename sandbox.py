a = [[[0, 0, 1], [1, 0, 0]]]

def search_array(array, target):
  for i in array:
    if i == target:
      return True
  return False

print([0, 0, 1] in a[0])