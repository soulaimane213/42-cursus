/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: sofadl <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/03 14:36:44 by sofadl            #+#    #+#             */
/*   Updated: 2025/12/04 15:50:13 by sofadl           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*cut_leftover(char *str, int i)
{
	char	*new;

	if (str[i] == '\0')
	{
		free(str);
		return (NULL);
	}
	new = ft_strjoin_gnl(NULL, str + i + 1);
	free(str);
	return (new);
}

char	*extract_line(char **str)
{
	int		i;
	int		j;
	char	*line;

	i = 0;
	j = 0;
	while ((*str)[i] && (*str)[i] != '\n')
		i++;
	line = (char *)malloc(i + 2);
	if (line == NULL)
		return (NULL);
	while (j < i)
	{
		line[j] = (*str)[j];
		j++;
	}
	if ((*str)[i] == '\n')
		line[i++] = '\n';
	line[i] = '\0';
	*str = cut_leftover(*str, i - 1);
	return (line);
}

char	*get_next_line(int fd)
{
	static char	*leftover;
	char		*buffer;
	ssize_t		bytes;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	buffer = (char *)malloc((size_t)BUFFER_SIZE + 1);
	if (buffer == NULL)
		return (NULL);
	while (ft_strchr(leftover, '\n') == NULL)
	{
		bytes = read(fd, buffer, BUFFER_SIZE);
		if (bytes <= 0)
			break ;
		buffer[bytes] = '\0';
		leftover = ft_strjoin_gnl(leftover, buffer);
	}
	free(buffer);
	if (leftover == NULL || leftover[0] == '\0')
	{
		free(leftover);
		leftover = NULL;
		return (NULL);
	}
	return (extract_line(&leftover));
}
