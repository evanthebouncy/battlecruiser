import os
import numpy as np
    
def make_query(file_name):
  def query(x,y,z):
    os.system('csg -input data/{} -point {} {} {} -output shit.txt'.format(file_name,x,y,z))
    return True if int(open('shit.txt').readlines()[0][0]) else False

  return query

if __name__ == "__main__":
  qry1 = make_query("csg_three_spheres.txt")
  qry2 = make_query("gen_csg.txt")
  print qry1(0.0, 0.0, 0.0), qry2(0.0, 0.0, 0.0)

