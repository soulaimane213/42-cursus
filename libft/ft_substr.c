/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 18:18:24 by sofadl            #+#    #+#             */
/*   Updated: 2025/10/28 23:32:54 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

static char	*fill_result(char const *start, int len)
{
	int		i;
	char	*string;

	string = malloc(len + 1);
	if (!string)
		return (NULL);
	i = 0;
	while (i < len)
	{
		string[i] = start[i];
		i++;
	}
	string[i] = '\0';
	return (string);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	s_len;
	char	*save_ptr;

	if (!s)
		return (NULL);
	s_len = ft_strlen((char *)s);
	if ((size_t)start >= s_len)
	{
		save_ptr = malloc(1);
		if (!save_ptr)
			return (NULL);
		save_ptr[0] = '\0';
		return (save_ptr);
	}
	if (len > s_len - start)
		len = s_len - start;
	save_ptr = fill_result(&s[start], len);
	return (save_ptr);
}
