#include <ncurses.h>

int main(void){

  initscr();
  noecho();
  curs_set(0);

  printw("Rogue0 - press any key to exit");

  wrefresh(stdscr);

  getch();

  endwin();

  return 0;
}
