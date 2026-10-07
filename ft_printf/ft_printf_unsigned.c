/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf_unsigned.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 18:41:39 by sofadl            #+#    #+#             */
/*   Updated: 2025/11/26 18:41:40 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	get_power(unsigned int nbr)
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

static int	get_count(unsigned int nbr)
{
	int	count;

	count = 0;
	while (nbr > 0)
	{
		nbr /= 10;
		count++;
	}
	return (count);
}

int	ft_printf_unsigned(unsigned int nbr)
{
	int		digit_count;
	int		power;
	char	c;

	if (nbr == 0)
	{
		write(1, "0", 1);
		return (1);
	}
	digit_count = get_count(nbr);
	power = get_power(nbr);
	while (power > 0)
	{
		c = (nbr / power) % 10 + '0';
		write(1, &c, 1);
		power /= 10;
	}
	return (digit_count);
}
