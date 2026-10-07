/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 18:40:02 by sofadl            #+#    #+#             */
/*   Updated: 2025/11/26 18:40:06 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	f_printf(va_list args, int *i, char c)
{
	int	counter;

	counter = 0;
	if (c == 'c')
		counter += ft_print_char(va_arg(args, int));
	else if (c == 's')
		counter += ft_print_string(va_arg(args, char *));
	else if (c == 'p')
		counter += ft_print_address(va_arg(args, void *));
	else if (c == 'd' || c == 'i')
		counter += ft_print_digits(va_arg(args, int));
	else if (c == 'x' || c == 'X')
		counter += ft_print_hex(va_arg(args, unsigned int), c);
	else if (c == '%')
		counter += ft_print_format('%');
	else if (c == 'u')
		counter += ft_printf_unsigned(va_arg(args, unsigned int));
	(void)i;
	return (counter);
}

int	ft_printf(const char *str, ...)
{
	int		i;
	int		counter;
	va_list	args;

	if (str == NULL)
		return (-1);
	va_start(args, str);
	i = 0;
	counter = 0;
	while (str[i])
	{
		if (str[i] == '%')
		{
			i++;
			counter += f_printf(args, &i, str[i]);
		}
		else
			counter += ft_print_char(str[i]);
		i++;
	}
	return (counter);
}
