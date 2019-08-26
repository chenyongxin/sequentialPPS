#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualize sequential output data with XDMF in paraview/visIt

@author: CHEN Yongxin
"""


import numpy as np
from struct import unpack

def readData(fname):
    """
    Read raw data from file fname. The data stored in fname is in sequential order (chunked).
    This function is to plug each partition's data into a correct position of a global array.
    """
    with open(fname, 'rb') as fh:
        
        # read partitions
        partitions = np.array(unpack('iii', fh.read(4*3)), dtype=np.int32)
        
        # loop partitions
        for i in range(np.prod(partitions)):
            
            # partition info
            _ = unpack('i', fh.read(4))[0]     # rank
            extent = np.array( unpack('i'*6, fh.read(4*6)) )
            wholeExtent = np.array( unpack('i'*6, fh.read(4*6)) )
            
            # init if first
            if i == 0:
                n = wholeExtent[1::2] - wholeExtent[::2] + 1  # total grid points
                a = np.zeros(n, dtype=np.float32)                  # global array
            
            # data related info
            byte_size = unpack('i', fh.read(4))[0]
            n = extent[1::2] - extent[::2] + 1                # local grid points
            data = np.array( unpack('f'*np.prod(n), fh.read(byte_size)), dtype=np.float32 ).reshape(n, order='F')
            
            # plug into global array
            st = extent[::2]-1
            ed = extent[1::2]
            a[st[0]:ed[0], st[1]:ed[1], st[2]:ed[2]] = data
        
    return a



def writeXDMF(xml, fname, x, y, z, a):
    """
    Write XDMF for data in a rectilinear grid
    
    Parameters
    ----------
    xml: string
        Name of XDMF file. e.g. 'data.xmf'.
        
    fname: string
        File name of HDF5 file. e.g. 'data.h5'.
        
    x,y,z: array
        1D array for coordinates.
        
    a: array
        3D array of data.
    """
    import h5py
    
    # write XML file
    with open(xml, 'w') as fh:
        nx, ny, nz = a.shape
        fh.write('<?xml version="1.0" ?>\n')
        fh.write('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
        fh.write('<Xdmf Version="2.0">\n')
        fh.write('<Domain>\n')
        fh.write('<Grid Name="rectilinear_scalar" GridType="Uniform">\n')
        fh.write('<Topology TopologyType="3DRECTMesh" NumberOfElements="{} {} {}"/>\n'.format(nz, ny, nx))
        fh.write('<Geometry GeometryType="VXVYVZ">\n')
        fh.write('<DataItem Name="xcoords" Dimensions="{}" NumberType="Float" Precision="4" Format="HDF">\n'.format(x.size))
        fh.write(fname+':/xcoords\n')
        fh.write('</DataItem>\n')
        fh.write('<DataItem Name="ycoords" Dimensions="{}" NumberType="Float" Precision="4" Format="HDF">\n'.format(y.size))
        fh.write(fname+':/ycoords\n')
        fh.write('</DataItem>\n')
        fh.write('<DataItem Name="zcoords" Dimensions="{}" NumberType="Float" Precision="4" Format="HDF">\n'.format(z.size))
        fh.write(fname+':/zcoords\n')
        fh.write('</DataItem>\n')
        fh.write('</Geometry>\n')
        fh.write('<Attribute Name="data" AttributeType="Scalar" Center="Node">\n')
        fh.write('<DataItem Dimensions="{} {} {}" NumberType="Float" Precision="4" Format="HDF">\n'.format(nx, ny, nz))
        fh.write(fname+':/data\n')
        fh.write('</DataItem>\n')
        fh.write('</Attribute>\n')
        fh.write('</Grid>\n')
        fh.write('</Domain>\n')
        fh.write('</Xdmf>')

    # write HDF5 file
    with h5py.File(fname, 'w') as hf:
        hf.create_dataset('xcoords', data=x, dtype=np.float32)
        hf.create_dataset('ycoords', data=y, dtype=np.float32)
        hf.create_dataset('zcoords', data=z, dtype=np.float32)
        hf.create_dataset('data',    data=np.transpose(a), dtype=np.float32)

    
a = readData("data")
nx, ny, nz = a.shape
x = np.linspace(0., nx-1, nx)
y = np.linspace(0., ny-1, ny)
z = np.linspace(0., nz-1, nz)
writeXDMF("data.xmf", 'data.h5', x, y, z, a)