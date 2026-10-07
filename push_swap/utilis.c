/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utilis.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 04:07:43 by sofadl            #+#    #+#             */
/*   Updated: 2026/01/14 04:07:44 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	error_exit(t_vars *v)
{
	write(2, "Error\n", 6);
	if (v)
	{
		if (v->a)
			free_stack(v->a);
		if (v->b)
			free_stack(v->b);
		if (v->origi)
			free(v->origi);
		if (v->index)
			free(v->index);
	}
	exit(EXIT_FAILURE);
}

int	is_digit(char c)
{
	return (c >= '0' && c <= '9');
}

void	free_stack(t_stack *stack)
{
	t_stack	*tmp;

	while (stack)
	{
		tmp = stack->next;
		free(stack);
		stack = tmp;
	}
}

char	*ft_strtok(char *str, const char *delim)
{
	static char	*save;
	char		*token;

	if (str)
		save = str;
	if (!save || *save == '\0')
		return (NULL);
	while (*save && ft_is_delim(*save, delim))
		save++;
	if (*save == '\0')
		return (NULL);
	token = save;
	while (*save && !ft_is_delim(*save, delim))
		save++;
	if (*save)
	{
		*save = '\0';
		save++;
	}
	return (token);
}

int	ft_is_delim(char c, const char *delim)
{
	while (*delim)
	{
		if (c == *delim)
			return (1);
		delim++;
	}
	return (0);
}
