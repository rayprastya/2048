import tkinter as tk
from tkinter import messagebox


# You may import any submodules of tkinter here if you wish
# You may also import anything from the typing module
# All other additional imports will result in a deduction of up to 100% of your A3 mark

from a3_support import *

# Write your classes here
class Model:
	def __init__(self):
		self.new_game()
		self.score = 0
		self.undos = MAX_UNDOS
		self.prev_tiles = []
		self.prev_score = []

	def new_game(self):
		self.tiles = [[None,None,None,None],
		[None,None,None,None],
		[None,None,None,None],
		[None,None,None,None]]

		for row in range(2):
			self.add_tile()

	def get_tiles(self):
		return self.tiles

	def add_tile(self):
		temp = generate_tile(self.tiles)
		position, value = temp 
		self.tiles[position[0]][position[1]] = value

	def move_left(self):
		self.tiles = stack_left(self.tiles)
		merging = combine_left(self.tiles)
		self.score += merging[1]
		self.tiles = merging[0]
		self.tiles = stack_left(self.tiles)
		# self.add_tile()
	
	def move_right(self):
		self.tiles = reverse(self.tiles)
		self.move_left()
		self.tiles = reverse(self.tiles)

	def move_up(self):
		self.tiles = transpose(self.tiles)
		self.move_left()
		self.tiles = transpose(self.tiles)

	def move_down(self):
		self.tiles = transpose(self.tiles)
		self.move_right()
		self.tiles = transpose(self.tiles)

	def attempt_move(self, move):
		prev = self.tiles
		if move == UP:
			self.move_up()
		elif move == LEFT:
			self.move_left()
		elif move == DOWN:
			self.move_down()
		elif move == RIGHT:
			self.move_right()
		
		if prev == self.tiles:
			return False
		else:
			return True

	def get_score(self):
		return self.score

	def get_undos_remaining(self):
		return self.undos

	def use_undo(self):
		self.tiles = self.prev_tiles

	def has_won(self):
		for column in range(NUM_COLS):
			for row in range(NUM_ROWS):
				tile = self.tiles[column][row]
				if tile == 2048:
					return True
		
		return False

	def has_lost(self):
		board = self.tiles
		score = self.score
		key = ["w","a","s","d"]
		for i in key:
			move_output = self.attempt_move(i)
			if move_output == True:
				self.tiles = board
				self.score = score
				return False
		self.tiles = board
		self.score = score
		return True


class StatusBar(tk.Frame):
	def __init__(self,master,**kwargs):
		tk.Frame.__init__(self,
		master)
		frame1 = tk.Frame(self,bg=BACKGROUND_COLOUR,width=50,height=60)
		frame1.pack(side="left", pady=10,padx=10)

		t = tk.Label(
        	        master=frame1,
        	        text="SCORE",
        	        bg=BACKGROUND_COLOUR,
					fg=COLOURS[None],
        	        justify=tk.CENTER,
        	        font=('Arial bold', 20),
					)

		t.pack(side="top")
		
		self.score_text = tk.Label(
        	        master=frame1,
        	        text="0",
        	        bg=BACKGROUND_COLOUR,
					fg=LIGHT,
        	        justify=tk.CENTER,
        	        font=('Arial bold', 15),
					)

		self.score_text.pack(side="top")
		# Frame 2
		frame2 = tk.Frame(self,bg=BACKGROUND_COLOUR,width=50,height=60)
		frame2.pack(side="left", pady=10,padx=10)

		t1 = tk.Label(
        	        master=frame2,
        	        text="UNDOS",
        	        bg=BACKGROUND_COLOUR,
					fg=COLOURS[None],
        	        justify=tk.CENTER,
        	        font=('Arial bold', 20),
        	        # width=5,
                    # height=2
					)

		t1.pack(side="top")
		
		self.undo_text = tk.Label(
        	        master=frame2,
        	        text=MAX_UNDOS,
        	        bg=BACKGROUND_COLOUR,
					fg=LIGHT,
        	        justify=tk.CENTER,
        	        font=('Arial bold', 15),
					)

		self.undo_text.pack(side="top")

		# frame3 = tk.Frame(master,bg="white",width=50,height=60)
		# frame3.pack(side="left", pady=20,padx=20)

		self.new_game_button = tk.Button(
        	        master=self,
        	        text="New Game",
        	        # width=5,
                    # height=2
					)

		self.new_game_button.pack(side="top", pady=10)
		
		self.undo_button = tk.Button(
        	        master=self,
        	        text="Undo Move",
					)

		self.undo_button.pack(side="top")


	def redraw_infos(self, score, undos):
		self.score_text.config(text=score)
		self.undo_text.config(text=undos)

	def set_callbacks(self, new_game_command, undo_command):
		self.undo_button.config(command=undo_command)
		self.new_game_button.config(command=new_game_command)
		

class GameGrid(tk.Canvas):
	def __init__(self,master,**kwargs):
		tk.Canvas.__init__(self,
		master,
		background = BACKGROUND_COLOUR, 
		width = BOARD_WIDTH,
		height = BOARD_HEIGHT
		)
		self.square = {}

	def _get_bbox(self,position):
		column, row = position
		x_min = row * 100 + BUFFER
		y_min = column * 100 + BUFFER
		x_max = x_min + 100 - BUFFER
		y_max = y_min + 100 - BUFFER

		return x_min, y_min, x_max, y_max

	def _get_midpoint(self,position):
		box = self._get_bbox(position)
		x_min, y_min, x_max, y_max = box 
		mid_point = ((x_min + x_max) / 2, (y_min + y_max) / 2)

		return mid_point
		

	def clear(self):
		self.delete("all")

	def redraw(self,tiles):
		self.clear()
		for column in range(NUM_COLS):
			for row in range(NUM_ROWS):
				tile = tiles[column][row]
				if tile == None:
					bg_color = COLOURS[None]
					font_color = ""
					text=""

				else:
					bg_color = COLOURS[tile]
					font_color = FG_COLOURS[tile]
					text=str(tile)

				box = self._get_bbox((column,row))
				x_min, y_min, x_max, y_max = box
				self.square[column,row] = self.create_rectangle(x_min, y_min, x_max, y_max, fill=bg_color, tags="rect", outline="")
				# grid_row.append(t)
				if tile is not None:
					text_box = self._get_midpoint((column,row))
					x, y = text_box
					self.create_text(x, y, font=TILE_FONT, fill=font_color, text=text)

class Game:
	def __init__(self,master):
		self.master = master
		self.master.title("CSSE1001/7030 2022 Semester 2 A3")
		title = tk.Label(
		master=self.master,
		text="2048",
		bg=COLOURS[2048],
		fg=LIGHT,
		justify=tk.CENTER,
		font=TITLE_FONT,
		padx = 10,
		)
		# title.grid(sticky='nswe')
		title.pack(side="top", fill="both")
		self.model = Model()
		self.game_grid = GameGrid(self.master)
		self.game_grid.pack(side="top", fill="both", expand="false")
		self.master.bind("<Key>",self.attempt_move)
		self.statusbar = StatusBar(self.master)
		self.statusbar.pack(side="top")
		self.statusbar.set_callbacks(self.start_new_game, self.undo_previous_move)
		self.draw()
		# master.pack()
		
	def draw(self):
		self.game_grid.redraw(self.model.get_tiles())
		
	def attempt_move(self, event):
		move_command = ["w","a","s","d"]
		if event.keysym in move_command:
			if len(self.model.prev_tiles) == 3:
				self.model.prev_tiles.pop()
			if len(self.model.prev_score) == 3:
				self.model.prev_score.pop()
			self.model.prev_tiles.insert(0, self.model.tiles)
			self.model.prev_score.insert(0, self.model.get_score())
			movement = self.model.attempt_move(event.keysym)
			self.draw()
			won = self.model.has_won()
			if won:
				messagebox.askquestion(
					title=None,
					message= WIN_MESSAGE)
			else:
				self.statusbar.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())
				if movement == True:
					self.master.after(NEW_TILE_DELAY, self.new_tile)
				
	def new_tile(self):
		self.model.add_tile()
		self.draw()
		lose = self.model.has_lost()
		if lose:
			messagebox.askquestion(
				title=None,
				message= LOSS_MESSAGE)
		
	def undo_previous_move(self):
		get_undo = self.model.get_undos_remaining()
		if len(self.model.prev_tiles) >= 1 and get_undo >= 1: 
			undo = self.model.prev_tiles
			score = self.model.prev_score
			self.model.tiles = undo[0]
			self.model.prev_tiles.pop(0)
			self.model.score = score[0]
			self.model.prev_score.pop(0)
			self.model.undos -= 1
			self.draw()
			self.statusbar.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())

	def start_new_game(self):
		self.model = Model()
		self.draw()
		self.statusbar.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())


def play_game(root):
	# Add a docstring and type hints to this function
	# Then write your code here
	Game(root)

if __name__ == '__main__':
	root = tk.Tk()
	play_game(root)
	root.mainloop()



