/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/14 03:24:41 by sofadl            #+#    #+#             */
/*   Updated: 2026/01/14 03:24:42 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	check_empty_arg(char **av)
{
	int	i;
	int	flag;
	int	j;

	i = 1;
	flag = -1;
	while (av[i])
	{
		flag = -1;
		j = 0;
		if (av[i][j] == 0)
			return (-1);
		while (av[i][j])
		{
			if (av[i][j] != 32)
				flag = 1;
			j++;
		}
		if (flag == -1)
			return (-1);
		i++;
	}
	return (flag);
}

static int	ft_atoi_safe(char *s, int *arr)
{
	long	result;
	int		sign;

	result = 0;
	sign = 1;
	if (*s == '+' || *s == '-')
	{
		if (*s == '-')
			sign = -1;
		s++;
	}
	if (!*s)
		error_exit_2(arr);
	while (*s)
	{
		if (!is_digit(*s))
			error_exit_2(arr);
		result = result * 10 + (*s - '0');
		if ((result * sign) > 2147483647 || (result * sign) < -2147483648)
			error_exit_2(arr);
		s++;
	}
	return ((int)(result * sign));
}

static int	count_tokens(int argc, char **argv)
{
	int		i;
	int		count;
	char	*p;

	i = 1;
	count = 0;
	while (i < argc)
	{
		p = argv[i];
		while (*p)
		{
			while (*p == ' ')
				p++;
			if (*p)
				count++;
			while (*p && *p != ' ')
				p++;
		}
		i++;
	}
	return (count);
}

static void	check_duplicates(int *arr, int size)
{
	int	i;
	int	j;

	i = 0;
	while (i < size)
	{
		j = i + 1;
		while (j < size)
		{
			if (arr[i] == arr[j])
				error_exit_2(arr);
			j++;
		}
		i++;
	}
}

int	*parse_input(int argc, char **argv, int *out_size)
{
	int		*arr;
	int		i;
	int		j;
	char	*token;

	i = 1;
	j = 0;
	*out_size = count_tokens(argc, argv);
	if (*out_size == 0)
		return (NULL);
	arr = malloc(sizeof(int) * (*out_size));
	if (!arr)
		error_exit_2(arr);
	while (i < argc)
	{
		token = ft_strtok(argv[i], " ");
		while (token)
		{
			arr[j++] = ft_atoi_safe(token, arr);
			token = ft_strtok(NULL, " ");
		}
		i++;
	}
	check_duplicates(arr, *out_size);
	return (arr);
}
