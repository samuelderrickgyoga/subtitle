import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QPushButton, QSizePolicy, QGridLayout, QFrame)
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon
import pyqtgraph.opengl as gl
from scipy.io import wavfile
from scipy.signal import stft
from librosa.feature import mfcc, chroma_stft
import librosa
import queue
import sounddevice as sd

class RealTimeKeyIdentificationViz(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup UI
        self.setWindowTitle("Real-Time Vocal Key Identification System")
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
        """)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create header
        self.create_header()
        
        # Create system visualization area
        self.create_system_visualization()
        
        # Create data flow visualization
        self.create_data_flow_viz()
        
        # Create controls
        self.create_controls()
        
        # Setup data and state
        self.setup_data()
        
        # Setup timers for animations
        self.setup_timers()
        
    def create_header(self):
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("Real-Time Vocal Key Identification System")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #89b4fa;")
        
        subtitle_label = QLabel("Interactive Pipeline Visualization")
        subtitle_label.setStyleSheet("font-size: 16px; color: #a6adc8;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)
        
        self.main_layout.addWidget(header_frame)
    
    def create_system_visualization(self):
        self.system_viz_frame = QFrame()
        self.system_viz_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        system_viz_layout = QGridLayout(self.system_viz_frame)
        
        # Labels for system blocks
        input_label = QLabel("Audio Input")
        teacher_label = QLabel("Teacher Model\n(Contrastive SSL)")
        student_label = QLabel("Student Model\n(Knowledge Distillation)")
        phonation_label = QLabel("Phonation-Aware\nFeature Extraction")
        output_label = QLabel("Key Prediction")
        
        for label in [input_label, teacher_label, student_label, phonation_label, output_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold; color: #89b4fa;")
        
        # Create plots for system blocks
        self.input_plot = pg.PlotWidget(title="Raw Audio Input")
        self.teacher_plot = pg.PlotWidget(title="Teacher Model Embeddings")
        self.student_plot = pg.PlotWidget(title="Student Model")
        self.phonation_plot = pg.PlotWidget(title="Phonation Features")
        self.output_plot = pg.PlotWidget(title="Key Prediction")
        
        # Style all plots
        for plot in [self.input_plot, self.teacher_plot, self.student_plot, self.phonation_plot, self.output_plot]:
            plot.setBackground('#313244')
            plot.showGrid(x=True, y=True, alpha=0.3)
            
        # Add plots to layout
        system_viz_layout.addWidget(input_label, 0, 0)
        system_viz_layout.addWidget(self.input_plot, 1, 0)
        
        system_viz_layout.addWidget(teacher_label, 0, 1)
        system_viz_layout.addWidget(self.teacher_plot, 1, 1)
        
        system_viz_layout.addWidget(student_label, 0, 2)
        system_viz_layout.addWidget(self.student_plot, 1, 2)
        
        system_viz_layout.addWidget(phonation_label, 2, 0)
        system_viz_layout.addWidget(self.phonation_plot, 3, 0)
        
        system_viz_layout.addWidget(output_label, 2, 2)
        system_viz_layout.addWidget(self.output_plot, 3, 2)
        
        # Setup 3D embedding visualization in the middle bottom
        self.embedding_view = gl.GLViewWidget()
        self.embedding_view.setCameraPosition(distance=40)
        self.embedding_view.setBackgroundColor('#313244')
        
        embedding_label = QLabel("Contrastive Learning Embeddings (3D)")
        embedding_label.setAlignment(Qt.AlignCenter)
        embedding_label.setStyleSheet("font-weight: bold; color: #89b4fa;")
        
        system_viz_layout.addWidget(embedding_label, 2, 1)
        system_viz_layout.addWidget(self.embedding_view, 3, 1)
        
        self.main_layout.addWidget(self.system_viz_frame)
    
    def create_data_flow_viz(self):
        data_flow_frame = QFrame()
        data_flow_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        data_flow_frame.setFixedHeight(200)
        data_flow_layout = QVBoxLayout(data_flow_frame)
        
        # Create title
        flow_title = QLabel("Data Flow Pipeline")
        flow_title.setAlignment(Qt.AlignCenter)
        flow_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #89b4fa;")
        data_flow_layout.addWidget(flow_title)
        
        # Create data flow plot
        self.flow_plot = pg.PlotWidget()
        self.flow_plot.setBackground('#313244')
        self.flow_plot.hideAxis('left')
        self.flow_plot.hideAxis('bottom')
        data_flow_layout.addWidget(self.flow_plot)
        
        self.main_layout.addWidget(data_flow_frame)
    
    def create_controls(self):
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        
        # Create visualization mode selector
        viz_mode_label = QLabel("Visualization Mode:")
        self.viz_mode_combo = QComboBox()
        self.viz_mode_combo.addItems([
            "Full Pipeline", 
            "Contrastive SSL", 
            "Knowledge Distillation", 
            "Feature Extraction"
        ])
        self.viz_mode_combo.currentIndexChanged.connect(self.change_viz_mode)
        
        # Create audio source selector
        audio_source_label = QLabel("Audio Source:")
        self.audio_source_combo = QComboBox()
        self.audio_source_combo.addItems([
            "Sample Recording", 
            "Simulated Input", 
            "Live Microphone Input"
        ])
        self.audio_source_combo.currentIndexChanged.connect(self.change_audio_source)
        
        # Create phonation mode selector
        phonation_label = QLabel("Phonation Type:")
        self.phonation_combo = QComboBox()
        self.phonation_combo.addItems([
            "Modal", 
            "Falsetto", 
            "Breathy", 
            "Pressed"
        ])
        self.phonation_combo.currentIndexChanged.connect(self.change_phonation_mode)
        
        # Create start/stop button
        self.start_stop_btn = QPushButton("Start Visualization")
        self.start_stop_btn.clicked.connect(self.toggle_visualization)
        
        # Add widgets to layout
        controls_layout.addWidget(viz_mode_label)
        controls_layout.addWidget(self.viz_mode_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(audio_source_label)
        controls_layout.addWidget(self.audio_source_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(phonation_label)
        controls_layout.addWidget(self.phonation_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(self.start_stop_btn)
        
        self.main_layout.addWidget(controls_frame)
    
    def setup_data(self):
        # Initialize sample data
        self.is_running = False
        self.current_frame = 0
        self.audio_data = np.sin(np.linspace(0, 10 * np.pi, 1000)) * 0.5
        self.buffer_size = 1000
        self.audio_buffer = np.zeros(self.buffer_size)
        
        # Setup data structures for visualization
        self.setup_input_viz()
        self.setup_teacher_viz()
        self.setup_student_viz()
        self.setup_phonation_viz()
        self.setup_output_viz()
        self.setup_embedding_viz()
        self.setup_flow_viz()
        
        # Audio processing queue
        self.audio_queue = queue.Queue(maxsize=10)
        
    def setup_input_viz(self):
        # Raw audio input waveform
        self.input_curve = self.input_plot.plot(self.audio_buffer, pen=pg.mkPen(color='#89b4fa', width=2))
        
    def setup_teacher_viz(self):
        # Representation of high-dimensional embeddings
        teacher_x = np.linspace(0, 100, 100)
        teacher_y = np.zeros(100)
        self.teacher_curve = self.teacher_plot.plot(teacher_x, teacher_y, pen=pg.mkPen(color='#f38ba8', width=2))
        
    def setup_student_viz(self):
        # Knowledge distillation visualization
        student_x = np.linspace(0, 100, 100)
        student_y = np.zeros(100)
        
        # Create soft targets (blurred)
        self.soft_targets_curve = self.student_plot.plot(student_x, student_y, 
                                                       pen=pg.mkPen(color='#f9e2af', width=2, style=Qt.DashLine))
        
        # Create student predictions
        self.student_curve = self.student_plot.plot(student_x, student_y,
                                                   pen=pg.mkPen(color='#a6e3a1', width=2))
    
    def setup_phonation_viz(self):
        # Phonation features visualization (as spectrogram)
        phonation_img = np.zeros((100, 100))
        self.phonation_img_item = pg.ImageItem(phonation_img)
        self.phonation_plot.addItem(self.phonation_img_item)
        
        # Add color map - FIX: Ensure position and colors arrays are the same length
        position = np.linspace(0, 1, 4)  # Changed from 5 to 4 to match colors length
        colors = [(0, 0, 100), (0, 50, 200), (100, 100, 255), (255, 255, 255)]
        color_map = pg.ColorMap(position, colors)
        self.phonation_img_item.setLookupTable(color_map.getLookupTable(0.0, 1.0, 256))
        
    def setup_output_viz(self):
        # Key prediction visualization
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        x = np.arange(len(keys))
        y = np.zeros(len(keys))
        
        self.output_bars = pg.BarGraphItem(x=x, height=y, width=0.6, brush='#b4befe')
        self.output_plot.addItem(self.output_bars)
        self.output_plot.setYRange(0, 1)
        self.output_plot.setXRange(-0.5, len(keys) - 0.5)
        
        # Set x-axis ticks to musical keys
        axis = self.output_plot.getAxis('bottom')
        axis.setTicks([[(i, key) for i, key in enumerate(keys)]])
    
    def setup_embedding_viz(self):
        # 3D scatter plot for embedding visualization
        # Create a grid
        gx = gl.GLGridItem()
        gx.setSize(50, 50, 50)
        gx.setSpacing(5, 5, 5)
        self.embedding_view.addItem(gx)
        
        # Create scatter points for embeddings
        pos = np.random.normal(size=(100, 3))
        size = np.random.random(100) * 0.5 + 0.5
        color = np.zeros((100, 4))
        color[:, 0] = np.linspace(0.3, 0.9, 100)  # Red
        color[:, 1] = np.linspace(0.2, 0.7, 100)  # Green
        color[:, 2] = 1.0  # Blue
        color[:, 3] = 0.8  # Alpha
        
        self.embedding_scatter = gl.GLScatterPlotItem(pos=pos, size=size, color=color)
        self.embedding_view.addItem(self.embedding_scatter)
    
    def setup_flow_viz(self):
        # Data flow visualization
        # Define stages in the pipeline
        stages = [
            "Audio Input", "Pre-processing", "Feature Extraction", 
            "Teacher Model", "Student Model", "Phonation Analysis", "Key Detection"
        ]
        
        # Create markers for data flowing through the pipeline
        self.flow_markers = []
        
        # Set up x-axis
        self.flow_plot.setXRange(0, len(stages) - 1)
        self.flow_plot.setYRange(-1, 1)
        
        # Add stage labels
        axis = self.flow_plot.getAxis('bottom')
        axis.setTicks([[(i, stage) for i, stage in enumerate(stages)]])
        
        # Add connection lines
        for i in range(len(stages) - 1):
            line = pg.PlotCurveItem(
                x=[i, i+1],
                y=[0, 0],
                pen=pg.mkPen(color='#7f849c', width=3)
            )
            self.flow_plot.addItem(line)
        
        # Add stage nodes
        for i in range(len(stages)):
            node = pg.ScatterPlotItem()
            node.addPoints([i], [0], size=15, brush=pg.mkBrush('#89b4fa'))
            self.flow_plot.addItem(node)
            
            # Add node labels
            text = pg.TextItem(stages[i], anchor=(0.5, 0), color='#cdd6f4')
            text.setPos(i, -0.2)
            self.flow_plot.addItem(text)
        
        # Add data flow markers
        for i in range(5):  # 5 data markers
            marker = pg.ScatterPlotItem()
            marker.addPoints([-1], [0], size=10, brush=pg.mkBrush('#f5c2e7'))
            self.flow_plot.addItem(marker)
            self.flow_markers.append(marker)
    
    def setup_timers(self):
        # Main animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_visualization)
        
        # Flow animation timer
        self.flow_timer = QTimer()
        self.flow_timer.timeout.connect(self.update_flow)
        
        # Audio processing timer
        self.audio_timer = QTimer()
        self.audio_timer.timeout.connect(self.process_audio)
        
        # 3D embedding animation timer
        self.embedding_timer = QTimer()
        self.embedding_timer.timeout.connect(self.update_embeddings)
    
    def toggle_visualization(self):
        if not self.is_running:
            self.is_running = True
            self.start_stop_btn.setText("Stop Visualization")
            
            # Start timers
            self.animation_timer.start(50)  # 20 fps
            self.flow_timer.start(200)      # Flow updates
            self.audio_timer.start(100)     # Audio processing
            self.embedding_timer.start(50)  # Embedding animation
            
            # Start audio if needed
            if self.audio_source_combo.currentText() == "Live Microphone Input":
                self.start_audio_capture()
        else:
            self.is_running = False
            self.start_stop_btn.setText("Start Visualization")
            
            # Stop timers
            self.animation_timer.stop()
            self.flow_timer.stop()
            self.audio_timer.stop()
            self.embedding_timer.stop()
            
            # Stop audio if needed
            if hasattr(self, 'audio_stream') and self.audio_stream:
                self.audio_stream.stop()
                self.audio_stream.close()
    
    def change_viz_mode(self):
        # Change visualization mode based on selection
        mode = self.viz_mode_combo.currentText()
        print(f"Visualization mode changed to: {mode}")
        
    def change_audio_source(self):
        # Change audio source based on selection
        source = self.audio_source_combo.currentText()
        print(f"Audio source changed to: {source}")
        
        # Reset audio data
        self.audio_buffer = np.zeros(self.buffer_size)
        self.input_curve.setData(self.audio_buffer)
        
        # Handle live microphone initialization if running
        if self.is_running and source == "Live Microphone Input":
            self.start_audio_capture()
        elif hasattr(self, 'audio_stream') and self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream.close()
    
    def change_phonation_mode(self):
        # Change phonation mode based on selection
        mode = self.phonation_combo.currentText()
        print(f"Phonation mode changed to: {mode}")
    
    def start_audio_capture(self):
        # Setup audio capture from microphone
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
            # Convert to mono and put in queue
            audio_mono = np.mean(indata, axis=1)
            try:
                self.audio_queue.put_nowait(audio_mono)
            except queue.Full:
                pass  # Queue is full, skip this frame
        
        try:
            self.audio_stream = sd.InputStream(
                callback=audio_callback,
                channels=1,
                samplerate=44100,
                blocksize=1024
            )
            self.audio_stream.start()
        except Exception as e:
            print(f"Error starting audio stream: {e}")
    
    def process_audio(self):
        if not self.is_running:
            return
            
        audio_source = self.audio_source_combo.currentText()
        
        if audio_source == "Live Microphone Input":
            # Process audio from microphone queue
            try:
                audio_chunk = self.audio_queue.get_nowait()
                # Update buffer with new data (rolling window)
                self.audio_buffer = np.roll(self.audio_buffer, -len(audio_chunk))
                self.audio_buffer[-len(audio_chunk):] = audio_chunk
            except queue.Empty:
                pass  # No new audio data
        else:
            # Simulated audio
            t = np.linspace(0, 2*np.pi, 100)
            current_t = (self.current_frame % 100) * 2*np.pi/100
            new_chunk = np.sin(t + current_t) * 0.5
            
            if audio_source == "Sample Recording":
                # Add some harmonic components to simulate a recording
                new_chunk += np.sin(2*t + current_t*1.3) * 0.3
                new_chunk += np.sin(3*t + current_t*0.7) * 0.15
            
            # Update buffer with new data (rolling window)
            chunk_size = len(new_chunk)
            self.audio_buffer = np.roll(self.audio_buffer, -chunk_size)
            self.audio_buffer[-chunk_size:] = new_chunk
    
    def update_visualization(self):
        if not self.is_running:
            return
            
        # Update frame counter
        self.current_frame += 1
        
        # Update input visualization
        self.input_curve.setData(self.audio_buffer)
        
        # Update teacher model visualization (high-dim embeddings projection)
        t = np.linspace(0, 4*np.pi, 100)
        teacher_y = np.sin(t + self.current_frame/10) * 0.5 + np.sin(2*t + self.current_frame/8) * 0.3
        self.teacher_curve.setData(t, teacher_y)
        
        # Update student model visualization (knowledge distillation)
        # Soft targets (teacher outputs)
        soft_targets = np.sin(t + self.current_frame/10) * 0.5 + np.sin(2*t + self.current_frame/8) * 0.3
        soft_targets += np.random.normal(0, 0.05, size=len(t))  # Add noise
        
        # Student predictions (trying to match teacher)
        student_preds = np.sin(t + self.current_frame/10) * 0.5 + np.sin(2*t + self.current_frame/8) * 0.3
        student_preds += np.random.normal(0, 0.15, size=len(t))  # Add more noise
        
        self.soft_targets_curve.setData(t, soft_targets)
        self.student_curve.setData(t, student_preds)
        
        # Update phonation visualization
        phonation_mode = self.phonation_combo.currentText()
        spec = self.generate_phonation_spectrogram(phonation_mode)
        self.phonation_img_item.setImage(spec.T)
        
        # Update key prediction visualization
        key_probs = self.generate_key_prediction()
        self.output_bars.setOpts(height=key_probs)
    
    def update_flow(self):
        if not self.is_running:
            return
            
        # Update data flow markers
        for i, marker in enumerate(self.flow_markers):
            # Calculate position based on time offset
            pos = (self.current_frame / 20 + i * 1.2) % 8 - 1
            
            if 0 <= pos < 6:
                # Data point is within the pipeline
                marker.setData([pos], [0])
            else:
                # Data point is outside the pipeline
                marker.setData([-2], [0])  # Hide it outside view
    
    def update_embeddings(self):
        if not self.is_running:
            return
            
        # Update 3D embedding visualization
        # Rotate current points
        pos = self.embedding_scatter.pos()
        
        # Apply rotation and small random movement
        angle = self.current_frame * 0.01
        rotation = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        
        new_pos = np.dot(pos, rotation)
        new_pos += np.random.normal(0, 0.1, size=new_pos.shape)  # Add small random movement
        
        # Update scatter plot
        self.embedding_scatter.setData(pos=new_pos)
    
    def generate_phonation_spectrogram(self, mode):
        # Generate different spectrograms based on phonation mode
        t = np.linspace(0, 10, 100)
        spec = np.zeros((100, 100))
        
        if mode == "Modal":
            # Strong fundamental, balanced harmonics
            for i in range(100):
                harmonic_strength = np.exp(-i/20)
                freq = i / 2
                spec[:, i] = np.sin(2*np.pi*freq*t + self.current_frame/10) * harmonic_strength
        
        elif mode == "Falsetto":
            # Weaker fundamental, stronger high harmonics, narrower bandwidth
            for i in range(100):
                if i < 20:
                    harmonic_strength = np.exp(-(i-20)**2/200)
                else:
                    harmonic_strength = np.exp(-(i-50)**2/500)
                freq = i / 1.5
                spec[:, i] = np.sin(2*np.pi*freq*t + self.current_frame/10) * harmonic_strength
        
        elif mode == "Breathy":
            # More noise, weaker harmonics
            for i in range(100):
                harmonic_strength = np.exp(-i/30) * 0.6
                freq = i / 2
                spec[:, i] = np.sin(2*np.pi*freq*t + self.current_frame/10) * harmonic_strength
            
            # Add noise
            spec += np.random.normal(0, 0.2, size=spec.shape)
            
        elif mode == "Pressed":
            # Stronger harmonics, more energy
            for i in range(100):
                harmonic_strength = np.exp(-i/15) * 1.2
                if i % 2 == 0:  # Emphasize even harmonics
                    harmonic_strength *= 1.3
                freq = i / 2
                spec[:, i] = np.sin(2*np.pi*freq*t + self.current_frame/10) * harmonic_strength
        
        # Add time-varying component
        modulation = np.sin(self.current_frame / 20)
        spec *= (1 + modulation * 0.2)
        
        # Normalize
        spec = (spec - spec.min()) / (spec.max() - spec.min() + 1e-9)
        return spec
    
    def generate_key_prediction(self):
        # Generate simulated key prediction probabilities
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        probs = np.zeros(len(keys))
        
        # Make a primary prediction that shifts over time
        primary_idx = (self.current_frame // 100) % len(keys)
        probs[primary_idx] = 0.7 + 0.2 * np.sin(self.current_frame / 30)
        
        # Add probability to neighboring keys
        for i in range(len(keys)):
            distance = min(abs(i - primary_idx), len(keys) - abs(i - primary_idx))
            if distance > 0:
                probs[i] = max(0, 0.6 - distance * 0.15) * (0.8 + 0.2 * np.sin(self.current_frame / 20 + i))
        
        # Normalize
        return probs / (probs.sum() + 1e-9)

def main():
    app = QApplication(sys.argv)
    window = RealTimeKeyIdentificationViz()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()