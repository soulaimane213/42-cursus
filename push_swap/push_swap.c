/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 03:25:39 by sofadl            #+#    #+#             */
/*   Updated: 2026/01/14 03:25:43 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "header.h"

static void	init_vars(t_vars *v, int argc, char **argv)
{
	v->origi = NULL;
	v->index = NULL;
	v->a = NULL;
	v->b = NULL;
	v->i = 0;
	v->size = 0;
	v->origi = parse_input(argc, argv, &v->size);
	if (!v->origi || check_empty_arg(argv) == -1)
		error_exit(v);
	v->index = get_index(v->origi, v->size);
	if (!v->index)
		error_exit(v);
	v->i = 0;
}

static void	fill_stack(t_vars *v)
{
	while (v->i < v->size)
	{
		add_new(&v->a, new_node(v->index[v->i], v->origi[v->i]));
		v->i++;
	}
}

int	main(int argc, char **argv)
{
	t_vars	v;

	if (argc < 2)
		return (0);
	init_vars(&v, argc, argv);
	fill_stack(&v);
	radix_logic(&v.a, &v.b, v.size);
	free_stack(v.a);
	free_stack(v.b);
	free(v.origi);
	free(v.index);
	return (0);
}
