X_LOW, X_HIGH = -2.0, 2.0
Y_LOW, Y_HIGH = -2.0, 2.0
Z_LOW, Z_HIGH = -2.0, 2.0
R_LOW, R_HIGH = 1.0, 2.0

import random

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

class Intersect(Node):
  def __init__(self, nodes):
    self.nodes = nodes

  def export(self):
    to_return = '''
    {} {{
        Type internal
        Operator intersect
        numChildren {}
        Child {}
    }}
'''.format(self.name, len(self.nodes), "".join([node.name+" " for node in self.nodes]))
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

  def export_render(self):
    ret = '''
PerspectiveCamera {{
    center 5 5 5
    direction -1 -1 -1
    up 0 1 0
    angle 90
}}

Lights {{
    numLights 2
    PointLight {{
        position 5 5 0
        color 0.9 0.9 0.9
        falloff 0.025
    }}
    DirectionalLight {{
        direction 1 0 -1
        color 0.9 0.9 0.9
    }}
}}

Background {{
    color 0 0 0 
    ambientLight 0.1 0.1 0.1 
}}

Materials {{
    numMaterials 4
    Material {{
        diffuseColor 0.7 0 0
        specularColor 0.6 0.6 0.6
        shininess 20
    }}
    Material {{ diffuseColor 0 0.5 0 }}
    Material {{
        diffuseColor 0.70 0.58 0.37
        specularColor 0.92 0.81 0.48
        shininess 8
    }}
    Material {{
        diffuseColor 0.75 0.63 0.42
        specularColor 0.97 0.86 0.53
        shininess 4
    }}
}}

Group {{
  numObjects 1
  {}

}}

'''.format(self.export())
    return ret

  def write_file(self, name, render=False):
    strr = self.export() if not render else self.export_render()
    print "################ "
    print strr
    print "################ "
    fd = open("data/{}".format(name), "w")
    fd.write(strr)
    fd.close()

def sample_sphere():
  return Sphere(random.uniform(X_LOW,X_HIGH),
                random.uniform(Y_LOW,Y_HIGH),
                random.uniform(Z_LOW,Z_HIGH),
                random.uniform(R_LOW,R_HIGH),
               )

def sample_random_csg(d=3):

  def _sample_random_csg(depth):
    if depth == 0:
      sphere = sample_sphere()
      return sphere, [sphere]
    else:
      idxx = random.randint(0,3)
      lhs, lhs_list = _sample_random_csg(depth - 1)
      rhs, rhs_list = _sample_random_csg(depth - 1)
      sphere = sample_sphere()
      if idxx == 0:
        return sphere, [sphere]
      if idxx == 1:
        union_ = Union([lhs, rhs])
        return union_, [union_] + lhs_list + rhs_list
      if idxx == 2:
        intersect_ = Intersect([lhs, rhs])
        return intersect_, [intersect_] + lhs_list + rhs_list
      if idxx == 3:
        sub_ = Subtract(lhs, rhs)
        return sub_, [sub_] + lhs_list + rhs_list
      assert 0, "NANI?! {} ".format(idxx)

  root, nodes = _sample_random_csg(d)
  return CSG(root, nodes)
      
 
if __name__ == '__main__':
  # s1 = Sphere(0.0, 0.0, 0.0, 1.0)
  # s2 = Sphere(1.0, 0.0, 1.0, 1.0)
  # s3 = Sphere(0.0, 1.0, 0.0, 1.0)
  # n0 = Union([s1,s3])
  # n4 = Subtract(n0, s2)

  # csg = CSG(n4, [s1,s2,s3,n0,n4])
  # print csg.export()
  # csg.write_file()

  print 'wololo'
  csg = sample_random_csg(4)
  # print csg.export()
  csg.write_file("csg.txt", render=True)

  import os
  print "trying to draw"
  os.system('csg render -input data/csg.txt -output data/haha.png -size 400 400')


