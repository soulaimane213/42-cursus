/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_address.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 18:45:00 by sofadl            #+#    #+#             */
/*   Updated: 2025/11/26 21:58:59 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	print_hex(unsigned long nbr, char *hex)
{
	unsigned long	buffer[16];
	int				j;
	int				i;
	int				count;

	j = 0;
	count = 0;
	while (nbr > 0)
	{
		buffer[j] = nbr % 16;
		nbr /= 16;
		j++;
	}
	i = j - 1;
	while (i >= 0)
	{
		write(1, &hex[buffer[i]], 1);
		count++;
		i--;
	}
	return (count);
}

int	ft_print_address(void *ptr)
{
	char			*hex;
	unsigned long	nbr;
	int				count;

	hex = "0123456789abcdef";
	if (ptr == NULL)
	{
		write(1, "(nil)", 5);
		return (5);
	}
	nbr = (unsigned long)ptr;
	write(1, "0x", 2);
	count = 2;
	count += print_hex(nbr, hex);
	return (count);
}
