import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Game"

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        # Only clear the screen at the start of each frame
        self.clear()  
        # Draw everything else here
        arcade.draw_text("Hello Arcade!", 100, 300, arcade.color.WHITE, 24)

def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
