/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 22:20:30 by sofadl            #+#    #+#             */
/*   Updated: 2025/10/31 21:09:27 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *ptr, int value, size_t size)
{
	size_t			i;
	unsigned char	*address;

	i = 0;
	address = (unsigned char *)ptr;
	while (i < size)
	{
		address[i] = value;
		i++;
	}
	return (ptr);
}
