/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_hex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 18:49:26 by sofadl            #+#    #+#             */
/*   Updated: 2025/11/26 18:49:27 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_hex(unsigned int nbr, char spec)
{
	char	*hex;
	char	c;
	int		count;

	count = 0;
	if (spec == 'x')
		hex = "0123456789abcdef";
	else
		hex = "0123456789ABCDEF";
	if (nbr >= 16)
		count += ft_print_hex(nbr / 16, spec);
	c = hex[nbr % 16];
	write(1, &c, 1);
	count++;
	return (count);
}
