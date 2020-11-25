import pygame
import math

# constants
DISPLAY_SIZE = (1280, 720)
CENTRE       = list(map(int, [DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2]))

GRID_OFFSET = 80

AXIS_X_POS = list(map(int, [GRID_OFFSET, DISPLAY_SIZE[1] - (GRID_OFFSET / 2)]))
AXIS_X_SIZE = [(DISPLAY_SIZE[0] - 40) - GRID_OFFSET, 0]
AXIS_X_ENDPOS = [AXIS_X_POS[0] + AXIS_X_SIZE[0], AXIS_X_POS[1] + AXIS_X_SIZE[1]]

AXIS_Y_POS = list(map(int, [GRID_OFFSET, GRID_OFFSET / 2]))
AXIS_Y_SIZE = [0, DISPLAY_SIZE[1] - GRID_OFFSET]
AXIS_Y_ENDPOS = [AXIS_Y_POS[0] + AXIS_Y_SIZE[0], AXIS_Y_POS[1] + AXIS_Y_SIZE[1]]

DARKRED = [150, 10 , 10 ]
DARKBLUE = [20, 30, 55]
BLUE = [110, 110, 220]
YELLOW = [220, 220, 110]
LIGHTGREEN = [120 , 170 , 130]
LIME = [150, 200, 120]
AXIS_COLOUR = LIGHTGREEN
CLEAR_COLOUR = DARKBLUE
POINTS_COLOUR = DARKRED
MIDLINE_COLOUR = BLUE
LINE_COLOUR = YELLOW
CONTROLS_COLOUR = LIME

clicked = False
font = None

grid_interval_x = 1
grid_interval_y = 1

points = []

def grid_x(val):
	return int(AXIS_X_POS[0] + (grid_interval_x * val))

def grid_y(val, trough, peak):
	diff = peak - trough
	if diff == 0:
		return int(AXIS_Y_ENDPOS[1])
	return int(
		AXIS_Y_ENDPOS[1] - (AXIS_Y_SIZE[1]/diff * val)
	)

def apply(display, amp, arg, mid):
	global grid_interval_x, grid_interval_y, points
	if arg <= 0:
		arg = 1
	period = int(math.pi*2 / arg)

	points.clear()

	peak = mid + amp
	trough = mid - amp
	data_range = peak - trough
	grid_interval_y = AXIS_Y_SIZE[1] / peak

	for i in range(0, data_range + 1):
		x = grid_x(0) - 4
		y = grid_y(i, trough, peak)

		# horizontal markers on Y axis
		pygame.draw.line(display, AXIS_COLOUR, [x, y], [x + 8, y])

		# number line
		num = smallfont.render(str(trough + i), False, AXIS_COLOUR)
		display.blit(num, [x-20, y-6])

	if period == 0:
		period = 1

	grid_interval_x = AXIS_X_SIZE[0] / period

	for i in range(0, period + 1):
		x = grid_x(i)
		y = grid_y(0, trough, peak)

		# vertical markers on X axis
		pygame.draw.line(display, AXIS_COLOUR, [x, y], [x, y + 8])

		# number line
		num = smallfont.render(str(i), False, AXIS_COLOUR)
		display.blit(num, [x-6, y+12])

	pygame.draw.line(display, MIDLINE_COLOUR,
		[AXIS_Y_POS[0], grid_y(mid-trough, trough, peak)],
		[AXIS_X_ENDPOS[0], grid_y(mid-trough, trough, peak)])

	for i in range(0, period + 1):
		x = grid_x(i)
		y = grid_y(mid + period * math.sin(math.pi*2/period * i)-trough, trough, peak)
		points.append([x, y])
		pygame.draw.circle(display, POINTS_COLOUR, [x, y], 4)

def draw_axis_lines(display):
	pygame.draw.line(display, AXIS_COLOUR, AXIS_X_POS, AXIS_X_ENDPOS, 2)
	pygame.draw.line(display, AXIS_COLOUR, AXIS_Y_POS, AXIS_Y_ENDPOS, 2)

def run():
	global manual, font, smallfont, clicked, mouse_down, angle_deg_auto, angle_deg_manual, ap, mp

	pygame.init()
	pygame.font.init()

	font = pygame.font.SysFont("Noto Mono", 22)
	smallfont = pygame.font.SysFont("Noto Mono", 12)

	display = pygame.display.set_mode(DISPLAY_SIZE)
	pygame.display.set_caption("Sinusoidal Graph")

	clock = pygame.time.Clock()

	lines_on = True
	should_run = True
	y_origin = 65
	amplitude = 15
	num_points = 7

	control_strings = [
		"q - Quit",
		"l - Toggle line",
		"up/down - Amplitude",
		"left/right - Precision"
	]

	controls = [font.render(control_strings[i], True, CONTROLS_COLOUR) for i in range(0, len(control_strings))]

	while should_run:
		# events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				should_run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					should_run = False
				elif event.key == pygame.K_UP:
					amplitude -= 2
				elif event.key == pygame.K_DOWN:
					amplitude += 2
				elif event.key == pygame.K_LEFT:
					num_points -= 2
					if num_points <= 0:
						num_points = 1
				elif event.key == pygame.K_RIGHT:
					num_points += 2
				elif event.key == pygame.K_l:
					lines_on = not lines_on

		display.fill(CLEAR_COLOUR)

		draw_axis_lines(display)
		apply(display, amplitude, (math.pi*2)/(num_points+1), y_origin)

		if lines_on:
			pygame.draw.lines(display, LINE_COLOUR, False, points)

		for i in range(0, len(controls)):
			display.blit(controls[i], (940, 20 + i * 30))
			
		pygame.display.update()
		clock.tick(20)

if __name__ == "__main__":
	run()
else:
	run()
