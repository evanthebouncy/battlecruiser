import os
import numpy as np
    
def make_query(file_name):
  def query(x,y,z):
    os.system('csg -input data/{} -point {} {} {} -output out.txt'.format(file_name,x,y,z))
    return True if int(open('out.txt').readlines()[0][0]) else False
  return query

def diff_set(file1, file2):
  os.system('csg diff data/{} data/{} -output out.txt'.format(file1, file2))
  print open('out.txt').readlines()

if __name__ == "__main__":
  # qry1 = make_query("csg_three_spheres.txt")
  # qry2 = make_query("gen_csg.txt")
  # print qry1(0.0, 0.0, 0.0), qry2(0.0, 0.0, 0.0)
  diff_set('csg.txt', 'csg_two_spheres.txt')

