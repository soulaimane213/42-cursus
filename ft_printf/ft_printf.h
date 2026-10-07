/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 21:45:49 by sofadl            #+#    #+#             */
/*   Updated: 2025/11/26 21:45:55 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <unistd.h>
# include <stdarg.h>

int	ft_print_char(char c);
int	ft_print_string(char *str);
int	ft_print_address(void *ptr);
int	ft_print_digits(int nbr);
int	ft_print_hex(unsigned int nbr, char spec);
int	ft_print_format(char c);
int	ft_printf_unsigned(unsigned int nbr);
int	ft_printf(const char *str, ...);

#endif
