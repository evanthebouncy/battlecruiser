class Node:
  def __init__(self):
    pass
  def coronation(self, name):
    self.name = name

class Sphere(Node):
  def __init__(self, x,y,z,r):
    self.x, self.y, self.z, self.r = x,y,z,r
  def export(self):
    to_return = '''
    {} {{
      Type leaf
      MaterialIndex 0
      Sphere {{
          Center {} {} {}
          Radius {}
      }}
    }}
'''.format(self.name, self.x, self.y, self.z, self.r)
    return to_return

    
class Union(Node):
  def __init__(self, nodes):
    self.nodes = nodes

  def export(self):
    to_return = '''
    {} {{
        Type internal
        Operator union
        numChildren {}
        Child {}
    }}
'''.format(self.name, len(self.nodes), "".join([node.name+" " for node in self.nodes]))
    return to_return

# class Intersection(Node):
#   def __init__(self, nodes):
#     self.nodes = nodes
#   def export(self):
#     to_return = '''
#         {} {{
#             Type internal
#             Operator subtract
#             numChildren {}
#             Child {}
#         }}
#     '''.format(self.name, len(self.nodes), "".join([node.name+" " for node in self.nodes]))
#     return to_return


class Subtract(Node):
  def __init__(self, node1, node2):
    self.node1, self.node2 = node1, node2
  def export(self):
    to_return = '''
    {} {{
        Type internal
        Operator subtract
        numChildren {}
        Child {}
    }}
'''.format(self.name, 2, self.node1.name+" "+self.node2.name)
    return to_return

class CSG:
  def __init__(self, root_node, nodes):
    self.root_node = root_node
    self.nodes = nodes
    self.uniq = 0

  def export(self):
    ret = '''
CSG {{
    numNodes {} 
'''.format(len(self.nodes))
    for i,node in enumerate(self.nodes):
      node.coronation('n{}'.format(i))
    for node in self.nodes:
      ret += node.export() 
    ret += "}\n"
    return ret

 
if __name__ == '__main__':
  s1 = Sphere(0.0, 0.0, 0.0, 1.0)
  s2 = Sphere(1.0, 0.0, 1.0, 1.0)
  s3 = Sphere(0.0, 1.0, 0.0, 1.0)
  n0 = Union([s1,s3])
  n4 = Subtract(n0, s2)

  csg = CSG(n4, [s1,s2,s3,n0,n4])
  print csg.export()
  assert 0
  s1.coronation("0")
  s2.coronation("1")
  s3.coronation("2")
  n0.coronation("uninuni")
  print s1.export()
  print n0.export()


