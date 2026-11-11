extends CharacterBody2D

const SPEED = 50.0

# walk in all directions
func _physics_process(delta):
	
	# player x movement
	var x_direction := Input.get_axis("move_left", "move_right")
	
	# player y movement
	var y_direction := Input.get_axis("move_up", "move_down")
	
	if x_direction:
		velocity.x = x_direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
	
	if y_direction:
		velocity.y = y_direction * SPEED
	else:
		velocity.y = move_toward(velocity.y, 0, SPEED)
	
	# changes player position based on x and y inputs
	position += (velocity.normalized() * SPEED) * delta
