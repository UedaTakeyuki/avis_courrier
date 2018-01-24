# refer to https://sites.google.com/site/lifeslash7830/home/hua-xiang-chu-li/opencvniyoruhuaxiangchuliafinbianhuantoka
import cv2
import numpy as np

def transform(ifile,ofile,left,right,depth):
	img = cv2.imread(ifile,1)
	rows,cols,ch = img.shape

	print rows
	print cols

	pts1 = np.float32([[0,0],[rows,0],[-left,cols],[rows + right,cols]])
	pts2 = np.float32([[0,0],[rows,0],[0,cols - depth],[rows,cols - depth]])

	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(img,M,(cols,rows))

	cv2.imwrite(ofile,dst)

if __name__ == '__main__':
	transform('v1_06.jpg', 'result.jpg', 400, 200, 90)
