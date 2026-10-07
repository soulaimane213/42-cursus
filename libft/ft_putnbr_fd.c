/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/29 15:17:38 by sofadl            #+#    #+#             */
/*   Updated: 2025/10/29 17:11:21 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <unistd.h>

static int	get_div(int nbr)
{
	int	result;

	result = 1;
	while (nbr > 9)
	{
		nbr /= 10;
		result *= 10;
	}
	return (result);
}

void	ft_putnbr_fd(int n, int fd)
{
	int		the_div;
	int		sec_num;
	char	num;

	if (n == -2147483648)
	{
		write(fd, "-", 1);
		write(fd, "2147483648", 10);
		return ;
	}
	if (n < 0)
	{
		write(fd, "-", 1);
		n *= -1;
	}
	the_div = get_div(n);
	sec_num = n;
	while (the_div > 0)
	{
		num = (sec_num / the_div) % 10 + '0';
		write(fd, &num, 1);
		the_div /= 10;
	}
}
