def format_number(num):
    num = float(num)
    
    if num >= 1_000_000_000:
        return f"{round(num / 1_000_000_000, 1)} млрд."
    elif num >= 1_000_000:
        return f"{round(num / 1_000_000, 1)} млн."
    elif num >= 1_000:
        return f"{round(num / 1_000, 1)} тыс."
    else:
        return str(int(num))