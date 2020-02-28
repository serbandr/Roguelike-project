def to_camera_coordinates(x, y, camera_width, camera_height, camera_x, camera_y):
	#convert coordinates on the map to coordinates on the screen
	x, y = (x - camera_x, y - camera_y)
 
	if (x < 0 or y < 0 or x >= camera_width or y >= camera_height):
		return (None, None)  #if it's outside the view, return nothing
 
	return x, y

def move_camera(target_x, target_y, camera_width, camera_height, camera_y, camera_x, game_map):
 
	#new camera coordinates (top-left corner of the screen relative to the map)
	x = target_x - camera_width // 2  #coordinates so that the target is at the center of the screen
	y = target_y - camera_height // 2
 
	#make sure the camera doesn't see outside the map
	if x < 0: x = 0
	if y < 0: y = 0
	if x > game_map.width - camera_width - 1: x = game_map.width - camera_width - 1
	if y > game_map.height - camera_height - 1: y = game_map.height - camera_height - 1
 
	return x, y
 