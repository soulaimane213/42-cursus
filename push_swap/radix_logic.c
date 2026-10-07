/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_logic.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 03:30:54 by sofadl            #+#    #+#             */
/*   Updated: 2026/01/14 03:30:55 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	radix_logic(t_stack **a, t_stack **b, int size)
{
	int	i;
	int	j;
	int	max_bits;
	int	num;

	max_bits = 0;
	while (((size - 1) >> max_bits) != 0)
		max_bits++;
	i = 0;
	while (i < max_bits)
	{
		j = 0;
		while (j < size)
		{
			num = (*a)->index;
			if (((num >> i) & 1) == 1)
				ra(a);
			else
				pb(a, b);
			j++;
		}
		while (*b != NULL)
			pa(a, b);
		i++;
	}
}
