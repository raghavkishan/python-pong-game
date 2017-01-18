# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0.0, 0.0]
acc = 1
SCORE_1 = 0
SCORE_2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """The Ball is spwaned from the center to the appropriate direction depending on which player
     won the previos point.Boolean variables used for the direction."""

    global ball_pos, ball_vel, SCORE_1, SCORE_2, acc  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if (direction):
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -random.randrange(2, 4)
    else:
        ball_vel[0] = -random.randrange(2, 4)
        ball_vel[1] = -random.randrange(2, 4)
    acc = 1


# define event handlers
def restart():
    """ This event handler is to reset the scores and start a new game on clicking restart"""
    new_game()


def new_game():
    """ Initializes the variables for a new game"""
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, SCORE_1, SCORE_2  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(RIGHT)
    SCORE_1 = 0
    SCORE_2 = 0
    acc = 1


def draw(canvas):
    """inlcudes the code to perform all the visible drawings on the canvas with the logic for the paddles  and the gutters."""
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, acc, SCORE_1, SCORE_2

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += (acc * ball_vel[0])
    ball_pos[1] += (acc * ball_vel[1])
    # Collision with top and bottom wall
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "red", "white")

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) >= HALF_PAD_HEIGHT and (paddle1_pos + paddle1_vel) <= (HEIGHT) - HALF_PAD_HEIGHT:
        paddle1_pos = paddle1_pos + paddle1_vel

    if (paddle2_pos + paddle2_vel) >= HALF_PAD_HEIGHT and (paddle2_pos + paddle2_vel) <= (HEIGHT) - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_line([0, paddle1_pos + HALF_PAD_HEIGHT], [0, paddle1_pos - HALF_PAD_HEIGHT], PAD_WIDTH + 9, "white")
    canvas.draw_line([WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], PAD_WIDTH + 9,
                     "white")

    # determine whether paddle and ball collide

    if (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT) and (ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT) and (
        ball_pos[0] <= BALL_RADIUS):
        ball_vel[0] = -ball_vel[0]
        acc += (0.1 * acc)
    elif ball_pos[0] <= BALL_RADIUS:
        SCORE_2 += 1
        spawn_ball(RIGHT)

    if (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT) and (ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT) and (
        ball_pos[0] >= (WIDTH - BALL_RADIUS)):
        ball_vel[0] = -ball_vel[0]
        acc += (0.1 * acc)
    elif ball_pos[0] >= (WIDTH - BALL_RADIUS):
        SCORE_1 += 1
        spawn_ball(LEFT)

    # draw scores
    canvas.draw_text(str(SCORE_1), [255, 50], 45, "white")
    canvas.draw_text(str(SCORE_2), [320, 50], 45, "white")


def keydown(key):
    """Updates the velocity of the paddles when the key is pressed."""
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -4
    if key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 4
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -4
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 4


def keyup(key):
    """ Updates the velocity of the paddles when the key pressed is left."""
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button = frame.add_button("Restart", restart)

# start frame
new_game()
frame.start()
