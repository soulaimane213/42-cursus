/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 11:39:35 by sofadl            #+#    #+#             */
/*   Updated: 2025/10/29 17:09:19 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include <stdio.h>

static int	digit_count(long int num, int flag)
{
	int	count;

	count = 0;
	if (num == 0)
	{
		count = 1;
		return (count);
	}
	while (num > 0)
	{
		count++;
		num /= 10;
	}
	if (flag < 0)
		count++;
	return (count);
}

static int	get_power(long int num)
{
	int	result;

	result = 1;
	while (num >= 10)
	{
		num /= 10;
		result *= 10;
	}
	return (result);
}

static void	fill_array(char *result, int *i, long int n, int power)
{
	while (power > 0)
	{
		result[*i] = (n / power) % 10 + '0';
		power /= 10;
		(*i)++;
	}
}

static void	set_negative(char *result, int flag, int *i)
{
	if (flag < 0)
	{
		result[0] = '-';
		(*i)++;
	}
}

char	*ft_itoa(int n)
{
	int			i;
	int			digit;
	int			power;
	long int	nbr;
	char		*result;

	i = 0;
	nbr = n;
	if (n < 0)
		nbr *= -1;
	digit = digit_count(nbr, n);
	power = get_power(nbr);
	result = malloc(digit + 1);
	if (!result)
		return (NULL);
	set_negative(result, n, &i);
	fill_array(result, &i, nbr, power);
	result[i] = '\0';
	return (result);
}
