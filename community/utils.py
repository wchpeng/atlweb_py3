def select_page_range(page_range, n):
    if n < 3:
        return page_range[:5]
    elif n > len(page_range)-3:
        return page_range[-5:]
    else:
        return page_range[n-3:n+2]