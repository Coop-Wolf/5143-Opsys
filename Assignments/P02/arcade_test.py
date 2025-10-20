import arcade

# Constants for the window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_TITLE = "My First Arcade Window"

# Create a window class
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

    # This is called every time the window needs to draw
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Hello Arcade!", 200, 200, arcade.color.WHITE, 24)

# Run the game
def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
