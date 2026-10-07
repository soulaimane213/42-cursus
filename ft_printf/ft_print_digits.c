/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_digits.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 18:47:31 by sofadl            #+#    #+#             */
/*   Updated: 2025/11/26 18:47:32 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	get_power(long nbr)
{
	int	result;

	result = 1;
	while (nbr >= 10)
	{
		nbr /= 10;
		result *= 10;
	}
	return (result);
}

int	get_count(long nbr)
{
	int	i;

	i = 0;
	if (nbr == 0)
		return (1);
	while (nbr > 0)
	{
		nbr /= 10;
		i++;
	}
	return (i);
}

int	ft_print_digits(int nbr)
{
	long	num;
	int		power;
	int		digit_count;
	char	c;

	num = nbr;
	digit_count = 0;
	power = 0;
	if (nbr < 0)
	{
		write(1, "-", 1);
		digit_count = 1;
		num = -num;
	}
	digit_count += get_count(num);
	power = get_power(num);
	while (power > 0)
	{
		c = (num / power) % 10 + '0';
		write(1, &c, 1);
		power /= 10;
	}
	return (digit_count);
}
