#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>


//Modélisation des pièces du jeu
struct piece
{
  short int val;
};

typedef struct piece piece;


//Caractéristiques des différentes pièces
enum Color
  {
   BLACK = 0,
   WHITE = 1
  };

enum Height
  {
   TALL = 0,
   SHORT = 1
  };

enum Top
  {
   ROUNDED = 0,
   UNROUNDED = 1
  };

enum Shape
  {
   SQUARE = 0,
   CIRCLE = 1
  };


typedef enum Color Color;
typedef enum Height Height;
typedef enum Shape Shape;
typedef enum Top Top;



//Constructeur
piece *constr(Color color, Height height, Top top, Shape shape)
{
  piece *p = malloc(sizeof(piece));
  p->val = 0;
  p->val += color;
  p->val += height << 1;
  p->val += top << 2;
  p->val += shape << 3;
  return p;
}



int compare(piece *p1, piece *p2) //Compare si deux pièces p1 et p2 ont au moins une caractéristique en commun
{
  int v1 = p1->val;
  int v2 = p2->val;
  if ((v1^v2) != 15)
      return true;
  return false;
}


void test()
{
  piece *p = constr(BLACK,TALL ,ROUNDED, CIRCLE);
  piece *p2 = constr(BLACK,SHORT , UNROUNDED, SQUARE);

  if (compare(p2,p) == true)
    printf("true\n");
  else
    printf("false\n");
  
  free(p);
  free(p2);
}


int main()
{
  void()
  return 0;
}



