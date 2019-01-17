#!/usr/local/bin/python3
def rowFormat(matrix):
	end = ''
	for i in range(len(matrix)):
		if(i % 2 == 1):
			matrix[i] = matrix[i][::-1]
		end += ','.join(matrix[i]) 
		if(i != len(matrix) - 1):
			end += ',\n'
	return end

from PIL import Image
from pprint import pprint

size = 17
dimen = (size, size)


im = Image.open('i.bmp') 
im.resize(dimen)
pixels = im.load()

pix_matrix = []
for i in range(size):
	pix_matrix.append(['0x%02x%02x%02x' % pixels[i , j] for j in range(size)])

print(str(pix_matrix).replace("\'", "").replace('[', '{').replace(']', '}') + '\n\n')

print(rowFormat(pix_matrix))
