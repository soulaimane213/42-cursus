/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/31 19:20:41 by sofadl            #+#    #+#             */
/*   Updated: 2025/10/31 19:20:41 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t			i;
	size_t			j;
	const char		*save_start;

	if (!*little)
		return ((char *)big);
	i = 0;
	while (i < len && big[i])
	{
		if (big[i] == little[0])
		{
			j = 0;
			save_start = &big[i];
			while (big[i + j] && little[j] && (i + j) < len
				&& big[i + j] == little[j])
				j++;
			if (little[j] == '\0')
				return ((char *)save_start);
		}
		i++;
	}
	return (NULL);
}
