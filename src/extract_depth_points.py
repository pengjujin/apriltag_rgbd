#!/usr/bin/env python
import sys
import cv2
import numpy as np
import bayesplane
import plane

def main(args):
	fx = 529.29
	fy = 531.28
	px = 466.96
	py = 273.26
	depth_image = cv2.imread("../data/depth_frame.png", cv2.IMREAD_ANYDEPTH)
	rgb_image = cv2.imread("../data/rgb_frame.png")
	april_tag_rgb = rgb_image[175:195, 440:458]
	april_tag_depth = depth_image[175:195, 440:458]
	cv2.imshow('april_tag', april_tag_rgb)
	cv2.waitKey(0)
	all_pts = []
	for i in range(175, 178):
		for j in range(440, 448):
			depth = depth_image[i,j] / 1000.0
			if(depth != 0):
				x = (i - px) * depth / fx
				y = (i - py) * depth / fy
				all_pts.append([x,y,depth])
	sample_cov = 0.05
	samples = np.array(all_pts)
	cov = np.asarray([sample_cov] * samples.shape[0])
	plane_est = bayesplane.fit_plane_bayes(samples, cov)

	# Generate AprilTag homography poses from the image
	# sample a few points from the apriltags and compare it to the plane
	plane_est.plot(10)
	
if __name__ == '__main__':
	main(sys.argv)