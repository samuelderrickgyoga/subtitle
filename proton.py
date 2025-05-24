import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QPushButton, QSizePolicy, QGridLayout, QFrame,
                             QTabWidget, QProgressBar, QToolTip)
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon, QPixmap
import pyqtgraph.opengl as gl
import networkx as nx


class ProtonSmartCartViz(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup UI
        self.setWindowTitle("Proton Smart Solar-Powered Golf Cart Pipeline")
        self.setMinimumSize(1200, 800)
        
        # Set dark theme with blue accents
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QLabel {
                color: #cdd6f4;
                font-size: 14px;
            }
            QComboBox {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #7f849c;
                border-radius: 5px;
                padding: 5px;
                min-width: 6em;
            }
            QComboBox:hover {
                border: 1px solid #89b4fa;
            }
            QComboBox QAbstractItemView {
                background-color: #313244;
                color: #cdd6f4;
                selection-background-color: #89b4fa;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QFrame {
                border: 1px solid #7f849c;
                border-radius: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #7f849c;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #7f849c;
                border-bottom-color: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QProgressBar {
                border: 1px solid #7f849c;
                border-radius: 5px;
                text-align: center;
                background-color: #313244;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 5px;
            }
        """)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create header
        self.create_header()
        
        # Create tab widget for different views
        self.create_tab_widget()
        
        # Create controls
        self.create_controls()
        
        # Setup data and state
        self.setup_data()
        
        # Setup timers for animations
        self.setup_timers()
    
    def create_header(self):
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("Proton Smart Solar-Powered Golf Cart")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #89b4fa;")
        
        subtitle_label = QLabel("Interactive Pipeline Visualization")
        subtitle_label.setStyleSheet("font-size: 16px; color: #a6adc8;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)
        
        self.main_layout.addWidget(header_frame)
    
    def create_tab_widget(self):
        self.tab_widget = QTabWidget()
        
        # Create tabs for different views
        self.overview_tab = QWidget()
        self.electrical_tab = QWidget()
        self.software_tab = QWidget()
        self.mechanical_tab = QWidget()
        self.comms_tab = QWidget()
        self.gantt_tab = QWidget()
        
        # Add tabs to widget
        self.tab_widget.addTab(self.overview_tab, "Pipeline Overview")
        self.tab_widget.addTab(self.electrical_tab, "Electrical View")
        self.tab_widget.addTab(self.software_tab, "Software View")
        self.tab_widget.addTab(self.mechanical_tab, "Mechanical View")
        self.tab_widget.addTab(self.comms_tab, "Communication Layer")
        self.tab_widget.addTab(self.gantt_tab, "Project Timeline")
        
        # Setup each tab
        self.setup_overview_tab()
        self.setup_electrical_tab()
        self.setup_software_tab()
        self.setup_mechanical_tab()
        self.setup_comms_tab()
        self.setup_gantt_tab()
        
        self.main_layout.addWidget(self.tab_widget)
    
    def setup_overview_tab(self):
        layout = QVBoxLayout(self.overview_tab)
        
        # Create pipeline visualization
        pipeline_frame = QFrame()
        pipeline_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pipeline_layout = QVBoxLayout(pipeline_frame)
        
        # Create title
        pipeline_title = QLabel("Development Pipeline")
        pipeline_title.setAlignment(Qt.AlignCenter)
        pipeline_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #89b4fa;")
        pipeline_layout.addWidget(pipeline_title)
        
        # Create pipeline visualization widget
        self.pipeline_view = pg.GraphicsLayoutWidget()
        self.pipeline_view.setBackground('#313244')
        pipeline_layout.addWidget(self.pipeline_view)
        
        # Add to tab layout
        layout.addWidget(pipeline_frame)
        
        # Create system components grid
        components_frame = QFrame()
        components_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        components_layout = QGridLayout(components_frame)
        
        # Create component blocks
        self.create_component_blocks(components_layout)
        
        # Add to tab layout
        layout.addWidget(components_frame)
    
    def create_component_blocks(self, layout):
        # Define the main components of the golf cart
        components = [
            ("Concept & Design", "Requirements, team roles, research, sketches", 0, 0),
            ("CAD & Prototyping", "Structural and mechanical designs", 0, 1),
            ("Embedded Systems", "Microcontrollers, sensors, actuators, dashboard", 0, 2),
            ("Power System", "Solar panel, battery pack, charge controller", 1, 0),
            ("Software Layer", "Dashboard UI, diagnostics, web/app interface", 1, 1),
            ("Communication Layer", "Bluetooth, Wi-Fi, GSM, GPS", 1, 2),
            ("Security & Auth", "RFID, Fingerprint, secure gear shift, tracking", 2, 0),
            ("Diagnostics & Testing", "Real-time metrics, incline testing, motor stress tests", 2, 1),
            ("Deployment & Evaluation", "Field testing, regulatory compliance, feedback loop", 2, 2)
        ]
        
        self.component_frames = {}
        
        for title, desc, row, col in components:
            component_frame = QFrame()
            component_frame.setStyleSheet("background-color: #313244;")
            component_layout = QVBoxLayout(component_frame)
            
            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: bold; color: #89b4fa; font-size: 14px;")
            title_label.setAlignment(Qt.AlignCenter)
            
            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignCenter)
            
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(np.random.randint(0, 101))  # Random progress for demo
            
            component_layout.addWidget(title_label)
            component_layout.addWidget(desc_label)
            component_layout.addWidget(progress)
            
            layout.addWidget(component_frame, row, col)
            self.component_frames[title] = {
                'frame': component_frame,
                'progress': progress
            }
    
    def setup_electrical_tab(self):
        layout = QVBoxLayout(self.electrical_tab)
        
        # Create electrical system visualization
        electrical_frame = QFrame()
        electrical_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        electrical_layout = QVBoxLayout(electrical_frame)
        
        # Create title
        electrical_title = QLabel("Electrical System Architecture")
        electrical_title.setAlignment(Qt.AlignCenter)
        electrical_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #89b4fa;")
        electrical_layout.addWidget(electrical_title)
        
        # Create electrical diagram widget
        self.electrical_view = pg.GraphicsLayoutWidget()
        self.electrical_view.setBackground('#313244')
        electrical_layout.addWidget(self.electrical_view)
        
        # Add to tab layout
        layout.addWidget(electrical_frame)
        
        # Create electrical components details
        details_frame = QFrame()
        details_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        details_frame.setFixedHeight(200)
        details_layout = QGridLayout(details_frame)
        
        # Add electrical component details
        components = [
            ("Solar Panel", "100W monocrystalline", "85%"),
            ("Battery Pack", "48V 20Ah LiFePO4", "90%"),
            ("Charge Controller", "MPPT 60A", "75%"),
            ("Motor Controller", "500W BLDC Controller", "80%"),
            ("Dashboard Display", "7\" LCD Touch Panel", "65%")
        ]
        
        for i, (name, spec, progress) in enumerate(components):
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: bold;")
            
            spec_label = QLabel(spec)
            
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(int(progress[:-1]))
            
            details_layout.addWidget(name_label, i, 0)
            details_layout.addWidget(spec_label, i, 1)
            details_layout.addWidget(progress_bar, i, 2)
        
        # Add to tab layout
        layout.addWidget(details_frame)
    
    def setup_software_tab(self):
        layout = QVBoxLayout(self.software_tab)
        
        # Create software architecture visualization
        software_frame = QFrame()
        software_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        software_layout = QVBoxLayout(software_frame)
        
        # Create title
        software_title = QLabel("Software Architecture")
        software_title.setAlignment(Qt.AlignCenter)
        software_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #89b4fa;")
        software_layout.addWidget(software_title)
        
        # Create software diagram widget
        self.software_view = pg.GraphicsLayoutWidget()
        self.software_view.setBackground('#313244')
        software_layout.addWidget(self.software_view)
        
        # Add to tab layout
        layout.addWidget(software_frame)
        
        # Create software stack details
        stack_frame = QFrame()
        stack_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        stack_frame.setFixedHeight(200)
        stack_layout = QGridLayout(stack_frame)
        
        # Add software stack details
        components = [
            ("Dashboard UI", "Flutter/Dart", "70%"),
            ("Firmware", "C/C++ (ESP32)", "85%"),
            ("Mobile App", "React Native", "60%"),
            ("Cloud Backend", "Node.js/Express", "50%"),
            ("Analytics", "Python/TensorFlow", "40%")
        ]
        
        for i, (name, tech, progress) in enumerate(components):
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: bold;")
            
            tech_label = QLabel(tech)
            
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(int(progress[:-1]))
            
            stack_layout.addWidget(name_label, i, 0)
            stack_layout.addWidget(tech_label, i, 1)
            stack_layout.addWidget(progress_bar, i, 2)
        
        # Add to tab layout
        layout.addWidget(stack_frame)
    
    def setup_mechanical_tab(self):
        layout = QVBoxLayout(self.mechanical_tab)
        
        # Create mechanical system visualization
        mechanical_frame = QFrame()
        mechanical_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mechanical_layout = QVBoxLayout(mechanical_frame)
        
        # Create title
        mechanical_title = QLabel("Mechanical Design")
        mechanical_title.setAlignment(Qt.AlignCenter)
        mechanical_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #89b4fa;")
        mechanical_layout.addWidget(mechanical_title)
        
        # Create 3D model view
        self.mechanical_view = gl.GLViewWidget()
        self.mechanical_view.setCameraPosition(distance=40)
        self.mechanical_view.setBackgroundColor('#313244')
        mechanical_layout.addWidget(self.mechanical_view)
        
        # Add to tab layout
        layout.addWidget(mechanical_frame)
        
        # Create mechanical components details
        details_frame = QFrame()
        details_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        details_frame.setFixedHeight(200)
        details_layout = QGridLayout(details_frame)
        
        # Add mechanical component details
        components = [
            ("Chassis", "Aluminum alloy frame", "95%"),
            ("Suspension", "Independent front suspension", "80%"),
            ("Seating", "2-person ergonomic design", "90%"),
            ("Solar Roof", "Integrated panel mount", "75%"),
            ("Steering", "Electric power steering", "85%")
        ]
        
        for i, (name, spec, progress) in enumerate(components):
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: bold;")
            
            spec_label = QLabel(spec)
            
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(int(progress[:-1]))
            
            details_layout.addWidget(name_label, i, 0)
            details_layout.addWidget(spec_label, i, 1)
            details_layout.addWidget(progress_bar, i, 2)
        
        # Add to tab layout
        layout.addWidget(details_frame)
    
    def setup_comms_tab(self):
        layout = QVBoxLayout(self.comms_tab)
        
        # Create communication system visualization
        comms_frame = QFrame()
        comms_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        comms_layout = QVBoxLayout(comms_frame)
        
        # Create title
        comms_title = QLabel("Communication Layer Architecture")
        comms_title.setAlignment(Qt.AlignCenter)
        comms_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #89b4fa;")
        comms_layout.addWidget(comms_title)
        
        # Create communication diagram widget
        self.comms_view = pg.GraphicsLayoutWidget()
        self.comms_view.setBackground('#313244')
        comms_layout.addWidget(self.comms_view)
        
        # Add to tab layout
        layout.addWidget(comms_frame)
        
        # Create communication protocols details
        protocols_frame = QFrame()
        protocols_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        protocols_frame.setFixedHeight(200)
        protocols_layout = QGridLayout(protocols_frame)
        
        # Add communication protocols details
        components = [
            ("Bluetooth", "BLE 5.0 for mobile app connection", "90%"),
            ("Wi-Fi", "802.11ac for firmware updates", "85%"),
            ("GPS", "NEO-6M module for location tracking", "80%"),
            ("GSM", "SIM800L for remote monitoring", "70%"),
            ("CAN Bus", "Internal component communication", "95%")
        ]
        
        for i, (name, desc, progress) in enumerate(components):
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: bold;")
            
            desc_label = QLabel(desc)
            
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(int(progress[:-1]))
            
            protocols_layout.addWidget(name_label, i, 0)
            protocols_layout.addWidget(desc_label, i, 1)
            protocols_layout.addWidget(progress_bar, i, 2)
        
        # Add to tab layout
        layout.addWidget(protocols_frame)
    
    def setup_gantt_tab(self):
        layout = QVBoxLayout(self.gantt_tab)
        
        # Create Gantt chart visualization
        gantt_frame = QFrame()
        gantt_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        gantt_layout = QVBoxLayout(gantt_frame)
        
        # Create title
        gantt_title = QLabel("Project Timeline")
        gantt_title.setAlignment(Qt.AlignCenter)
        gantt_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #89b4fa;")
        gantt_layout.addWidget(gantt_title)
        
        # Create Gantt chart widget
        self.gantt_view = pg.PlotWidget()
        self.gantt_view.setBackground('#313244')
        self.gantt_view.showGrid(x=True, y=True, alpha=0.3)
        gantt_layout.addWidget(self.gantt_view)
        
        # Add to tab layout
        layout.addWidget(gantt_frame)
        
        # Create milestone details
        milestone_frame = QFrame()
        milestone_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        milestone_frame.setFixedHeight(200)
        milestone_layout = QGridLayout(milestone_frame)
        
        # Add milestone details
        milestones = [
            ("Requirements Gathering", "Completed", "100%"),
            ("Design Phase", "Completed", "100%"),
            ("Prototype Development", "In Progress", "75%"),
            ("Testing & Validation", "In Progress", "40%"),
            ("Production", "Not Started", "0%")
        ]
        
        for i, (name, status, progress) in enumerate(milestones):
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: bold;")
            
            status_label = QLabel(status)
            if status == "Completed":
                status_label.setStyleSheet("color: #a6e3a1;")  # Green
            elif status == "In Progress":
                status_label.setStyleSheet("color: #f9e2af;")  # Yellow
            else:
                status_label.setStyleSheet("color: #f38ba8;")  # Red
            
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(int(progress[:-1]))
            
            milestone_layout.addWidget(name_label, i, 0)
            milestone_layout.addWidget(status_label, i, 1)
            milestone_layout.addWidget(progress_bar, i, 2)
        
        # Add to tab layout
        layout.addWidget(milestone_frame)
    
    def create_controls(self):
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        
        # Create view mode selector
        viz_mode_label = QLabel("Visualization Mode:")
        self.viz_mode_combo = QComboBox()
        self.viz_mode_combo.addItems([
            "System Overview", 
            "Component Details",
            "Data Flow",
            "3D Model"
        ])
        self.viz_mode_combo.currentIndexChanged.connect(self.change_viz_mode)
        
        # Create component selector
        component_label = QLabel("Component Focus:")
        self.component_combo = QComboBox()
        self.component_combo.addItems([
            "All Components",
            "Power System",
            "Chassis & Mechanical",
            "Control Electronics",
            "Software & UI",
            "Communication"
        ])
        self.component_combo.currentIndexChanged.connect(self.change_component_focus)
        
        # Create status filter
        status_label = QLabel("Status Filter:")
        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "All Statuses",
            "Not Started",
            "In Progress",
            "Completed"
        ])
        self.status_combo.currentIndexChanged.connect(self.filter_by_status)
        
        # Create export button
        self.export_btn = QPushButton("Export Diagram")
        self.export_btn.clicked.connect(self.export_diagram)
        
        # Add widgets to layout
        controls_layout.addWidget(viz_mode_label)
        controls_layout.addWidget(self.viz_mode_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(component_label)
        controls_layout.addWidget(self.component_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(status_label)
        controls_layout.addWidget(self.status_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(self.export_btn)
        
        self.main_layout.addWidget(controls_frame)
    
    def setup_data(self):
        # Initialize data structures for visualization
        self.is_running = False
        self.current_frame = 0
        
        # Setup pipeline visualization
        self.setup_pipeline_viz()
        
        # Setup electrical system visualization
        self.setup_electrical_viz()
        
        # Setup software architecture visualization
        self.setup_software_viz()
        
        # Setup mechanical 3D model
        self.setup_mechanical_viz()
        
        # Setup communication system visualization
        self.setup_comms_viz()
        
        # Setup Gantt chart
        self.setup_gantt_viz()
    
    def setup_pipeline_viz(self):
        # Create pipeline visualization
        pipeline_plot = self.pipeline_view.addPlot()
        pipeline_plot.hideAxis('left')
        pipeline_plot.hideAxis('bottom')
        
        # Define stages in the pipeline
        stages = [
            "Concept", "Design", "Prototype", "Testing", "Production", "Deployment"
        ]
        
        # Add connection lines
        for i in range(len(stages) - 1):
            line = pg.PlotCurveItem(
                x=[i, i+1],
                y=[0, 0],
                pen=pg.mkPen(color='#7f849c', width=3)
            )
            pipeline_plot.addItem(line)
        
        # Add stage nodes
        self.pipeline_nodes = []
        for i in range(len(stages)):
            node = pg.ScatterPlotItem()
            node.addPoints([i], [0], size=30, brush=pg.mkBrush('#89b4fa'))
            pipeline_plot.addItem(node)
            self.pipeline_nodes.append(node)
            
            # Add node labels
            text = pg.TextItem(stages[i], anchor=(0.5, 0), color='#cdd6f4')
            text.setPos(i, -0.2)
            pipeline_plot.addItem(text)
        
        # Set plot range
        pipeline_plot.setXRange(-0.5, len(stages) - 0.5)
        pipeline_plot.setYRange(-1, 1)
    
    def setup_electrical_viz(self):
        # Create electrical system visualization
        electrical_plot = self.electrical_view.addPlot()
        electrical_plot.hideAxis('left')
        electrical_plot.hideAxis('bottom')
        
        # Create a network diagram for electrical components
        # Solar Panel -> Charge Controller -> Battery -> Motor Controller -> Motor
        
        # Define node positions
        positions = {
            'Solar Panel': (0, 0),
            'Charge Controller': (1, 0),
            'Battery': (2, 0),
            'Motor Controller': (3, 0),
            'Motor': (4, 0),
            'Dashboard': (2, 1),
            'Sensors': (1, -1),
            'Lights': (3, -1)
        }
        
        # Add nodes
        self.electrical_nodes = {}
        for name, pos in positions.items():
            node = pg.ScatterPlotItem()
            node.addPoints([pos[0]], [pos[1]], size=30, brush=pg.mkBrush('#89b4fa'))
            electrical_plot.addItem(node)
            
            # Add node labels
            text = pg.TextItem(name, anchor=(0.5, 0), color='#cdd6f4')
            text.setPos(pos[0], pos[1] - 0.2)
            electrical_plot.addItem(text)
            
            self.electrical_nodes[name] = node
        
        # Add connections
        connections = [
            ('Solar Panel', 'Charge Controller'),
            ('Charge Controller', 'Battery'),
            ('Battery', 'Motor Controller'),
            ('Motor Controller', 'Motor'),
            ('Battery', 'Dashboard'),
            ('Sensors', 'Motor Controller'),
            ('Battery', 'Lights')
        ]
        
        for src, dst in connections:
            src_pos = positions[src]
            dst_pos = positions[dst]
            
            line = pg.PlotCurveItem(
                x=[src_pos[0], dst_pos[0]],
                y=[src_pos[1], dst_pos[1]],
                pen=pg.mkPen(color='#7f849c', width=2)
            )
            electrical_plot.addItem(line)
        
        # Set plot range
        electrical_plot.setXRange(-1, 5)
        electrical_plot.setYRange(-1.5, 1.5)
    
# Fix for the QGraphicsRectItem error
# Replace the setup_software_viz method with this corrected version:

    def setup_software_viz(self):
        # Create software architecture visualization
        software_plot = self.software_view.addPlot()
        software_plot.hideAxis('left')
        software_plot.hideAxis('bottom')
        
        # Create a layered architecture diagram
        
        # Define layer positions
        layers = [
            ('UI Layer', 0),
            ('Application Layer', 1),
            ('Communication Layer', 2),
            ('Hardware Abstraction', 3),
            ('Firmware', 4)
        ]
        
        # Add layers as horizontal bars
        for name, y_pos in layers:
            # Create rectangle for layer using QGraphicsRectItem from QtWidgets
            from PyQt5.QtWidgets import QGraphicsRectItem
            from PyQt5.QtCore import QRectF
            from PyQt5.QtGui import QPen, QBrush, QColor
            
            rect = QGraphicsRectItem(QRectF(0, y_pos - 0.4, 5, 0.8))
            rect.setPen(QPen(QColor('#7f849c')))
            rect.setBrush(QBrush(QColor('#313244')))
            software_plot.addItem(rect)
            
            # Add layer label
            text = pg.TextItem(name, anchor=(0.5, 0.5), color='#cdd6f4')
            text.setPos(2.5, y_pos)
            software_plot.addItem(text)
        
        # Add components within layers
        components = [
            ('Dashboard UI', 0, 1),
            ('Mobile App', 0, 4),
            ('User Settings', 1, 1),
            ('Diagnostics', 1, 2.5),
            ('Analytics', 1, 4),
            ('Bluetooth', 2, 1),
            ('GSM/GPS', 2, 4),
            ('Sensors API', 3, 1),
            ('Motor Control', 3, 2.5),
            ('Power Management', 3, 4),
            ('ESP32 Core', 4, 2.5)
        ]
        
        for name, y_pos, x_pos in components:
            # Add component node
            node = pg.ScatterPlotItem()
            node.addPoints([x_pos], [y_pos], size=15, brush=pg.mkBrush('#89b4fa'))
            software_plot.addItem(node)
            
            # Add component label
            text = pg.TextItem(name, anchor=(0.5, -0.5), color='#cdd6f4')
            text.setPos(x_pos, y_pos)
            software_plot.addItem(text)
        
        # Set plot range
        software_plot.setXRange(-0.5, 5.5)
        software_plot.setYRange(-0.5, 4.5)

    
    def setup_mechanical_viz(self):
        # Create a 3D model visualization of the golf cart
        
        # Add a grid for reference
        grid = gl.GLGridItem()
        grid.setSize(50, 50, 1)
        grid.setSpacing(5, 5, 0)
        self.mechanical_view.addItem(grid)
        
        # Create a simplified 3D model of the golf cart
        
        # Chassis (base)
        chassis_points = np.array([
            [-10, -5, 0], [10, -5, 0], [10, 5, 0], [-10, 5, 0],  # Bottom
            [-10, -5, 3], [10, -5, 3], [10, 5, 3], [-10, 5, 3],  # Top
        ])
        
        chassis_faces = np.array([
            [0, 1, 2], [0, 2, 3],  # Bottom
            [4, 5, 6], [4, 6, 7],  # Top
            [0, 1, 5], [0, 5, 4],  # Front
            [1, 2, 6], [1, 6, 5],  # Right
            [2, 3, 7], [2, 7, 6],  # Back
            [3, 0, 4], [3, 4, 7]   # Left
        ])
        
        chassis_colors = np.ones((len(chassis_faces), 4)) * np.array([0.3, 0.5, 0.8, 0.8])
        
        self.chassis_mesh = gl.GLMeshItem(
            vertexes=chassis_points,
            faces=chassis_faces,
            faceColors=chassis_colors,
            smooth=False
        )
        self.mechanical_view.addItem(self.chassis_mesh)
        
        # Solar roof
        roof_points = np.array([
            [-9, -4.5, 3], [9, -4.5, 3], [9, 4.5, 3], [-9, 4.5, 3],  # Bottom
            [-9, -4.5, 3.5], [9, -4.5, 3.5], [9, 4.5, 3.5], [-9, 4.5, 3.5],  # Top
        ])
        
        roof_faces = np.array([
            [0, 1, 2], [0, 2, 3],  # Bottom
            [4, 5, 6], [4, 6, 7],  # Top
            [0, 1, 5], [0, 5, 4],  # Front
            [1, 2, 6], [1, 6, 5],  # Right
            [2, 3, 7], [2, 7, 6],  # Back
            [3, 0, 4], [3, 4, 7]   # Left
        ])
        
        roof_colors = np.ones((len(roof_faces), 4)) * np.array([0.1, 0.2, 0.4, 0.9])
        
        self.roof_mesh = gl.GLMeshItem(
            vertexes=roof_points,
            faces=roof_faces,
            faceColors=roof_colors,
            smooth=False
        )
        self.mechanical_view.addItem(self.roof_mesh)
        
        # Wheels (simplified as mesh cylinders since GLCylinderItem is not available)
        self.wheels = []
        wheel_positions = [
            [-7, -5, 1.5],  # Front left
            [7, -5, 1.5],   # Front right
            [-7, 5, 1.5],   # Rear left
            [7, 5, 1.5]     # Rear right
        ]
        
        # Create a cylinder mesh manually
        def create_cylinder_mesh(radius, height, sides):
            vertices = []
            faces = []
            colors = []
            
            # Create top and bottom circles
            for i in range(sides):
                angle = 2 * np.pi * i / sides
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                vertices.append([x, y, 0])  # Bottom circle
                vertices.append([x, y, height])  # Top circle
            
            # Create faces (triangles)
            for i in range(sides):
                # Get indices for current and next vertices
                i0 = i * 2
                i1 = i * 2 + 1
                i2 = (i * 2 + 2) % (sides * 2)
                i3 = (i * 2 + 3) % (sides * 2)
                
                # Add side faces (2 triangles per side)
                faces.append([i0, i2, i1])
                faces.append([i1, i2, i3])
                
                # Add colors for these faces
                colors.append([0.2, 0.2, 0.2, 1.0])
                colors.append([0.2, 0.2, 0.2, 1.0])
            
            # Add bottom and top faces
            bottom_center_idx = len(vertices)
            vertices.append([0, 0, 0])  # Bottom center
            top_center_idx = len(vertices)
            vertices.append([0, 0, height])  # Top center
            
            for i in range(sides):
                i0 = i * 2  # Bottom circle vertex
                i2 = (i * 2 + 2) % (sides * 2)  # Next bottom circle vertex
                
                # Add bottom face
                faces.append([bottom_center_idx, i2, i0])
                colors.append([0.2, 0.2, 0.2, 1.0])
                
                # Add top face
                i1 = i * 2 + 1  # Top circle vertex
                i3 = (i * 2 + 3) % (sides * 2)  # Next top circle vertex
                faces.append([top_center_idx, i1, i3])
                colors.append([0.2, 0.2, 0.2, 1.0])
            
            return np.array(vertices), np.array(faces), np.array(colors)
        
        # Create wheels
        for pos in wheel_positions:
            # Create cylinder mesh
            wheel_verts, wheel_faces, wheel_colors = create_cylinder_mesh(1.5, 1, 20)
            
            # Rotate to horizontal orientation (90 degrees around Y axis)
            # Apply rotation matrix to vertices
            rotation = np.array([
                [0, 0, 1],
                [0, 1, 0],
                [-1, 0, 0]
            ])
            wheel_verts = np.dot(wheel_verts, rotation)
            
            # Translate to position
            wheel_verts += np.array(pos)
            
            # Create mesh item
            wheel = gl.GLMeshItem(
                vertexes=wheel_verts,
                faces=wheel_faces,
                faceColors=wheel_colors,
                smooth=False
            )
            self.mechanical_view.addItem(wheel)
            self.wheels.append(wheel)
        
        # Set initial camera position
        self.mechanical_view.setCameraPosition(distance=40, elevation=30, azimuth=45)

    
    def setup_comms_viz(self):
        # Create communication system visualization
        comms_plot = self.comms_view.addPlot()
        comms_plot.hideAxis('left')
        comms_plot.hideAxis('bottom')
        
        # Create a network diagram for communication components
        
        # Define node positions
        positions = {
            'Golf Cart': (2, 0),
            'Mobile App': (0, 2),
            'Cloud Server': (4, 2),
            'GPS Satellite': (2, 4),
            'GSM Tower': (4, 0),
            'Maintenance System': (0, 0)
        }
        
        # Add nodes
        self.comms_nodes = {}
        for name, pos in positions.items():
            node = pg.ScatterPlotItem()
            node.addPoints([pos[0]], [pos[1]], size=30, brush=pg.mkBrush('#89b4fa'))
            comms_plot.addItem(node)
            
            # Add node labels
            text = pg.TextItem(name, anchor=(0.5, 0), color='#cdd6f4')
            text.setPos(pos[0], pos[1] - 0.3)
            comms_plot.addItem(text)
            
            self.comms_nodes[name] = node
        
        # Add connections
        connections = [
            ('Golf Cart', 'Mobile App', 'Bluetooth'),
            ('Golf Cart', 'Cloud Server', 'Wi-Fi'),
            ('Golf Cart', 'GPS Satellite', 'GPS'),
            ('Golf Cart', 'GSM Tower', 'GSM'),
            ('Mobile App', 'Cloud Server', 'Internet'),
            ('Maintenance System', 'Cloud Server', 'Internet'),
            ('Maintenance System', 'Golf Cart', 'Direct Connection')
        ]
        
        for src, dst, label in connections:
            src_pos = positions[src]
            dst_pos = positions[dst]
            
            # Calculate midpoint for label
            mid_x = (src_pos[0] + dst_pos[0]) / 2
            mid_y = (src_pos[1] + dst_pos[1]) / 2
            
            # Add connection line
            line = pg.PlotCurveItem(
                x=[src_pos[0], dst_pos[0]],
                y=[src_pos[1], dst_pos[1]],
                pen=pg.mkPen(color='#7f849c', width=2)
            )
            comms_plot.addItem(line)
            
            # Add connection label
            text = pg.TextItem(label, anchor=(0.5, 0.5), color='#a6adc8')
            text.setPos(mid_x, mid_y)
            comms_plot.addItem(text)
        
        # Set plot range
        comms_plot.setXRange(-0.5, 4.5)
        comms_plot.setYRange(-0.5, 4.5)
    
    def setup_gantt_viz(self):
        # Create Gantt chart visualization
        self.gantt_view.setLabel('left', 'Tasks')
        self.gantt_view.setLabel('bottom', 'Timeline (Weeks)')
        
        # Define project tasks and their timelines
        tasks = [
            ('Requirements', 0, 4),
            ('Design', 3, 8),
            ('Mechanical Prototype', 7, 14),
            ('Electrical System', 9, 16),
            ('Software Development', 10, 20),
            ('Integration', 16, 22),
            ('Testing', 20, 26),
            ('Certification', 24, 28),
            ('Production Setup', 26, 32),
            ('Launch', 32, 34)
        ]
        
        # Create bars for each task
        self.gantt_bars = []
        colors = [
            (0.5, 0.7, 0.9, 0.8),  # Light blue
            (0.3, 0.5, 0.8, 0.8),  # Blue
            (0.2, 0.4, 0.7, 0.8),  # Dark blue
            (0.4, 0.6, 0.8, 0.8),  # Medium blue
            (0.6, 0.8, 1.0, 0.8),  # Sky blue
            (0.3, 0.6, 0.7, 0.8),  # Teal
            (0.5, 0.5, 0.8, 0.8),  # Purple-blue
            (0.4, 0.5, 0.7, 0.8),  # Slate blue
            (0.7, 0.7, 0.9, 0.8),  # Lavender
            (0.2, 0.3, 0.6, 0.8)   # Navy
        ]
        
        for i, (task, start, end) in enumerate(tasks):
            # Create bar
            bar = pg.BarGraphItem(
                x0=[start],
                y0=[i - 0.3],
                width=[end - start],
                height=[0.6],
                brush=pg.mkBrush(colors[i])
            )
            self.gantt_view.addItem(bar)
            self.gantt_bars.append(bar)
            
            # Add task label
            text = pg.TextItem(task, anchor=(1, 0.5), color='#cdd6f4')
            text.setPos(start - 0.5, i)
            self.gantt_view.addItem(text)
        
        # Add current progress line
        self.progress_line = pg.InfiniteLine(
            pos=14,  # Current week
            angle=90,
            pen=pg.mkPen(color='#f38ba8', width=2)
        )
        self.gantt_view.addItem(self.progress_line)
        
        # Set plot range
        self.gantt_view.setXRange(0, 35)
        self.gantt_view.setYRange(-1, len(tasks))
        
        # Set y-axis ticks
        y_ticks = [(i, '') for i in range(len(tasks))]
        self.gantt_view.getAxis('left').setTicks([y_ticks])
    
    def setup_timers(self):
        # Main animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_visualization)
        self.animation_timer.start(50)  # 20 fps
        
        # 3D model animation timer
        self.model_timer = QTimer()
        self.model_timer.timeout.connect(self.update_3d_model)
        self.model_timer.start(50)  # 20 fps
    
    def update_visualization(self):
        # Update frame counter
        self.current_frame += 1
        
        # Update pipeline visualization
        self.update_pipeline()
        
        # Update electrical system visualization
        self.update_electrical_system()
        
        # Update component progress bars with slight animation
        for component, data in self.component_frames.items():
            progress = data['progress']
            current = progress.value()
            
            # Add small random fluctuation to progress for animation effect
            fluctuation = np.random.randint(-2, 3)
            new_value = max(0, min(100, current + fluctuation))
            
            progress.setValue(new_value)
    
    def update_pipeline(self):
        # Highlight current stage in pipeline
        current_stage = (self.current_frame // 100) % len(self.pipeline_nodes)
        
        for i, node in enumerate(self.pipeline_nodes):
            if i == current_stage:
                # Highlight current stage
                node.setBrush(pg.mkBrush('#f5c2e7'))  # Pink
                node.setSize(40)
            elif i < current_stage:
                # Completed stages
                node.setBrush(pg.mkBrush('#a6e3a1'))  # Green
                node.setSize(30)
            else:
                # Future stages
                node.setBrush(pg.mkBrush('#89b4fa'))  # Blue
                node.setSize(30)
    
    def update_electrical_system(self):
        # Animate electrical system to show power flow
        components = list(self.electrical_nodes.keys())
        current_component = components[self.current_frame % len(components)]
        
        for name, node in self.electrical_nodes.items():
            if name == current_component:
                # Highlight current component
                node.setBrush(pg.mkBrush('#f5c2e7'))  # Pink
                node.setSize(40)
            else:
                # Other components
                node.setBrush(pg.mkBrush('#89b4fa'))  # Blue
                node.setSize(30)
    
    def update_3d_model(self):
        # Rotate the 3D model slowly
        if hasattr(self, 'chassis_mesh'):
            # Rotate chassis and roof
            self.chassis_mesh.rotate(0.5, 0, 0, 1)  # Rotate around z-axis
            self.roof_mesh.rotate(0.5, 0, 0, 1)  # Rotate around z-axis
            
            # For custom wheel meshes, we need to rotate them differently
            for wheel in self.wheels:
                wheel.rotate(0.5, 0, 0, 1)  # Rotate around z-axis

    
    def change_viz_mode(self):
        # Change visualization mode based on selection
        mode = self.viz_mode_combo.currentText()
        print(f"Visualization mode changed to: {mode}")
        
        # Switch to appropriate tab based on mode
        if mode == "System Overview":
            self.tab_widget.setCurrentIndex(0)
        elif mode == "Component Details":
            # Choose appropriate tab based on current component focus
            component = self.component_combo.currentText()
            if component == "Power System" or component == "Control Electronics":
                self.tab_widget.setCurrentIndex(1)  # Electrical tab
            elif component == "Software & UI":
                self.tab_widget.setCurrentIndex(2)  # Software tab
            elif component == "Chassis & Mechanical":
                self.tab_widget.setCurrentIndex(3)  # Mechanical tab
            elif component == "Communication":
                self.tab_widget.setCurrentIndex(4)  # Comms tab
        elif mode == "Data Flow":
            self.tab_widget.setCurrentIndex(4)  # Comms tab
        elif mode == "3D Model":
            self.tab_widget.setCurrentIndex(3)  # Mechanical tab
    
    def change_component_focus(self):
        # Change component focus based on selection
        component = self.component_combo.currentText()
        print(f"Component focus changed to: {component}")
    def filter_by_status(self):
        # Filter components by status
        status = self.status_combo.currentText()
        print(f"Status filter changed to: {status}")
        
        # Update component visibility based on status
        for component, data in self.component_frames.items():
            frame = data['frame']
            status_label = data['status']
            
            if status == "All Statuses":
                frame.setVisible(True)
            elif status == status_label.text():
                frame.setVisible(True)
            else:
                frame.setVisible(False)
    
    def export_diagram(self):
        # Export current visualization as image
        current_tab = self.tab_widget.currentWidget()
        
        # Create a QPixmap to capture the current tab
        pixmap = QPixmap(current_tab.size())
        current_tab.render(pixmap)
        
        # Get current timestamp for filename
        timestamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
        filename = f"proton_smart_cart_{timestamp}.png"
        
        # Save the pixmap to file
        pixmap.save(filename)
        print(f"Diagram exported to: {filename}")
        
        # Show confirmation message
        QMessageBox.information(
            self,
            "Export Successful",
            f"Diagram has been exported to:\n{filename}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Apply dark theme palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.WindowText, QColor(205, 214, 244))
    palette.setColor(QPalette.Base, QColor(24, 24, 37))
    palette.setColor(QPalette.AlternateBase, QColor(49, 50, 68))
    palette.setColor(QPalette.ToolTipBase, QColor(30, 30, 46))
    palette.setColor(QPalette.ToolTipText, QColor(205, 214, 244))
    palette.setColor(QPalette.Text, QColor(205, 214, 244))
    palette.setColor(QPalette.Button, QColor(49, 50, 68))
    palette.setColor(QPalette.ButtonText, QColor(205, 214, 244))
    palette.setColor(QPalette.BrightText, QColor(245, 194, 231))
    palette.setColor(QPalette.Link, QColor(137, 180, 250))
    palette.setColor(QPalette.Highlight, QColor(137, 180, 250))
    palette.setColor(QPalette.HighlightedText, QColor(30, 30, 46))
    app.setPalette(palette)
    
    # Set stylesheet for custom styling
    app.setStyleSheet("""
        QMainWindow, QDialog {
            background-color: #1e1e2e;
        }
        QTabWidget::pane {
            border: 1px solid #45475a;
            border-radius: 4px;
            background-color: #1e1e2e;
        }
        QTabBar::tab {
            background-color: #313244;
            color: #cdd6f4;
            padding: 8px 16px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #45475a;
            color: #cdd6f4;
        }
        QFrame {
            border-radius: 4px;
        }
        QLabel {
            color: #cdd6f4;
        }
        QPushButton {
            background-color: #45475a;
            color: #cdd6f4;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #585b70;
        }
        QPushButton:pressed {
            background-color: #7f849c;
        }
        QComboBox {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            border-radius: 4px;
            padding: 4px 8px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #313244;
            color: #cdd6f4;
            selection-background-color: #45475a;
        }
        QProgressBar {
            border: 1px solid #45475a;
            border-radius: 4px;
            background-color: #313244;
            text-align: center;
            color: #cdd6f4;
        }
        QProgressBar::chunk {
            background-color: #89b4fa;
            border-radius: 3px;
        }
    """)
    
    window = ProtonSmartCartViz()
    window.show()
    
    sys.exit(app.exec_())
