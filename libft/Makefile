CC = cc
CFLAGS = -Wall -Wextra -Werror

NAME = libft.a

SRC = ft_isprint.c ft_putendl_fd.c ft_strlcat.c ft_substr.c ft_atoi.c ft_itoa.c \
ft_putnbr_fd.c ft_strlcpy.c ft_tolower.c ft_bzero.c ft_memchr.c ft_putstr_fd.c \
ft_strlen.c ft_toupper.c ft_calloc.c ft_memcmp.c ft_split.c ft_strmapi.c \
ft_isalnum.c ft_memcpy.c ft_strchr.c ft_strncmp.c ft_isalpha.c ft_memmove.c \
ft_strdup.c ft_strnstr.c ft_isascii.c ft_memset.c ft_striteri.c ft_strrchr.c \
ft_isdigit.c ft_putchar_fd.c ft_strjoin.c ft_strtrim.c 


SRCBONUS =  ft_lstadd_front_bonus.c  ft_lstadd_back_bonus.c  ft_lstclear_bonus.c \
ft_lstdelone_bonus.c  ft_lstiter_bonus.c ft_lstlast_bonus.c ft_lstsize_bonus.c ft_lstnew_bonus.c


OBJBONUS = $(SRCBONUS:.c=.o)

OBJ = $(SRC:.c=.o)

all: $(NAME)


bonus: $(OBJ) $(OBJBONUS)
	ar rc $(NAME) $(OBJ) $(OBJBONUS)

$(NAME): $(OBJ)
	ar rc $(NAME) $(OBJ)

clean:
	rm -f $(OBJ) $(OBJBONUS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY:  clean bonus re fclean all
