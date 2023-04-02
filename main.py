from lib.utils import display_art
from window import AppWindow

def main():
  display_art()
  window = AppWindow()
  window.mainloop()


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass
