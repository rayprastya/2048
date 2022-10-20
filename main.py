import tkinter as tk

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
		# a = random.randint(0, len(self.tiles)-1)
		# b = random.randint(0, len(self.tiles)-1)
		# while self.tiles[a][b] != None:
		# 	a = random.randint(0, len(self.tiles)-1)
		# 	b = random.randint(0, len(self.tiles)-1)
		# mat[a][b] = 2
		# return mat
		# generate_tile(self.tiles[a][b])

	def move_left(self):
		self.tiles = stack_left(self.tiles)
		merging = combine_left(self.tiles)
		self.score += merging[1]
		self.tiles = merging[0]
		self.tiles = stack_left(self.tiles)
		# self.add_tile()
		print("move left",self.tiles)
	
	def move_right(self):
		self.tiles = reverse(self.tiles)
		self.move_left()
		self.tiles = reverse(self.tiles)
		print("move right",self.tiles)

	def move_up(self):
		self.tiles = transpose(self.tiles)
		self.move_left()
		self.tiles = transpose(self.tiles)
		print("move up",self.tiles)

	def move_down(self):
		self.tiles = transpose(self.tiles)
		self.move_right()
		self.tiles = transpose(self.tiles)
		print("move down",self.tiles)

	def attempt_move(self, move):
		temp_tiles = self.tiles

		if move == UP:
			self.move_up()
		elif move == LEFT:
			self.move_left()
		elif move == DOWN:
			self.move_down()
		elif move == RIGHT:
			self.move_right()
		
		if temp_tiles == self.tiles:
			return False
		else:
			return True

	def get_score(self):
		return self.score

	def get_undos(self):
		return self.undos

	def use_undo(self):
		pass

	def has_won(self):
		pass 

	def has_lost(self):
		pass


class StatusBar(tk.Frame):
	def __init__(self,master,**kwargs):
		tk.Frame.__init__(self,
		master)
		frame1 = tk.Frame(master,bg=BACKGROUND_COLOUR,width=100,height=60)
		frame1.pack(side="left", pady=20,padx=20)

		t = tk.Label(
        	        master=frame1,
        	        text="SCORE",
        	        bg=BACKGROUND_COLOUR,
					fg=LIGHT,
        	        justify=tk.CENTER,
        	        font=('Arial bold', 25),
        	        # width=5,
                    # height=2
					)

		t.pack(side="top")
		
		self.score_text = tk.Label(
        	        master=frame1,
        	        text=0,
        	        bg=BACKGROUND_COLOUR,
					fg=LIGHT,
        	        justify=tk.CENTER,
        	        font=('Arial bold', 25),
					)

		self.score_text.pack(side="top")
		# Frame 2
		frame2 = tk.Frame(master,bg=BACKGROUND_COLOUR,width=100,height=60)
		frame2.pack(side="left", pady=20,padx=20)

		t1 = tk.Label(
        	        master=frame2,
        	        text="UNDOS",
        	        bg=BACKGROUND_COLOUR,
					fg=LIGHT,
        	        justify=tk.CENTER,
        	        font=('Arial bold', 25),
        	        # width=5,
                    # height=2
					)

		t1.pack(side="top")
		
		self.undo_text = tk.Label(
        	        master=frame2,
        	        text=0,
        	        bg=BACKGROUND_COLOUR,
					fg=LIGHT,
        	        justify=tk.CENTER,
        	        font=('Arial bold', 25),
					)

		self.undo_text.pack(side="top")

		frame3 = tk.Frame(master,bg="white",width=100,height=60)
		frame3.pack(side="left", pady=20,padx=20)

		self.new_game_button = tk.Button(
        	        master=frame3,
        	        text="New Game",
        	        command = self.callback,
        	        # width=5,
                    # height=2
					)

		self.new_game_button.pack(side="top", pady=10)
		
		self.undo_button = tk.Button(
        	        master=frame3,
        	        text="Undo Move",
        	        command = self.callback,
					)

		self.undo_button.pack(side="top")


	def redraw_infos(self, score, undos):
		pass
	def set_callback(self, new_game_command, undo_command):
		pass

class GameGrid(tk.Canvas):
	def __init__(self,master,**kwargs):
		tk.Canvas.__init__(self,
		master,
		background = BACKGROUND_COLOUR, 
		width = BOARD_WIDTH,
		height = BOARD_HEIGHT)

		# master.geometry('400x400')
		# self.model = Model()
		# self.model_tiles = self.model.get_tiles()
		self.square = {}
		# self.canvas = tk.Canvas(master, )
		
		# self.create_rectangle(fill=BACKGROUND_COLOUR)
		# self.rect = self.create_rectangle(0, 0, 400, 400, fill='red')
		# self.redraw(self.model_tiles)
	
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
				# cell = tk.Frame(
        	    #     self,
        	    #     bg=COLOURS[None],
        	    #     width=BOARD_WIDTH / NUM_COLS,
        	    #     height=BOARD_HEIGHT / NUM_COLS
        	    # )
				# cell.grid(
        	    #     row=i,
        	    #     column=j,
        	    #     padx=BUFFER,
        	    #     pady=BUFFER
        	    # )
				# t = tk.Label(
        	    #     master=cell,
        	    #     text="",
        	    #     bg=COLOURS[None],
        	    #     justify=tk.CENTER,
        	    #     font=TILE_FONT,
        	    #     width=5,
                #     height=2
				# 	)
				# t.grid()
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
				
			# self.grid_cells.append(grid_row)
		
		# for i in range(NUM_ROWS):
		# 	for j in range(NUM_COLS):
		# 		# self.redraw(self.model_tiles[i][j])
				
		# 		if tile == None:
		# 			self.grid_cells[i][j].configure(text="",bg=COLOURS[None])
		# 		else:
		# 			self.grid_cells[i][j].configure(
		# 				text=str(tile),
		# 				bg=COLOURS[tile],
		# 				fg=FG_COLOURS[tile]
		# 			)

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
		self.draw()
		self.statusbar = StatusBar(self.master)
		self.statusbar.pack(side="top")
		# master.pack()
		
	def draw(self):
		self.game_grid.redraw(self.model.get_tiles())

	def attempt_move(self, event):
		move_command = ["w","a","s","d"]
		if event.keysym in move_command:
			movement = self.model.attempt_move(event.keysym)
			if movement == True:
				self.game_grid.after(NEW_TILE_DELAY, self.new_tile())
				
	def new_tile(self):
		self.model.add_tile()  
		self.draw()

	def undo_previous_move(self):
		pass 

	def start_new_game(self):
		pass


def play_game(root):
	# Add a docstring and type hints to this function
	# Then write your code here
	Game(root)

if __name__ == '__main__':
	root = tk.Tk()
	play_game(root)
	root.mainloop()
