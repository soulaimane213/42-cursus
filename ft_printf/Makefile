cc = cc
Flags = -WALL -Wextra -Werror
NAME = libftprintf.a

SRCS = ft_print_address.c ft_print_char.c ft_print_digits.c ft_printf.c ft_print_format.c ft_printf_unsigned.c \
ft_print_hex.c ft_print_string.c print_string.c

OBJ = ft_print_address.o ft_print_char.o ft_print_digits.o ft_printf.o ft_print_format.o ft_printf_unsigned.o \
ft_print_hex.o ft_print_string.o 

all: $(NAME)

$(NAME): $(OBJ)
	ar rc $(NAME) $(OBJ)

clean:
	rm -f $(OBJ) 

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY:  clean bonus re fclean all
