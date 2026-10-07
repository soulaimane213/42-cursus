/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 03:39:49 by sofadl            #+#    #+#             */
/*   Updated: 2026/01/14 03:39:49 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#ifndef HEADER_H
# define HEADER_H

# include <stdlib.h>
# include <unistd.h>
# include <stddef.h>

typedef struct s_stack
{
	int				value;
	int				index;
	struct s_stack	*next;
}	t_stack;

typedef struct s_vars
{
	int		size;
	int		*origi;
	int		*index;
	int		i;
	t_stack	*a;
	t_stack	*b;
}	t_vars;

int		my_atoi(char **av);
int		check_if_numbers(char **av);
int		check_number(char *arg);
void	add_new(t_stack **a, t_stack *new);
t_stack	*new_node(int number, int value);
int		*parse_input(int argc, char **argv, int *out_size);
int		*get_index(int *org, int size);
void	ft_sort(int *org, int *arr, int size);
void	radix_logic(t_stack **a, t_stack **b, int size);
void	pa(t_stack **a, t_stack **b);
void	pb(t_stack **a, t_stack **b);
void	ra(t_stack **a);
void	error_exit(t_vars *v);
int		is_digit(char c);
void	free_stack(t_stack *stack);
char	*ft_strtok(char *str, const char *delim);
int		ft_is_delim(char c, const char *delim);
int		check_empty_arg(char **av);
void	error_exit_2(void *arr);
#endif
