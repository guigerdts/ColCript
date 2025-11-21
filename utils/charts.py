# utils/charts.py - Gráficas ASCII para terminal

def create_bar_chart(data, max_width=50, show_values=True):
    """
    Crea un gráfico de barras ASCII horizontal
    data: lista de tuplas (label, value)
    """
    if not data:
        return "No hay datos para mostrar"
    
    # Encontrar valor máximo
    max_value = max(value for _, value in data)
    
    if max_value == 0:
        max_value = 1
    
    lines = []
    
    for label, value in data:
        # Calcular ancho de la barra
        bar_width = int((value / max_value) * max_width)
        bar = "█" * bar_width
        
        # Formatear label (truncar si es muy largo)
        short_label = label[:20] + "..." if len(label) > 20 else label
        short_label = short_label.ljust(23)
        
        # Formatear valor
        if show_values:
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = f"{value}"
            
            line = f"{short_label} {bar} {value_str}"
        else:
            line = f"{short_label} {bar}"
        
        lines.append(line)
    
    return "\n".join(lines)

def create_progress_bar(current, total, width=40, label=""):
    """
    Crea una barra de progreso
    """
    if total == 0:
        percentage = 0
    else:
        percentage = (current / total) * 100
    
    filled = int((current / total) * width) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    
    if label:
        return f"{label}: [{bar}] {percentage:.2f}%"
    else:
        return f"[{bar}] {percentage:.2f}%"

def create_distribution_chart(ranges, width=50):
    """
    Crea un gráfico de distribución por rangos
    ranges: lista de tuplas (rango_nombre, cantidad)
    """
    return create_bar_chart(ranges, width, show_values=True)

def create_percentage_bar(label, percentage, width=40):
    """
    Crea una barra de porcentaje simple
    """
    filled = int((percentage / 100) * width)
    bar = "█" * filled + "░" * (width - filled)
    
    return f"{label.ljust(25)} [{bar}] {percentage:.2f}%"

def create_sparkline(values, height=5):
    """
    Crea un mini gráfico de línea (sparkline)
    """
    if not values or len(values) < 2:
        return "Datos insuficientes"
    
    min_val = min(values)
    max_val = max(values)
    
    if max_val == min_val:
        return "▄" * len(values)
    
    # Símbolos de diferentes alturas
    blocks = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    
    sparkline = ""
    for value in values:
        # Normalizar valor
        normalized = (value - min_val) / (max_val - min_val)
        block_index = int(normalized * (len(blocks) - 1))
        sparkline += blocks[block_index]
    
    return sparkline

def print_table(headers, rows, col_widths=None):
    """
    Imprime una tabla formateada
    """
    if not col_widths:
        col_widths = [15] * len(headers)
    
    # Separador
    separator = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    
    # Header
    header_row = "|"
    for i, header in enumerate(headers):
        header_row += f" {header.ljust(col_widths[i])} |"
    
    # Imprimir tabla
    lines = [separator, header_row, separator]
    
    for row in rows:
        row_str = "|"
        for i, cell in enumerate(row):
            cell_str = str(cell)[:col_widths[i]].ljust(col_widths[i])
            row_str += f" {cell_str} |"
        lines.append(row_str)
    
    lines.append(separator)
    
    return "\n".join(lines)

# Test
if __name__ == "__main__":
    print("\n📊 Probando gráficas ASCII...\n")
    
    # Barra de progreso
    print("1. Barra de progreso:")
    print(create_progress_bar(150, 21000000, label="CLC en circulación"))
    print()
    
    # Gráfico de barras
    print("2. Top Wallets:")
    wallets = [
        ("Guillo1", 90),
        ("Bob", 70.5),
        ("Alice", 29.5),
        ("Katrin1", 10)
    ]
    print(create_bar_chart(wallets))
    print()
    
    # Porcentajes
    print("3. Distribución de riqueza:")
    print(create_percentage_bar("Top 1%", 44.77))
    print(create_percentage_bar("Top 10%", 80.09))
    print()
    
    # Tabla
    print("4. Tabla de estadísticas:")
    headers = ["Métrica", "Valor"]
    rows = [
        ["Bloques", "5"],
        ["Transacciones", "7"],
        ["Fees totales", "1.0 CLC"],
        ["Mineros", "3"]
    ]
    print(print_table(headers, rows, [20, 15]))
    print()
    
    # Sparkline
    print("5. Tendencia de bloques:")
    block_times = [2.85, 2.16, 0.82, 0.26, 0.30]
    print(f"Tiempos: {create_sparkline(block_times)}")
    print()
    
    print("✅ Gráficas funcionando\n")
