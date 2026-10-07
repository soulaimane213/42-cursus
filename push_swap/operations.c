/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operations.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 03:20:13 by sofadl            #+#    #+#             */
/*   Updated: 2026/01/14 03:20:14 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "header.h"

void	pa(t_stack **a, t_stack **b)
{
	t_stack	*tmp;

	if (*b == NULL)
		return ;
	tmp = *b;
	*b = (*b)->next;
	tmp->next = *a;
	*a = tmp;
	write(1, "pa\n", 3);
}

void	pb(t_stack **a, t_stack **b)
{
	t_stack	*tmp;

	if (*a == NULL)
		return ;
	tmp = *a;
	*a = (*a)->next;
	tmp->next = *b;
	*b = tmp;
	write(1, "pb\n", 3);
}

void	ra(t_stack **a)
{
	t_stack	*first;
	t_stack	*tmp;

	if (*a == NULL || (*a)->next == NULL)
		return ;
	first = *a;
	*a = first->next;
	tmp = *a;
	while (tmp->next != NULL)
		tmp = tmp->next;
	tmp->next = first;
	first->next = NULL;
	write(1, "ra\n", 3);
}
