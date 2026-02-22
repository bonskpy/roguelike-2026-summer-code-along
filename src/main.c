#include <ncurses.h>

int main(void){

  int pos_y, pos_x;
  char ch, input;

  pos_y = pos_x = 0;

  initscr();
  noecho();
  curs_set(0);
  wrefresh(stdscr);

  pos_y = COLS / 2;
  pos_x = LINES / 2;
  ch = '@';

  printw("Rogue0\n");
  printw("Player position: %d,%d", pos_y, pos_x);


  mvaddch(pos_y, pos_x, ch);

  while((input = getch()) != 'q'){
    
    switch(input){
      case 'h':
        pos_x -= 1;
        break;
      case 'l':
        pos_x += 1;
        break;
      case 'j':
        pos_y += 1;
        break;
      case 'k':
        pos_y -= 1;
        break;
    }

    clear();
    
    mvaddch(pos_y, pos_x, ch);

    wrefresh(stdscr);

  }

  endwin();

  return 0;
}
