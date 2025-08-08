from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QSize, QRect

def create_app_icon():
    """
    Creates a simple app icon programmatically.
    Returns a QIcon object that can be used as the application icon.
    """
    # Create a pixmap for the icon
    size = 512
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    # Create a painter to draw on the pixmap
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Draw a rounded rectangle as the background
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(QColor(0, 113, 227)))  # Apple blue color
    painter.drawRoundedRect(QRect(0, 0, size, size), 100, 100)
    
    # Draw a trash can icon
    painter.setPen(QPen(QColor(255, 255, 255), 20))
    painter.setBrush(QBrush(QColor(240, 240, 240)))
    
    # Draw the trash can body
    can_width = size * 0.6
    can_height = size * 0.5
    can_x = (size - can_width) / 2
    can_y = size * 0.35
    painter.drawRoundedRect(QRect(can_x, can_y, can_width, can_height), 20, 20)
    
    # Draw the trash can lid
    lid_width = can_width * 1.2
    lid_height = size * 0.1
    lid_x = (size - lid_width) / 2
    lid_y = can_y - lid_height - 10
    painter.drawRoundedRect(QRect(lid_x, lid_y, lid_width, lid_height), 10, 10)
    
    # Draw the handle on the lid
    handle_width = lid_width * 0.2
    handle_height = lid_height * 0.8
    handle_x = (size - handle_width) / 2
    handle_y = lid_y - handle_height / 2
    painter.drawRoundedRect(QRect(handle_x, handle_y, handle_width, handle_height), 5, 5)
    
    # Draw "X" marks on the trash can
    painter.setPen(QPen(QColor(255, 255, 255), 15))
    
    # First X
    x1 = can_x + can_width * 0.25
    y1 = can_y + can_height * 0.3
    x2 = x1 + can_width * 0.15
    y2 = y1 + can_height * 0.15
    painter.drawLine(x1, y1, x2, y2)
    painter.drawLine(x1, y2, x2, y1)
    
    # Second X
    x1 = can_x + can_width * 0.6
    painter.drawLine(x1, y1, x2 + can_width * 0.35, y2)
    painter.drawLine(x1, y2, x2 + can_width * 0.35, y1)
    
    painter.end()
    
    # Create and return the icon
    return QIcon(pixmap)