/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_index.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 03:44:34 by sofadl            #+#    #+#             */
/*   Updated: 2026/01/14 03:44:36 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static void	copy_array(int *org, int *arr, int size)
{
	int	i;

	i = 0;
	while (i < size)
	{
		arr[i] = org[i];
		i++;
	}
}

static void	bubble_sort(int *arr, int size)
{
	int	i;
	int	j;
	int	tmp;

	i = 0;
	while (i < size - 1)
	{
		j = 0;
		while (j < size - i - 1)
		{
			if (arr[j] > arr[j + 1])
			{
				tmp = arr[j];
				arr[j] = arr[j + 1];
				arr[j + 1] = tmp;
			}
			j++;
		}
		i++;
	}
}

void	ft_sort(int *org, int *arr, int size)
{
	copy_array(org, arr, size);
	bubble_sort(arr, size);
}

static int	find_index(int value, int *sorted, int size)
{
	int	i;

	i = 0;
	while (i < size)
	{
		if (value == sorted[i])
			return (i);
		i++;
	}
	return (0);
}

int	*get_index(int *org, int size)
{
	int	*sorted;
	int	*index;
	int	i;

	sorted = malloc(sizeof(int) * size);
	index = malloc(sizeof(int) * size);
	if (!sorted || !index)
		return (NULL);
	ft_sort(org, sorted, size);
	i = 0;
	while (i < size)
	{
		index[i] = find_index(org[i], sorted, size);
		i++;
	}
	free(sorted);
	return (index);
}
