import tkinter as tk
import time
import random
import winsound

class Game(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.parent.configure(bg='black')

        
        self.snake=[]
        self.snake_id=[]
        
        self.feed_count=0
        self.fb_id=None
        self.fbx=None
        self.fby=None
        self.fb_color='white'
        self.block_size=50
        self.block_color='green'
        self.game_is_running=False
        self.hit=False
        self.game_is_over=False
        self.speed=0
        self.score_increase=10
        self.score=0
        self.direction='right'
        self.x_blocks=15
        self.y_blocks=10
        self.starting_block=[int(self.x_blocks/2),int(self.y_blocks/2)]
        self.score_text=tk.StringVar()

        
        self.container = tk.Frame(self.parent, width=self.x_blocks*self.block_size, height=self.y_blocks*self.block_size+1.5*self.block_size)
        self.container.grid()
        self.container.grid_propagate(0)
        self.container.columnconfigure(0, weight=1)
        score_frame = tk.Frame(self.container, width=self.x_blocks*self.block_size, height=1.5*self.block_size) #bg='#3f3f3f')
        score_frame.grid(row=0, sticky=tk.NSEW)
        score_frame.grid_propagate(0)
        score_frame.rowconfigure(0, weight=1)
        score_frame.columnconfigure(0, weight=1)
        #score_frame.columnconfigure(1, weight=1)
        self.s1=tk.Label(score_frame, textvariable=self.score_text, font=('Bauhaus 93',24,'bold'),fg='white', bg='black', anchor=tk.E)
        #s2=tk.Label(score_frame, text=str(self.score), font=('Calibri',24,'bold'),fg='white', bg='black', anchor=tk.W)
        self.s1.grid(row=0, column=0, sticky=tk.NSEW)
        #s2.grid(row=0, column=1, sticky=tk.E)
        
#'SCORE: '+'{0:>10}'.format(self.score)
        
        self.canvas = tk.Canvas(self.container, width=self.x_blocks*self.block_size, height=self.y_blocks*self.block_size, bg='#3f3f3f', bd=0, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky=tk.N)
        
        
        self.canvas.bind('<Button-1>', self.gameplay)

        self.canvas.bind_all('<Left>', self.turn_left)
        self.canvas.bind_all('<Right>', self.turn_right)    
        self.canvas.bind_all('<Up>', self.turn_up)        
        self.canvas.bind_all('<Down>', self.turn_down)
#        self.parent.bind_all('<space>', self.pause_game) 


    def create_and_draw_feeding_block(self):
        tfbx=random.randint(0,self.x_blocks-1)
        tfby=random.randint(0,self.y_blocks-1)
        loop_again=0
        while any(((self.snake[i].bx==tfbx and self.snake[i].by==tfby) for i in range(len(self.snake)))):
            tfbx=random.randint(0,self.x_blocks)
            tfby=random.randint(0,self.y_blocks)
        self.fbx=tfbx
        self.fby=tfby
        x1 = self.fbx*self.block_size
        x2 = self.fbx*self.block_size+self.block_size-1
        y1 = self.fby*self.block_size
        y2 = self.fby*self.block_size+self.block_size-1
        self.fb_id=self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.fb_color, outline=self.canvas['bg'])
        
    
    def create_starting_block(self):
        b = Block(self.starting_block[0],self.starting_block[1])
        self.snake.append(b)
        #print(self.snake[0].bx, self.snake[0].by)
        
    
    def create_new_block(self):
        bx = self.snake[-1].bx
        by = self.snake[-1].by
        if self.direction=='right':
            tbx = bx+1; tby = by
        if self.direction=='left':
            tbx = bx-1; tby = by
        if self.direction=='up':
            tbx = bx; tby = by-1
        if self.direction=='down':
            tbx = bx; tby = by+1
        #print(tbx, tby)
        if self.check_tentative_new_block(tbx, tby)=='HIT':
            print('HIT')
        else:
            bx = self.check_tentative_new_block(tbx, tby)[0]
            by = self.check_tentative_new_block(tbx, tby)[1]
            #print(bx, by)
            b = Block(bx, by)
            self.snake.append(b)
        
            
    def check_tentative_new_block(self, tbx, tby):
        if tbx==-1:
            tbx=self.x_blocks-1
        if tbx==self.x_blocks:
            tbx=0
        if tby==-1:
            tby=self.y_blocks-1
        if tby==self.y_blocks:
            tby=0
        for block in self.snake:
            if tbx==block.bx and tby==block.by:
                self.hit=True
                self.game_is_running=False
        return (tbx,tby)
    
    
    def draw_new_block(self):
        x1 = self.snake[-1].bx*self.block_size
        x2 = self.snake[-1].bx*self.block_size+self.block_size-1
        y1 = self.snake[-1].by*self.block_size
        y2 = self.snake[-1].by*self.block_size+self.block_size-1
        b_id=self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.block_color, outline=self.canvas['bg'])
        self.snake_id.append(b_id)
        #print(self.snake_id)
        #print(len(self.snake))
    
    
    def delete_and_undraw_tail_block(self):
        if self.fbx==self.snake[-1].bx and self.fby==self.snake[-1].by:
            self.canvas.delete(self.fb_id)
            self.score+=self.score_increase
            self.score_text.set('SCORE: '+'{0:>10}'.format(self.score))
            self.feed_count+=1
            winsound.PlaySound('arcade_beep.wav', winsound.SND_ASYNC)
            if self.feed_count%5==0:
                self.speed+=1
                self.score_increase+=5
            self.create_and_draw_feeding_block()
        else:
            del self.snake[0]
            self.canvas.delete(self.snake_id[0])
            del self.snake_id[0]
        
        
    def gameplay(self, event):
        if self.game_is_running:
            return
        if self.game_is_over:
            return
        self.score_text.set('SCORE: '+'{0:>10}'.format(self.score))
        self.create_starting_block()
        self.draw_new_block()
        self.create_and_draw_feeding_block()
        self.game_is_running=True
        self.game_action()
                
    def game_action(self):
        #time.sleep(0.5*(4/5)**self.speed)
        if self.game_is_running==False:
            return
        self.create_new_block()
        if self.hit==True:
            self.game_over()
            winsound.PlaySound('arcade_game_over.wav', winsound.SND_ASYNC)
            print("GAME OVER")
            print(f"FINAL SCORE: {self.score}")
        else:
            self.draw_new_block()
            self.delete_and_undraw_tail_block()
            self.parent.update()
            self.parent.after(int(300*(4/5)**self.speed), self.game_action)
    
    def game_over(self):
        self.canvas.create_text(int(self.canvas.winfo_width()/2),int(self.canvas.winfo_height()/2), text='GAME OVER', font=('Bauhaus 93',75,'bold'), fill='red')
        self.game_is_over=True
    
    def pause_game(self, event):
        self.game_is_running = not self.game_is_running
        if self.game_is_running:
            print('START')
        else:
            print('PAUSE')
    
    def change_direction(self, event):
        pass
            
    def turn_right(self, event):
        if self.direction=='up' or self.direction=='down':
            self.direction='right'
            #print(self.direction)
    
    def turn_up(self, event):
        if self.direction=='left' or self.direction=='right':
            self.direction='up'
            #print(self.direction)    
    
    def turn_left(self, event):
        if self.direction=='up' or self.direction=='down':
            self.direction='left'
            #print(self.direction)
            
    def turn_down(self, event):
        if self.direction=='left' or self.direction=='right':
            self.direction='down'
            #print(self.direction)        
            

    
class Block:
    def __init__(self, bx, by):
        self.bx = bx
        self.by = by
        

root=tk.Tk()
app=Game(root)
root.mainloop()
