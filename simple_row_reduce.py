"""
A simplistic row reduction utility for beginning linear algebra textbook problems 
(typically whole numbers which row reduce to a "clean" solution).

Uses numpy and the Fraction type from the fractions module. 
Module provides 1 public method: row_reduce() which takes a list of lists 
or a numpy ndarray as an argument. Optionally users can request a ndarray as a 
return type instead of the default (a Matrix of fractions in list form).

examples:

import simple_row_reduce as srr
from numpy import array

x = [2,3,1,5, -1,0,1,-1, 2,1,-1,3]
x = array(x).reshape(3,4)

solution = srr.row_reduce(x,1) # get ndarray as return type

print(solution)


## prints:
## [[ 1.  0. -1.  1.]
## [ 0.  1.  1.  1.]
## [ 0.  0.  0.  0.]]

## altenatively:
solution = srr.row_reduce(x)
print(solution)

## prints:
## [[Fraction(1, 1), Fraction(0, 1), Fraction(-1, 1), Fraction(1, 1)], [Fraction(0,
##  1), Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)], [Fraction(0, 1), Fraction(
## 0, 1), Fraction(0, 1), Fraction(0, 1)]]
"""
from fractions import Fraction
from numpy import array
from numpy import zeros
import numpy

FRACTIONLIST = 0
NPARRAY = 1


def _floatlist_to_fraclist(_arr):
	assert len(_arr) > 0
	m = len(_arr)
	n = len(_arr[0])
	for row in _arr:
		assert len(row) == n

	outlist = []
	for idx, row in enumerate(_arr):
		outlist.append([])
		for val in row:
			outlist[idx].append(Fraction.from_float(val))
	return outlist


def _fraclist_to_array(flist):
	assert len(flist) > 0
	m = len(flist)
	n = len(flist[0])
	for row in flist:
		assert len(row) == n
		
	outarr = zeros((m,n))
	for idxm, row in enumerate(flist):
		for idxn, colval in enumerate(row):
			outarr[idxm][idxn] = ((1.0*colval.numerator) / colval.denominator)
	
	return outarr

def _array_to_fraclist(_arr):
	assert len(_arr) > 0
	m = len(_arr)
	n = len(_arr[0])
	for row in _arr:
		assert len(row) == n

	outlist = []
	for idx, row in enumerate(_arr):
		outlist.append([])
		try:
			for val in row:
				outlist[idx].append(Fraction(val,1))
		except TypeError:
			print('found non integer value. interpreting as floats and attempting import...')
			return _floatlist_to_fraclist(_arr)
			
	return outlist

def row_reduce(flist, returntype = FRACTIONLIST):
	newlist = _array_to_fraclist(flist)
	
	x = len(newlist)
	assert x > 0
	y = len(newlist[0])
	assert y > 0
	for j in newlist:
		assert len(j) == y
	
	prow = 0
	pcol = 0
	
	while prow >= 0 and pcol >= 0:
		
		_force_leading_one(newlist, prow, pcol)
		_zero_column_vec(newlist, prow, pcol)
		
		# get next prow & pcol
		prow, pcol = _get_next_pivots(newlist, prow, pcol)
		
	
	if returntype:
		return _fraclist_to_array(newlist)
	
	return newlist
	
def _force_leading_one(flist, prow, pcol):
	dvx = Fraction(1,flist[prow][pcol])
	for i in range(len(flist[prow])):
		flist[prow][i] *= dvx

	
def _zero_column_vec(flist, prow, pcol):
	for idx, row in enumerate(flist):
		if idx != prow and row[pcol] != 0:  # skip 0s and pivot row
			mx = (-1 * flist[idx][pcol]) / flist[prow][pcol]
			for i in range(len(flist[prow])):
				flist[idx][i] += mx * flist[prow][i]
	

	
def _get_next_pivots(flist,prow,pcol):
	# force exit on fall-through
	prow_next = -2
	pcol_next = -2
	
	if prow == len(flist) - 1:
		return (-1,-1)
	
	else:
		offset = 1
		while prow + offset < len(flist) and sum(flist[prow+offset]) == 0:
			offset += 1
		prow_next =  prow + offset
		
		if prow_next >= len(flist):
			return (-1,-1)
		
		
	#cols
	if pcol == len(flist[0]) - 1:
		return (-1,-1)
	
	else:
		try:
			offset = 1
			while pcol + offset < len(flist[0]) and flist[prow_next][pcol + offset] == 0:
				offset += 1
			pcol_next = pcol + offset
		
			if pcol_next >= len(flist[0]):
				return (-1,-1)
		
		except:
			pdb.set_trace()
			
	return (prow_next, pcol_next)
	
	
