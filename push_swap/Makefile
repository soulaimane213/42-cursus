NAME = push_swap

CC = cc
CFLAGS = -Wall -Wextra -Werror

SRC = push_swap.c \
      parsing.c \
      radix_logic.c \
      operations.c \
      stack.c \
      get_index.c \
      utilis.c \
      erro_exit.c

OBJ = $(SRC:.c=.o)

HEADER = header.h

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
