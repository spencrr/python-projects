def rowFormat(matrix):
	end = ''
	for i in range(len(matrix)):
		if(i % 2 == 1):
			matrix[i] = matrix[i][::-1]
		end += ','.join(matrix[i]) 
		if(i != len(matrix) - 1):
			end += ',\n'
	return end

# def toMatrix(str):
# 	numbers = str.split(',')
# 	rows = []
# 	for i in range(17):
# 		n = (i) * 17
# 		rows.append(numbers[i * 17: (i + 1) * 17])
# 	return rows

from PIL import Image
from pprint import pprint

size = 17
dimen = (size, size)


im = Image.open('i.bmp') #CHANGE IMAGE NAME
im.resize(dimen)
pixels = im.load()

pix_matrix = []
for i in range(size):
	pix_matrix.append(['0x%02x%02x%02x' % pixels[i , j] for j in range(size)])

#for processing
print(str(pix_matrix).replace("\'", "").replace('[', '{').replace(']', '}') + '\n\n')

#for your arduino
print(rowFormat(pix_matrix))
